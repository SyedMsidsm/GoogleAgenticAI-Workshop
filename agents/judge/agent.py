from typing import Literal
from google.adk.agents import Agent
from pydantic import BaseModel, Field

MODEL = "gemini-2.5-flash"

# ============================================================
# STEP 4 — TODO: Define the JudgeFeedback schema
#
# Create a Pydantic BaseModel called JudgeFeedback with:
#   - status: Literal["pass", "fail"]  (with a Field description)
#   - feedback: str                    (with a Field description)
# ============================================================


# ============================================================
# STEP 4 — TODO: Define the Judge Agent
#
# Create an Agent named "judge" that:
#   - Uses the MODEL variable above
#   - Has a description: "Evaluates research findings for quality."
#   - Has an instruction to return status='fail' if findings are
#     insufficient, and status='pass' if they are comprehensive
#   - Uses output_schema=JudgeFeedback
#   - Sets disallow_transfer_to_parent=True
#   - Sets disallow_transfer_to_peers=True
#
# Then set:  root_agent = judge
# ============================================================
