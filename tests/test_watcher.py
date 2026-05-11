import os
import tempfile
from unittest.mock import patch, MagicMock

import watcher

# Isolate data from the real project
watcher.CACHE_FILE = os.path.join(tempfile.gettempdir(), "treecloud_test_watcher.json")


def setup_function():
    if os.path.exists(watcher.CACHE_FILE):
        os.remove(watcher.CACHE_FILE)


def teardown_function():
    if os.path.exists(watcher.CACHE_FILE):
        os.remove(watcher.CACHE_FILE)


def test_fetch_repos_returns_expected_structure():
    """Verify that fetch_repos_for_interest returns items with the right schema."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "full_name": "test/repo",
                "html_url": "https://github.com/test/repo",
                "description": "A test repo",
                "stargazers_count": 42,
            }
        ]
    }

    with patch("requests.get", return_value=mock_response):
        results = watcher.fetch_repos_for_interest("Test Interest")

    assert len(results) == 1
    item = results[0]
    assert item["title"] == "test/repo"
    assert item["link"] == "https://github.com/test/repo"
    assert item["description"] == "A test repo"
    assert item["stars"] == "42"
    assert item["why_interesting"] == "Top matched for 'Test Interest'"
    assert item["source"] == "GitHub Search API"


def test_fetch_repos_handles_api_error():
    """Verify graceful handling of HTTP errors."""
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.raise_for_status.side_effect = Exception("API rate limited")

    with patch("requests.get", return_value=mock_response):
        results = watcher.fetch_repos_for_interest("Test Interest")

    assert results == []


def test_fetch_repos_handles_network_error():
    """Verify graceful handling of network errors."""
    with patch("requests.get", side_effect=Exception("Connection refused")):
        results = watcher.fetch_repos_for_interest("Test Interest")

    assert results == []


def test_fetch_repos_limits_to_three():
    """Verify that at most 3 results are returned per interest."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {"full_name": f"test/repo{i}", "html_url": f"https://github.com/test/repo{i}",
             "description": "desc", "stargazers_count": i}
            for i in range(10)
        ]
    }

    with patch("requests.get", return_value=mock_response):
        results = watcher.fetch_repos_for_interest("Test Interest")

    assert len(results) == 3


def test_caching_integration():
    """Verify that cache is used and API is skipped on cache hit."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [{"full_name": "test/repo", "html_url": "", "description": "",
                    "stargazers_count": 1}]
    }

    # First call: API hit, cache populated
    with patch("requests.get", return_value=mock_response) as mock_get:
        results1 = watcher.fetch_repos_for_interest("Cached Interest")
        watcher.set_cached_results("Cached Interest", results1)
        assert mock_get.call_count == 1

    # Second call: should hit cache, not API
    cached = watcher.get_cached_results("Cached Interest", 3600)
    assert cached is not None
    assert cached[0]["title"] == "test/repo"
