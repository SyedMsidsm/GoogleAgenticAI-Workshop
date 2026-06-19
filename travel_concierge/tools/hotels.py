"""Mocked hotel search and room selection tools."""

import random

MOCK_HOTELS = [
    {"name": "The Grand Palace", "stars": 5, "base_price": 280},
    {"name": "Sunset Boutique", "stars": 4, "base_price": 160},
    {"name": "City Comfort Inn", "stars": 3, "base_price": 90},
]

MOCK_ROOMS = {
    5: ["Deluxe King", "Junior Suite", "Presidential Suite"],
    4: ["Standard Queen", "Superior Double", "Executive Room"],
    3: ["Standard Room", "Twin Room"],
}


def search_hotels(destination: str, check_in: str, check_out: str) -> dict:
    """Search for available hotels at a destination.

    Args:
        destination: The city or area to search in.
        check_in: Check-in date (YYYY-MM-DD).
        check_out: Check-out date (YYYY-MM-DD).

    Returns:
        A list of available hotels with pricing.
    """
    random.seed(f"{destination}{check_in}")
    hotels = []
    for h in MOCK_HOTELS:
        price = h["base_price"] + random.randint(-20, 40)
        hotels.append({
            "hotel_id": h["name"].replace(" ", "_").lower(),
            "name": h["name"],
            "stars": h["stars"],
            "location": destination,
            "check_in": check_in,
            "check_out": check_out,
            "price_per_night_usd": price,
        })
    return {"status": "success", "hotels": hotels}


def select_room(hotel_id: str, hotel_stars: int = 4) -> dict:
    """Show available room types for a selected hotel.

    Args:
        hotel_id: The ID of the selected hotel.
        hotel_stars: Star rating of the hotel (used to look up room types).

    Returns:
        Available room types.
    """
    rooms = MOCK_ROOMS.get(hotel_stars, MOCK_ROOMS[4])
    return {
        "status": "success",
        "hotel_id": hotel_id,
        "available_rooms": rooms,
    }
