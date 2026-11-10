"""Tests for mbta/routes.py."""

from typing import Any

from mbta.routes import get_route_names

FAKE_API_DATA = [
    {"id": "Red", "attributes": {"long_name": "Red Line", "type": 1}},
    {"id": "Blue", "attributes": {"long_name": "Blue Line", "type": 1}},
    {"id": "Green-B", "attributes": {"long_name": "Green Line B", "type": 0}},
]


def test_get_route_names() -> None:
    """Returns the long name of each route in order."""
    assert get_route_names(FAKE_API_DATA) == ["Red Line", "Blue Line", "Green Line B"]


def test_get_route_names_empty() -> None:
    """Returns an empty list when there are no routes."""
    assert get_route_names([]) == []