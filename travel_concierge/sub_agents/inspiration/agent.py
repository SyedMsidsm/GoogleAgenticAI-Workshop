"""Inspiration agent — helps users discover their dream destination."""

from google.adk.agents import Agent

from ._bootstrap import MODEL, memorize

inspiration_agent = Agent(
    model=MODEL,
    name="inspiration_agent",
    description=(
        "Helps users discover travel destinations and activities. "
        "Use this agent when the user wants ideas, recommendations, or "
        "things to do at a location."
    ),
    instruction="""
    You are an enthusiastic travel inspiration specialist.
    Your goal is to spark excitement and help users discover their perfect destination.

    - Ask about the user's interests, budget range, and travel style (adventure, relaxation, culture, food...).
    - Suggest 2-3 specific destinations that match their interests, with a short description of each.
    - For each destination, mention 3 must-do activities or experiences.
    - Use your knowledge to suggest great destinations with accurate information.
    - Once the user picks a destination, use memorize to save:
        - key="destination", value=<chosen city/country>
        - key="travel_interests", value=<their stated interests>
    - Be concise and enthusiastic. Use emojis sparingly to add warmth.
    """,
    tools=[memorize],
)

root_agent = inspiration_agent
