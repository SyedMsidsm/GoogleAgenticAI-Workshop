"""Mocked flight search and seat selection tools."""

from datetime import datetime, timedelta
import random


MOCK_AIRLINES = ["AirGDG", "CloudJet", "GeminiAir", "VertexWings"]

MOCK_SEATS = {
    "economy": ["12A", "12B", "14C", "15D", "20F"],
    "business": ["2A", "2B", "3C"],
}


def search_flights(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: str = "",
) -> dict:
    """Search for available flights between two cities.

    Args:
        origin: Departure city or airport code.
        destination: Arrival city or airport code.
        departure_date: Date of departure (YYYY-MM-DD).
        return_date: Date of return (YYYY-MM-DD), optional for one-way.

    Returns:
        A list of available flights with prices.
    """
    random.seed(f"{origin}{destination}{departure_date}")
    flights = []
    for i, airline in enumerate(MOCK_AIRLINES[:3]):
        dep_hour = 6 + i * 3
        arr_hour = dep_hour + 10 + random.randint(0, 3)
        price = 350 + random.randint(0, 500)
        flights.append({
            "flight_id": f"{airline[:2].upper()}{100 + i}",
            "airline": airline,
            "origin": origin,
            "destination": destination,
            "departure": f"{departure_date} {dep_hour:02d}:00",
            "arrival": f"{departure_date} {arr_hour:02d}:30",
            "price_usd": price,
            "class": "economy",
        })
    return {"status": "success", "flights": flights}


def select_seat(flight_id: str, seat_class: str = "economy") -> dict:
    """Show available seats for a selected flight.

    Args:
        flight_id: The ID of the selected flight.
        seat_class: 'economy' or 'business'.

    Returns:
        Available seat numbers for the chosen class.
    """
    seats = MOCK_SEATS.get(seat_class, MOCK_SEATS["economy"])
    return {
        "status": "success",
        "flight_id": flight_id,
        "seat_class": seat_class,
        "available_seats": seats,
    }
