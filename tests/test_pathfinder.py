"""Tests for mbta/pathfinder.py."""

import pytest 

from mbta.pathfinder import build_route_graph, find_route_path

FAKE_STOPS_BY_ROUTE: dict[str, list[str]] = {
    "Red Line": ["Davis", "Kendall/MIT", "Park Street", "Ashmont"],
    "Green Line B": ["Park Street", "Arlington", "Boston College"],
    "Blue Line": ["Wonderland", "Bowdoin"],
}


def test_build_route_graph() -> None:
    """Connects routes that share a stop and leaves others unconnected."""
    assert build_route_graph(FAKE_STOPS_BY_ROUTE) == {
        "Red Line": {"Green Line B"},
        "Green Line B": {"Red Line"},
        "Blue Line": set(),
    }


def test_same_route() -> None:
    """Returns one route when both stops are on it."""
    assert find_route_path(FAKE_STOPS_BY_ROUTE, "Davis", "Kendall/MIT") == ["Red Line"]


def test_one_transfer() -> None:
    """Returns both routes when a transfer is needed."""
    assert find_route_path(FAKE_STOPS_BY_ROUTE, "Ashmont", "Arlington") == [
        "Red Line",
        "Green Line B",
    ]


def test_no_path() -> None:
    """Returns None when the routes don't connect."""
    assert find_route_path(FAKE_STOPS_BY_ROUTE, "Davis", "Wonderland") is None


def test_unknown_stop() -> None:
    """Raises ValueError when a stop doesn't exist."""
    with pytest.raises(ValueError):
        find_route_path(FAKE_STOPS_BY_ROUTE, "Davis", "Bridgeport")
