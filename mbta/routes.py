"""Functions for working with MBTA data."""

from typing import Any


def get_route_names(raw_routes: list[dict[str, Any]]) -> list[str]:
    """Gets the name of each route from the raw API data."""
    return[route["attributes"]["long_name"] for route in raw_routes]