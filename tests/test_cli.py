import json
import subprocess
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


def run_agnara(*args, cwd=None):
    # agnara is in the current environment's PATH
    result = subprocess.run(["agnara", *args], capture_output=True, text=True, cwd=cwd, check=False)
    return result


def test_agnara_version():
    res = run_agnara("--version")
    assert res.returncode == 0, f"Failed: {res.stderr}"
    assert "0.1.0a8" in res.stdout


def test_agnara_help():
    res = run_agnara("--help")
    assert res.returncode == 0, f"Failed: {res.stderr}"
    assert "project" in res.stdout
    assert "app" in res.stdout


def test_project_create_dry_run(temp_dir):
    res = run_agnara("project", "create", "commerce", "--dry-run", cwd=temp_dir)
    assert res.returncode == 0, f"Failed: {res.stderr}"
    assert not (temp_dir / "commerce").exists(), "dry-run modified FS!"


def test_project_create_dry_run_json(temp_dir):
    res = run_agnara(
        "project", "create", "commerce", "--dry-run", "--json", cwd=temp_dir
    )
    assert res.returncode == 0, f"Failed: {res.stderr}"
    assert not (temp_dir / "commerce").exists(), "dry-run modified FS!"

    try:
        data = json.loads(res.stdout)
        assert isinstance(data, dict)
    except json.JSONDecodeError:
        pytest.fail("Output is not valid JSON")


def test_project_create_and_structure(temp_dir):
    res = run_agnara("project", "create", "commerce", cwd=temp_dir)
    assert res.returncode == 0, f"Failed: {res.stderr}"

    proj_dir = temp_dir / "commerce"
    assert proj_dir.exists()
    assert (proj_dir / "agnara.toml").exists()
    assert (proj_dir / "src").exists()
    assert (proj_dir / "tests").exists()
    assert (proj_dir / "pyproject.toml").exists()


def test_app_create(temp_dir):
    run_agnara("project", "create", "commerce", cwd=temp_dir)

    proj_dir = temp_dir / "commerce"

    apps_to_create = ["users", "catalog", "payments"]
    for app in apps_to_create:
        res = run_agnara("app", "create", app, cwd=proj_dir)
        assert res.returncode == 0, f"App creation failed for {app}: {res.stderr}"

        # Validate modular hexagonal structure
        app_dir = proj_dir / "src" / "commerce" / "apps" / app
        assert app_dir.exists(), f"App {app} not generated under src/<project>/apps/"
        assert (app_dir / "domain").exists()
        assert (app_dir / "application").exists()
        assert (app_dir / "adapters").exists()
        assert (app_dir / "adapters" / "inbound").exists()
        assert (app_dir / "adapters" / "outbound").exists()


def test_app_profiles(temp_dir):
    run_agnara("project", "create", "commerce", cwd=temp_dir)
    proj_dir = temp_dir / "commerce"

    profiles = ["app-api", "app-mcp", "app-agent", "app-worker"]
    for i, profile in enumerate(profiles):
        app_name = f"service_{i}"
        res = run_agnara(profile, app_name, cwd=proj_dir)
        assert res.returncode == 0, (
            f"App profile {profile} creation failed: {res.stderr}"
        )

        app_dir = proj_dir / "src" / "commerce" / "apps" / app_name
        assert app_dir.exists()
        assert (app_dir / "module.py").exists()


def test_invalid_name_rejection(temp_dir):
    res = run_agnara("project", "create", "invalid-name!", cwd=temp_dir)
    assert res.returncode != 0
    assert "invalid" in res.stderr.lower() or "error" in res.stderr.lower()


def test_file_exists_conflict(temp_dir):
    run_agnara("project", "create", "commerce", cwd=temp_dir)
    # Run again to see if it fails safe
    res = run_agnara("project", "create", "commerce", cwd=temp_dir)
    assert res.returncode != 0
    assert "exist" in res.stderr.lower() or "conflict" in res.stderr.lower()
