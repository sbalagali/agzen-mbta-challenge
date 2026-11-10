"""Find a list of subway routes to travel between two stops."""

from collections import deque


def build_route_graph(
    stops_by_route: dict[str, list[str]]
) -> dict[str, set[str]]:
    """Builds a graph where two routes are connected if they share a stop.
    
    Args:
        stops_by_route: Maps each route name to its list of stop names.

    Returns:
        Maps each route name to the set of routes it connects to.
    """
    graph = {route: set() for route in stops_by_route}
    for route_a, stops_a in stops_by_route.items():
        for route_b, stops_b in stops_by_route.items():
            if route_a != route_b and set(stops_a) & set(stops_b):
                graph[route_a].add(route_b)
    return graph


def find_route_path(
    stops_by_route: dict[str, list[str]],
    start_stop: str,
    end_stop: str,
) -> list[str] | None:
    """Finds routes from one stop to another with the fewest transfers.
    
    Args: 
        stops_by_route: Maps each route name to its list of stop names.
        start_stop: The name of the stop to start at, like "Northeastern University".
        end_stop: The name of the stop to end at, like "Park Street".

    Returns:
        The route name to ride in order, like ["Green Line E", "Red Line"].
        Returns None if no path exists.
    
    Raises:
        ValueError: If either stop isn't on any subway route. 
    """
    start_routes = [r for r, stops in stops_by_route.items() if start_stop in stops]
    end_routes = [r for r, stops in stops_by_route.items() if end_stop in stops]

    if not start_routes:
        raise ValueError(f"Unknown stop: {start_stop}")
    if not end_routes:
        raise ValueError(f"Unknown stop: {end_stop}")

    graph = build_route_graph(stops_by_route)
    queue = deque([[route] for route in start_routes])
    visited = set(start_routes)

    while queue:
        path = queue.popleft()
        current = path[-1]
        if current in end_routes:
            return path
        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None
