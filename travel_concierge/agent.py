"""Travel Concierge — root agent orchestrating the full traveler experience."""

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext

from travel_concierge import MODEL


def _init_session_state(callback_context: CallbackContext) -> None:
    """Pre-populate session state keys so instruction templates don't fail."""
    defaults = {"destination": "Not set", "travel_dates": "Not set", "itinerary": "None yet"}
    for key, value in defaults.items():
        if key not in callback_context.state:
            callback_context.state[key] = value


from travel_concierge.sub_agents.inspiration.agent import inspiration_agent
from travel_concierge.sub_agents.planning.agent import planning_agent
from travel_concierge.sub_agents.in_trip.agent import in_trip_agent

INSTRUCTION = """
You are an exclusive AI travel concierge. You help users through every stage of their journey:

1. **Inspiration** — When the user wants ideas, destinations, or things to do, transfer to `inspiration_agent`.
2. **Planning** — When the user has a destination and is ready to find flights, hotels, or build an itinerary, transfer to `planning_agent`.
3. **In-Trip** — When the user is currently traveling and needs real-time help (flight status, local tips, directions), transfer to `in_trip_agent`.

Keep your own responses short — just enough to greet the user or explain the handoff.
Ask clarifying questions before transferring if the user's intent is unclear.

Current user context (from memory):
- Destination: {destination}
- Travel dates: {travel_dates}
- Itinerary: {itinerary}
"""

root_agent = Agent(
    model=MODEL,
    name="travel_concierge",
    description="A personal AI travel concierge covering trip inspiration, planning, and in-trip support.",
    instruction=INSTRUCTION,
    sub_agents=[
        inspiration_agent,
        planning_agent,
        in_trip_agent,
    ],
    before_agent_callback=_init_session_state,
)
