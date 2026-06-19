import json
from typing import AsyncGenerator

from google.adk.agents import BaseAgent, LoopAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.events import Event, EventActions
import httpx

# ── Helpers (provided) ───────────────────────────────────────────────────────

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
    """Plain httpx client — no auth needed for localhost."""
    return httpx.AsyncClient(follow_redirects=True, timeout=timeout)


# ── STEP 7 — TODO: Connect to remote agents ─────────────────────────────────
#
# Create three RemoteA2aAgent instances:
#
#   researcher  →  http://localhost:8001/a2a/agent/.well-known/agent-card.json
#                  after_agent_callback = create_save_output_callback("research_findings")
#
#   judge       →  http://localhost:8002/a2a/agent/.well-known/agent-card.json
#                  after_agent_callback = create_save_output_callback("judge_feedback")
#
#   content_builder → http://localhost:8003/a2a/agent/.well-known/agent-card.json
#
# For each, pass:  httpx_client=plain_client()
# ─────────────────────────────────────────────────────────────────────────────


# ── STEP 8 — TODO: EscalationChecker ────────────────────────────────────────
#
# Create a class EscalationChecker(BaseAgent) that:
#   - Reads ctx.session.state.get("judge_feedback")
#   - If status == "pass"  → yield Event(author=self.name, actions=EventActions(escalate=True))
#   - Otherwise            → yield Event(author=self.name)
#
# Then instantiate:  escalation_checker = EscalationChecker(name="escalation_checker")
# ─────────────────────────────────────────────────────────────────────────────


# ── STEPS 9 & 10 — TODO: Wire up the pipeline ───────────────────────────────
#
# 1. Create a LoopAgent named "research_loop":
#       sub_agents=[researcher, judge, escalation_checker], max_iterations=3
#
# 2. Set root_agent to a SequentialAgent named "course_creation_pipeline":
#       sub_agents=[research_loop, content_builder]
# ─────────────────────────────────────────────────────────────────────────────
