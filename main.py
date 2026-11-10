"""Runs the MBTA subway challenge."""

from mbta.client import MBTAClient
from mbta.routes import (
    get_connecting_stops,
    get_route_names,
    get_route_with_fewest_stops,
    get_route_with_most_stops,
    get_stop_names,
)


def main():
    client = MBTAClient()
    raw_routes = client.get_subway_routes()

    # Q1
    print("Subway routes: ")
    print(", ".join(get_route_names(raw_routes)))

    # build a map of route name to its stop names
    stops_by_route = {}
    for route in raw_routes:
        name = route["attributes"]["long_name"]
        stops_by_route[name] = get_stop_names(client.get_stops_for_route(route["id"]))

    # Q2
    most_route, most_count = get_route_with_most_stops(stops_by_route)
    fewest_route, fewest_count = get_route_with_fewest_stops(stops_by_route)

    print(f"\nMost stops: {most_route} ({most_count} stops)")
    print(f"Fewest stops: {fewest_route} ({fewest_count} stops)")

    print("\nConnecting stops:")
    for stop, routes in get_connecting_stops(stops_by_route).items():
        print(f"{stop}: {', '.join(routes)}")



if __name__ == "__main__":
    main()