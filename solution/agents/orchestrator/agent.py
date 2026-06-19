import json
from typing import AsyncGenerator

from google.adk.agents import BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.events import Event, EventActions
import httpx


def create_save_output_callback(key: str):
    """Saves the agent's last text output into session state under `key`."""
    def _callback(ctx: CallbackContext, **kwargs) -> None:
        for event in reversed(ctx.session.events):
            if event.author == ctx.agent_name and event.content and event.content.parts:
                text = event.content.parts[0].text
                if text:
                    if key == "judge_feedback" and text.strip().startswith("{"):
                        try:
                            ctx.state[key] = json.loads(text)
                        except json.JSONDecodeError:
                            ctx.state[key] = text
                    else:
                        ctx.state[key] = text
                    return
    return _callback


def plain_client(timeout: float = 300.0) -> httpx.AsyncClient:
    return httpx.AsyncClient(follow_redirects=True, timeout=timeout)


# Remote agent connections
researcher = RemoteA2aAgent(
    name="researcher",
    agent_card="http://localhost:8001/a2a/agent/.well-known/agent-card.json",
    description="Gathers information using Google Search.",
    after_agent_callback=create_save_output_callback("research_findings"),
    httpx_client=plain_client(),
)

judge = RemoteA2aAgent(
    name="judge",
    agent_card="http://localhost:8002/a2a/agent/.well-known/agent-card.json",
    description="Evaluates research quality and returns structured feedback.",
    after_agent_callback=create_save_output_callback("judge_feedback"),
    httpx_client=plain_client(),
)

content_builder = RemoteA2aAgent(
    name="content_builder",
    agent_card="http://localhost:8003/a2a/agent/.well-known/agent-card.json",
    description="Builds a structured course from approved research.",
    httpx_client=plain_client(),
)


class EscalationChecker(BaseAgent):
    """Reads judge_feedback from session state and breaks the loop on 'pass'."""

    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        feedback = ctx.session.state.get("judge_feedback")
        is_pass = False
        if isinstance(feedback, dict) and feedback.get("status") == "pass":
            is_pass = True
        elif isinstance(feedback, str) and '"status": "pass"' in feedback:
            is_pass = True

        if is_pass:
            yield Event(author=self.name, actions=EventActions(escalate=True))
        else:
            yield Event(author=self.name)


escalation_checker = EscalationChecker(name="escalation_checker")

research_loop = LoopAgent(
    name="research_loop",
    description="Loops Researcher → Judge → EscalationChecker until quality passes.",
    sub_agents=[researcher, judge, escalation_checker],
    max_iterations=3,
)

root_agent = SequentialAgent(
    name="course_creation_pipeline",
    description="Researches a topic then builds a course from the approved findings.",
    sub_agents=[research_loop, content_builder],
)
