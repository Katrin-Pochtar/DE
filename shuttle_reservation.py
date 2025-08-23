import argparse
import json
from datetime import datetime
from typing import List, Tuple

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://reservation.pc.gc.ca/create-booking/results"
RESERVE_URL = "https://reservation.pc.gc.ca/api/create-booking"


def _build_search_params(date: str, people: int) -> dict:
    """Build query parameters for the search request."""
    return {
        "mapId": -2147483634,
        "searchTabGroupId": 3,
        "bookingCategoryId": 9,
        "resourceLocationId": -2147483642,
        "startDate": date,
        "endDate": date,
        "nights": 1,
        "isReserving": "true",
        "peopleCapacityCategoryCounts": json.dumps([[-32767, None, people, None]]),
        "filterData": json.dumps({}),
        "searchTime": datetime.utcnow().isoformat(),
        "flexibleSearch": json.dumps([False, False, None, 1]),
    }


def check_availability(session: requests.Session, date: str, people: int) -> List[Tuple[str, str]]:
    """Return a list of available resource ids and names."""
    params = _build_search_params(date, people)
    response = session.get(BASE_URL, params=params)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for card in soup.select("[data-resource-id]"):
        text = card.get_text(" ", strip=True).lower()
        if "sold out" in text or "unavailable" in text:
            continue
        resource_id = card.get("data-resource-id")
        title = card.get_text(" ", strip=True)
        if resource_id:
            results.append((resource_id, title))
    return results


def reserve(session: requests.Session, resource_id: str, date: str, people: int) -> dict:
    """Attempt to reserve a spot for the given resource id."""
    payload = {
        "resourceLocationId": resource_id,
        "startDate": date,
        "nights": 1,
        "peopleCapacityCategoryCounts": [[-32767, None, people, None]],
    }
    response = session.post(RESERVE_URL, json=payload)
    response.raise_for_status()
    return response.json()


def main(date: str, people: int) -> None:
    with requests.Session() as session:
        options = check_availability(session, date, people)
        if not options:
            print("No availability for the selected date")
            return
        resource_id, title = options[0]
        try:
            confirmation = reserve(session, resource_id, date, people)
        except requests.HTTPError as exc:
            print(f"Reservation failed: {exc}")
            return
        print(f"Reserved {title}: {confirmation}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check shuttle availability and reserve")
    parser.add_argument("--date", required=True, help="Date in YYYY-MM-DD format")
    parser.add_argument("--people", type=int, default=2, help="Number of people")
    args = parser.parse_args()
    main(args.date, args.people)
