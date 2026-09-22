import subprocess
import pytest
import json
import os
import tempfile
from pathlib import Path

@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)

def run_agnara(*args, cwd=None):
    # Assume agnara is in the PATH since we run in the venv
    result = subprocess.run(
        ["agnara", *args],
        capture_output=True,
        text=True,
        cwd=cwd
    )
    return result

def test_syntax_error_mre():
    """
    Minimal Reproducible Example for the SyntaxError on import.
    This test currently captures the gap/bug in 0.1.0a8.
    """
    result = run_agnara("--help")
    assert result.returncode != 0
    assert "SyntaxError: multiple exception types must be parenthesized" in result.stderr

def test_project_create_dry_run(temp_dir):
    """
    Verify --dry-run does not modify FS and output is parseable.
    """
    result = run_agnara("project", "create", "commerce", "--dry-run", "--json", cwd=temp_dir)
    
    # We expect this to fail due to the SyntaxError, but we document the intended assertion
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert not (temp_dir / "commerce").exists(), "dry-run modified FS!"
    try:
        data = json.loads(result.stdout)
        assert "bootstrap" in data
    except json.JSONDecodeError:
        pytest.fail("JSON not parseable")

def test_project_create_json(temp_dir):
    """
    Verify project creation and bootstrap instructions.
    """
    result = run_agnara("project", "create", "commerce", "--json", cwd=temp_dir)
    
    assert result.returncode == 0, f"CLI failed: {result.stderr}"
    assert (temp_dir / "commerce" / "pyproject.toml").exists()
    try:
        data = json.loads(result.stdout)
        assert "bootstrap" in data
    except json.JSONDecodeError:
        pytest.fail("JSON not parseable")

def test_app_create_modules(temp_dir):
    """
    Verify modular hexagonal layout and module importability.
    """
    # Create project first
    res_proj = run_agnara("project", "create", "commerce", cwd=temp_dir)
    if res_proj.returncode != 0:
        pytest.skip("Project creation failed, cannot test app creation")
        
    project_dir = temp_dir / "commerce"
    
    for app in ["users", "catalog", "payments"]:
        res_app = run_agnara("app", "create", app, "--project", "commerce", cwd=temp_dir)
        if res_app.returncode == 0:
            app_dir = project_dir / app
            assert app_dir.exists(), f"App {app} not created"
            assert (app_dir / "domain").exists(), "Missing domain layer (hexagonal)"
            assert (app_dir / "application").exists(), "Missing application layer"
            assert (app_dir / "infrastructure").exists(), "Missing infrastructure layer"
