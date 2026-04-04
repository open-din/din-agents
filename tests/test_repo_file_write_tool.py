import din_agents.shared.repo_profiles as repo_profiles
from din_agents.tools.repo_file_write_tool import make_repo_file_write_tool


def test_repo_file_write_creates_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    monkeypatch.setenv("DIN_AGENTS_REPO_WRITE", "1")
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        tool = make_repo_file_write_tool("din_core")
        msg = tool._run(relative_path="deep/x.txt", content="hello")
        assert "Wrote" in msg
        assert (tmp_path / "deep" / "x.txt").read_text() == "hello"
    finally:
        repo_profiles.get_repo_profiles.cache_clear()


def test_repo_file_write_disabled(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    monkeypatch.setenv("DIN_AGENTS_REPO_WRITE", "0")
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        tool = make_repo_file_write_tool("din_core")
        msg = tool._run(relative_path="y.txt", content="nope")
        assert "disabled" in msg.lower()
        assert not (tmp_path / "y.txt").is_file()
    finally:
        monkeypatch.setenv("DIN_AGENTS_REPO_WRITE", "1")
        repo_profiles.get_repo_profiles.cache_clear()


def test_repo_file_write_rejects_traversal(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        tool = make_repo_file_write_tool("din_core")
        msg = tool._run(relative_path="../escape.txt", content="x")
        assert "Invalid" in msg
    finally:
        repo_profiles.get_repo_profiles.cache_clear()
