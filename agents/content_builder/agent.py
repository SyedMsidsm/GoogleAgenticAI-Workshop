from google.adk.agents import Agent

MODEL = "gemini-2.5-flash"

# ============================================================
# STEP 6 — TODO: Define the Content Builder Agent
#
# Create an Agent named "content_builder" that:
#   - Uses the MODEL variable above
#   - Has a description: "Transforms research findings into a structured course."
#   - Has an instruction to format the approved research as a
#     well-structured course module using Markdown headings
#     (# for title, ## for sections)
#
# Then set:  root_agent = content_builder
# ============================================================
