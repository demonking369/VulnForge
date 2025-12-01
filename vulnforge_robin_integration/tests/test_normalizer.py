from ..normalizer import normalize_robin_output


def test_normalize_markdown():
    md = """
    ## Target
    - example.com
    Leak Type: credentials
    Source: forum
    First Seen: 2024-08-01
    Last Seen: 2024-08-05
    Raw Snippet:
    """
    items = normalize_robin_output(md)
    assert items
    item = items[0]
    assert item["target"].value == "example.com"
    assert item["leak_type"] == "credentials"
    assert item["source"] == "forum"
    assert item["first_seen"].isoformat().startswith("2024-08-01")
