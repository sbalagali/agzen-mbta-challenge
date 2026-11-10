"""Runs the MBTA subway challenge."""

from mbta.client import MBTAClient
from mbta.routes import get_route_names

def main():
    client = MBTAClient()
    names = get_route_names(client.get_subway_routes())

    print("Subway routes: ")
    print(", ".join(names))


if __name__ == "__main__":
    main()