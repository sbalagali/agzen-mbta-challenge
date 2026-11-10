"""Functions for working with MBTA data."""

from typing import Any


def get_route_names(raw_routes: list[dict[str, Any]]) -> list[str]:
    """Gets the name of each route from the raw API data."""
    return[route["attributes"]["long_name"] for route in raw_routes]


def get_stop_names(raw_stops: list[dict[str, Any]]) -> list[str]:
    """Gets the name of each stop from the raw API data."""
    return [stop["attributes"]["name"] for stop in raw_stops]


def get_route_with_most_stops(
    stops_by_route: dict[str, list[str]]
) -> tuple[str, int]:
    """Finds the route with the most stops."""
    best_route = ""
    best_count = -1
    for route, stops in stops_by_route.items():
        if len(stops) > best_count:
            best_route = route
            best_count = len(stops)
    return best_route, best_count


def get_route_with_fewest_stops(
    stops_by_route: dict[str, list[str]],
) -> tuple[str, int]:
    """Finds the route with the fewest stops."""
    best_route = ""
    best_count = float("inf")
    for route, stops in stops_by_route.items():
        if len(stops) < best_count:
            best_route = route
            best_count = len(stops)
    return best_route, int(best_count)


def get_connecting_stops(
    stops_by_route: dict[str, list[str]]
) -> dict[str, list[str]]:
    """Finds stops that are on two or more routes."""
    routes_by_stop = {}
    for route, stops in stops_by_route.items():
        for stop in stops:
            if stop not in routes_by_stop:
                routes_by_stop[stop] = []
            routes_by_stop[stop].append(route)

    connecting = {}
    for stop, routes in routes_by_stop.items():
        if len(routes) > 1:
            connecting[stop] = routes
    return connecting
