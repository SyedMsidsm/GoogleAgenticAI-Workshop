"""In-trip agent — helps users during an active trip."""

from google.adk.agents import Agent

from ._bootstrap import MODEL, memorize, recall


def check_flight_status(flight_id: str) -> dict:
    """Check the current status of a flight.

    Args:
        flight_id: The flight ID to check (e.g. 'AI100').

    Returns:
        The current flight status.
    """
    # Mocked: in production this would call a real flight status API
    statuses = ["On time", "On time", "On time", "Delayed by 20 mins", "On time"]
    import hashlib
    idx = int(hashlib.md5(flight_id.encode()).hexdigest(), 16) % len(statuses)
    return {"flight_id": flight_id, "status": statuses[idx]}


def get_local_tips(location: str, query: str) -> dict:
    """Get local tips and recommendations for a location.

    Args:
        location: The current city or area the traveler is in.
        query: What the traveler needs help with (e.g. 'best local restaurants near beach').

    Returns:
        Practical local tips.
    """
    # Delegates to google_search in the parent via instruction — this is a thin wrapper
    return {
        "location": location,
        "query": query,
        "tip": f"Search result placeholder for '{query}' in {location}. Use google_search for real results.",
    }


in_trip_agent = Agent(
    model=MODEL,
    name="in_trip_agent",
    description=(
        "Assists users who are currently on their trip. "
        "Use this agent for flight status, local tips, restaurant suggestions, "
        "things to do today, or any in-the-moment travel questions."
    ),
    instruction="""
    You are a real-time travel companion for someone who is currently on their trip.

    You can help with:
    - Checking flight status (use check_flight_status)
    - Finding restaurants, attractions, or local tips (use get_local_tips)
    - Recalling their itinerary or trip details (use recall with key="itinerary")
    - Saving new preferences or notes they want to remember (use memorize)

    Always be brief, practical, and actionable. The user is on the go.
    Start by recalling their itinerary to understand their trip context.
    """,
    tools=[check_flight_status, get_local_tips, memorize, recall],
)

root_agent = in_trip_agent
