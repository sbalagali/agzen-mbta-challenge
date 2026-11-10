"""Functions for working with MBTA data."""

from typing import Any


def get_route_names(raw_routes: list[dict[str, Any]]) -> list[str]:
    """Gets the name of each route from the raw API data.
    
    Args:
        raw_routes: The route data returned by the MBTA API.

    Returns: The long name of each route, like "Red Line".
    """
    return[route["attributes"]["long_name"] for route in raw_routes]