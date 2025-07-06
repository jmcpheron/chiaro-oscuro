"""
Very basic tests for chiaro-oscuro.
"""

from pathlib import Path


def test_basic_math():
    """Test that 1 equals 1."""
    assert 1 == 1


def test_assets_directory_exists():
    """Test that assets directory exists."""
    assets_dir = Path("assets")
    assert assets_dir.exists()


def test_logo_file_exists():
    """Test that the base logo file exists."""
    logo_path = Path("assets/logo.png")
    assert logo_path.exists()


def test_action_yml_exists():
    """Test that action.yml exists."""
    action_file = Path("action.yml")
    assert action_file.exists()


def test_pyproject_toml_exists():
    """Test that pyproject.toml exists."""
    pyproject_file = Path("pyproject.toml")
    assert pyproject_file.exists()


def test_src_directory_exists():
    """Test that src directory exists."""
    src_dir = Path("src")
    assert src_dir.exists()


def test_process_logos_module_exists():
    """Test that the main module exists."""
    main_module = Path("src/process_logos_llm.py")
    assert main_module.exists()


def test_utils_module_exists():
    """Test that utils module exists."""
    utils_module = Path("src/utils.py")
    assert utils_module.exists()


def test_readme_exists():
    """Test that README.md exists."""
    readme_file = Path("README.md")
    assert readme_file.exists()
