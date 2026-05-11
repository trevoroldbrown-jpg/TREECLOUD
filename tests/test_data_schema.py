import json
import os

DATA_FILE = "data.json"
REQUIRED_ITEM_KEYS = {"title", "link", "description", "stars", "why_interesting", "source"}


def test_data_file_exists():
    assert os.path.exists(DATA_FILE), f"{DATA_FILE} not found — run watcher.py first"


def test_data_file_is_valid_json():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert isinstance(data, dict), "data.json root should be a dict"


def test_data_has_required_structure():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "last_updated" in data, "Missing 'last_updated' key"
    assert "items" in data, "Missing 'items' key"
    assert isinstance(data["items"], list), "'items' should be a list"


def test_last_updated_is_iso_format():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    from datetime import datetime
    assert datetime.fromisoformat(data["last_updated"]), "last_updated not ISO format"


def test_all_items_have_required_keys():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data["items"]):
        missing = REQUIRED_ITEM_KEYS - set(item.keys())
        assert not missing, f"Item {i} ({item.get('title', '?')}) missing keys: {missing}"


def test_all_items_have_non_empty_titles():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data["items"]):
        assert item.get("title"), f"Item {i} has empty title"


def test_star_format():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    for i, item in enumerate(data["items"]):
        stars = item.get("stars", "")
        assert isinstance(stars, str), f"Item {i} stars should be string, got {type(stars)}"
        assert stars.isdigit() or stars.replace(",", "").isdigit(), \
            f"Item {i} stars '{stars}' not a numeric string"


def test_items_have_no_duplicate_titles():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    titles = [item["title"] for item in data["items"]]
    duplicates = [t for t in titles if titles.count(t) > 1]
    assert not duplicates, f"Duplicate titles found: {set(duplicates)}"
