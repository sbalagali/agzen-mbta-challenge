"""Tests for mbta/routes.py."""

from typing import Any

from mbta.routes import (
    get_route_names,
    get_connecting_stops,
    get_route_with_fewest_stops,
    get_route_with_most_stops,
    get_stop_names,
)

TEST_API_DATA = [
    {"id": "Red", "attributes": {"long_name": "Red Line", "type": 1}},
    {"id": "Blue", "attributes": {"long_name": "Blue Line", "type": 1}},
    {"id": "Green-B", "attributes": {"long_name": "Green Line B", "type": 0}},
]

TEST_STOPS_BY_ROUTE: dict[str, list[str]] = {
    "Red Line": ["Alewife", "Davis", "Park Street", "Downtown Crossing"],
    "Orange Line": ["Oak Grove", "Downtown Crossing"],
    "Green Line B": ["Boston College", "Park Street", "Government Center"],
}

def test_get_route_names() -> None:
    """Returns the long name of each route in order."""
    assert get_route_names(TEST_API_DATA) == ["Red Line", "Blue Line", "Green Line B"]


def test_get_route_names_empty() -> None:
    """Returns an empty list when there are no routes."""
    assert get_route_names([]) == []


def test_get_stop_names() -> None:
    """Returns the name of each stop in order."""
    raw_stops = [{"attributes": {"name": "Davis"}}, {"attributes": {"name": "Alewife"}}]
    assert get_stop_names(raw_stops) == ["Davis", "Alewife"]


def test_get_route_with_most_stops() -> None:
    """Returns the route with the most stops and its count."""
    assert get_route_with_most_stops(TEST_STOPS_BY_ROUTE) == ("Red Line", 4)


def test_get_route_with_fewest_stops() -> None:
    """Returns the route with the fewest stops and its count."""
    assert get_route_with_fewest_stops(TEST_STOPS_BY_ROUTE) == ("Orange Line", 2)


def test_get_connecting_stops() -> None:
    """Returns only stops on two or more routes."""
    assert get_connecting_stops(TEST_STOPS_BY_ROUTE) == {
        "Park Street": ["Red Line", "Green Line B"],
        "Downtown Crossing": ["Red Line", "Orange Line"],
    }
