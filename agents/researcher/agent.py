from google.adk.agents import Agent
from google.adk.tools.google_search_tool import google_search

MODEL = "gemini-2.5-flash"

# ============================================================
# STEP 3 — TODO: Define the Researcher Agent
#
# Create an Agent named "researcher" that:
#   - Uses the MODEL variable above
#   - Has a description: "Gathers information on a topic using Google Search."
#   - Has an instruction telling it to summarise findings clearly,
#     and to refine searches when given feedback
#   - Uses tools=[google_search]
#
# Then set:  root_agent = researcher
# ============================================================
