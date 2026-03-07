from pathlib import Path


def test_no_nested_mirror_tree_leftover():
    nested = Path("Experts/VirtualPanel/right/Experts/VirtualPanel/right")
    assert not nested.exists(), "Nested mirror tree should not exist"
