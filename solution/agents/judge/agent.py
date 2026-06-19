from typing import Literal
from google.adk.agents import Agent
from pydantic import BaseModel, Field

MODEL = "gemini-2.5-flash"


class JudgeFeedback(BaseModel):
    """Structured feedback from the Judge agent."""
    status: Literal["pass", "fail"] = Field(
        description="'pass' if research is sufficient, 'fail' if more work is needed."
    )
    feedback: str = Field(
        description="Detailed feedback on what is missing. If 'pass', a brief confirmation."
    )


judge = Agent(
    name="judge",
    model=MODEL,
    description="Evaluates research findings for completeness and accuracy.",
    instruction="""
    You are a strict editor. Evaluate the research findings against the
    user's original request.
    If the findings are missing key information, return status='fail' with
    specific feedback on what to improve.
    If they are comprehensive and accurate, return status='pass'.
    """,
    output_schema=JudgeFeedback,
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)

root_agent = judge
