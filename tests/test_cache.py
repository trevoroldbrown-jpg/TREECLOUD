import json
import os
import tempfile
from datetime import datetime, timedelta

# Patch cache file path before importing watcher
import watcher
watcher.CACHE_FILE = os.path.join(tempfile.gettempdir(), "treecloud_test_cache.json")


def setup_function():
    """Clean up any leftover test cache before each test."""
    if os.path.exists(watcher.CACHE_FILE):
        os.remove(watcher.CACHE_FILE)


def teardown_function():
    """Clean up test cache after each test."""
    if os.path.exists(watcher.CACHE_FILE):
        os.remove(watcher.CACHE_FILE)


def test_load_cache_returns_empty_when_no_file():
    assert watcher.load_cache() == {}


def test_load_cache_returns_empty_on_corrupted_file():
    with open(watcher.CACHE_FILE, "w") as f:
        f.write("not json")
    assert watcher.load_cache() == {}


def test_save_and_load_cache():
    cache = {"AI Agents": {"results": [], "cached_at": datetime.now().isoformat()}}
    watcher.save_cache(cache)
    loaded = watcher.load_cache()
    assert "AI Agents" in loaded
    assert loaded["AI Agents"]["results"] == []


def test_get_cached_results_returns_none_for_missing_interest():
    watcher.save_cache({"Other": {"results": [], "cached_at": datetime.now().isoformat()}})
    assert watcher.get_cached_results("AI Agents", 3600) is None


def test_get_cached_results_returns_results_when_fresh():
    results = [{"title": "test/repo", "stars": "100"}]
    watcher.set_cached_results("AI Agents", results)
    cached = watcher.get_cached_results("AI Agents", 3600)
    assert cached == results


def test_get_cached_results_returns_none_when_expired():
    results = [{"title": "test/repo", "stars": "100"}]
    watcher.set_cached_results("AI Agents", results)

    # Manually tweak the cached_at backward past TTL
    cache = watcher.load_cache()
    old_time = (datetime.now() - timedelta(hours=2)).isoformat()
    cache["AI Agents"]["cached_at"] = old_time
    watcher.save_cache(cache)

    assert watcher.get_cached_results("AI Agents", 3600) is None


def test_set_cached_results_overwrites_existing():
    watcher.set_cached_results("AI Agents", [{"title": "first"}])
    watcher.set_cached_results("AI Agents", [{"title": "second"}])
    cached = watcher.get_cached_results("AI Agents", 3600)
    assert cached == [{"title": "second"}]


def test_cache_ttl_respected():
    results = [{"title": "test/repo", "stars": "100"}]
    watcher.set_cached_results("AI Agents", results)
    # Very short TTL that has already passed
    still_fresh = watcher.get_cached_results("AI Agents", ttl_seconds=0)
    # Note: 0-second TTL means age >= 0 -> expired
    assert still_fresh is None, "0-second TTL should expire immediately"
