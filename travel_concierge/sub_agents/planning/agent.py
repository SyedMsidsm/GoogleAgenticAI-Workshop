"""Planning agent — helps users find flights and hotels and build an itinerary."""

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from travel_concierge import MODEL
from travel_concierge.tools.flights import search_flights, select_seat
from travel_concierge.tools.hotels import search_hotels, select_room
from travel_concierge.tools.memory import memorize, recall


# A focused sub-agent just for building the final itinerary summary
itinerary_agent = Agent(
    model=MODEL,
    name="itinerary_agent",
    description="Compiles the selected flights, hotel, and activities into a final itinerary.",
    instruction="""
    You are given the user's travel selections from session state.
    Compile everything into a clear, well-formatted itinerary with:
    - A title line: "🗺️ Your Trip to <destination>"
    - Flight details (outbound + return)
    - Hotel details
    - A day-by-day outline with suggested activities
    Keep it concise and easy to read.
    Use the recall tool to fetch: destination, travel_dates, selected_flight, selected_hotel.
    Then save the final itinerary text using memorize with key="itinerary".
    """,
    tools=[memorize, recall],
    disallow_transfer_to_parent=True,
    disallow_transfer_to_peers=True,
)


planning_agent = Agent(
    model=MODEL,
    name="planning_agent",
    description=(
        "Helps users find and select flights and hotels, then builds a trip itinerary. "
        "Use this agent once the user has chosen a destination and is ready to plan dates."
    ),
    instruction="""
    You are a meticulous trip planner.

    Step 1 — Gather details:
    - Ask for departure city, destination, travel dates, and number of travelers if not provided.
    - Use recall to check if 'destination' is already saved.
    - Save travel dates: memorize(key="travel_dates", value="<dates>")

    Step 2 — Flights:
    - Use search_flights to show options. Present them clearly (airline, time, price).
    - Once the user selects a flight, use select_seat to show seat options.
    - Save the selection: memorize(key="selected_flight", value="<flight_id> seat <seat>")

    Step 3 — Hotel:
    - Use search_hotels for their destination and dates. Present top 3 options.
    - Once selected, use select_room to show room types.
    - Save: memorize(key="selected_hotel", value="<hotel_name> - <room_type>")

    Step 4 — Itinerary:
    - Once flights and hotel are confirmed, hand off to itinerary_agent to compile the full plan.
    - Present the itinerary to the user clearly.

    Be thorough but conversational. Guide the user through each step one at a time.
    """,
    tools=[
        search_flights,
        select_seat,
        search_hotels,
        select_room,
        memorize,
        recall,
        AgentTool(agent=itinerary_agent),
    ],
)
