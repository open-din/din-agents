import pytest

from din_agents.shared.repo_paths import resolved_path_under_repo


def test_resolved_path_under_repo_ok(tmp_path) -> None:
    root = str(tmp_path)
    p = resolved_path_under_repo(root, "a/b/c.txt")
    assert p == tmp_path / "a" / "b" / "c.txt"


def test_resolved_path_rejects_parent_segments(tmp_path) -> None:
    with pytest.raises(ValueError, match="\\.\\."):
        resolved_path_under_repo(str(tmp_path), "../outside")
