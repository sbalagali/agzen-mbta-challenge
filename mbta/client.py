"""Client for making requests to the MBTA API."""

import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://api-v3.mbta.com"
SUBWAY_ROUTE_TYPES = "0,1" # 0 = light rail, 1 = heavy rail


class MBTAClient:
    """Sends requests to the MBTA API using a shared session."""
    
    def __init__(self, api_key: str | None=None) -> None:
        """Sets up session and attaches API key if one is available.
        
        Args: 
            api_key: MBTA API key. If one is not given, key is read from 
            MBTA_API_KEY environment variable. If none are given, requests
            are rate limited.
        """
        self.session = requests.Session()
        api_key = api_key or os.getenv("MBTA_API_KEY")
        if api_key:
            self.session.headers["x-api-key"] = api_key


    def _get(
        self,
        path: str,
        params: dict[str, str] | None=None,
    )-> list[dict[str, Any]]:
        """Sends a GET request to the API and returns the data.
        
        Args:
            path: The endpoint path, like "/routes".
            params: Query parameters to add to the URL.
        
        Returns: 
            The list of resources under the "data" key of the response.

        Raises: 
            requests.HTTPError: If the API returns an error status.
        """
        response = self.session.get(f"{BASE_URL}{path}", params=params, timeout = 10)
        response.raise_for_status()
        return response.json()["data"]


    def get_subway_routes(self) -> list[dict[str, Any]]:
        """Gets all subway routes (Light Rail and Heavy Rail)."""
        return self._get("/routes", params={"filter[type]": SUBWAY_ROUTE_TYPES})


    def get_stops_for_route(self, route_id: str) -> list[dict[str, Any]]:
        """Gets all stops on a route."""
        return self._get("/stops", params={"filter[route]": route_id})
