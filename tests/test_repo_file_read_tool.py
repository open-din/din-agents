import din_agents.shared.repo_profiles as repo_profiles
from din_agents.tools.repo_file_read_tool import make_repo_file_read_tool


def test_repo_file_read_returns_content(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        (tmp_path / "README.md").write_text("# Hello\nWorld")
        tool = make_repo_file_read_tool("din_core")
        result = tool._run(relative_path="README.md")
        assert "# Hello" in result
        assert "World" in result
    finally:
        repo_profiles.get_repo_profiles.cache_clear()


def test_repo_file_read_lists_directory(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        (tmp_path / "src").mkdir()
        (tmp_path / "src" / "lib.rs").write_text("fn main() {}")
        (tmp_path / "Cargo.toml").write_text("[package]")
        tool = make_repo_file_read_tool("din_core")
        result = tool._run(relative_path=".")
        assert "src" in result
        assert "Cargo.toml" in result
    finally:
        repo_profiles.get_repo_profiles.cache_clear()


def test_repo_file_read_not_found(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        tool = make_repo_file_read_tool("din_core")
        result = tool._run(relative_path="nonexistent.txt")
        assert "Not found" in result
    finally:
        repo_profiles.get_repo_profiles.cache_clear()


def test_repo_file_read_truncates_long_utf8(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    monkeypatch.setenv("DIN_AGENTS_MAX_REPO_READ_TOOL_CHARS", "100")
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        (tmp_path / "big.txt").write_text("x" * 500)
        tool = make_repo_file_read_tool("din_core")
        result = tool._run(relative_path="big.txt")
        assert result.count("x") == 100
        assert "[truncated:" in result
        assert "500 UTF-8 chars" in result
    finally:
        repo_profiles.get_repo_profiles.cache_clear()


def test_repo_file_read_rejects_traversal(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("DIN_CORE_PATH", str(tmp_path))
    repo_profiles.get_repo_profiles.cache_clear()
    try:
        tool = make_repo_file_read_tool("din_core")
        result = tool._run(relative_path="../escape.txt")
        assert "Invalid" in result
    finally:
        repo_profiles.get_repo_profiles.cache_clear()
