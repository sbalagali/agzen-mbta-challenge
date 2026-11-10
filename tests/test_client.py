"""Tests for mbta/client.py."""

from mbta.client import MBTAClient


def test_api_key_is_added_to_headers() -> None:
    """Adds the x-api-key header when a key is given."""
    client = MBTAClient(api_key="test-key")
    assert client.session.headers["x-api-key"] == "test-key"
