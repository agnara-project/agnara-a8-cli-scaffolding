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
    result = subprocess.run(
        ["agnara", *args], capture_output=True, text=True, cwd=cwd, check=False
    )
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
    res1 = run_agnara(
        "project", "create", "commerce", "--dry-run", "--json", cwd=temp_dir
    )
    res2 = run_agnara(
        "project", "create", "commerce", "--dry-run", "--json", cwd=temp_dir
    )
    assert res1.returncode == 0, f"Failed: {res1.stderr}"
    assert res2.returncode == 0, f"Failed: {res2.stderr}"

    # Determinism check
    assert res1.stdout == res2.stdout, "Dry-run JSON output is not deterministic"
    assert not (temp_dir / "commerce").exists(), "dry-run modified FS!"

    try:
        data = json.loads(res1.stdout)
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


import tomllib


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

    # Verify manifest
    manifest_path = proj_dir / "agnara.toml"
    with open(manifest_path, "rb") as f:
        manifest = tomllib.load(f)

    for app in apps_to_create:
        assert app in manifest.get("apps", {}), f"App {app} not declared in agnara.toml"
        assert manifest["apps"][app]["architecture"] == "modular-hexagonal"


def test_app_profiles(temp_dir):
    run_agnara("project", "create", "commerce", cwd=temp_dir)
    proj_dir = temp_dir / "commerce"

    profiles = {
        "app-api": {"exposures": ["http"], "files": ["http.py"]},
        "app-mcp": {"exposures": ["mcp"], "files": ["mcp.py"]},
        "app-agent": {"exposures": ["mcp", "a2a"], "files": ["mcp.py", "a2a.py"]},
        "app-worker": {
            "exposures": ["tasks", "events"],
            "files": ["tasks.py", "events.py"],
        },
    }

    for i, (profile, expected) in enumerate(profiles.items()):
        app_name = f"service_{i}"
        res = run_agnara(profile, app_name, cwd=proj_dir)
        assert res.returncode == 0, (
            f"App profile {profile} creation failed: {res.stderr}"
        )

        app_dir = proj_dir / "src" / "commerce" / "apps" / app_name
        assert app_dir.exists()
        assert (app_dir / "module.py").exists()

        # Verify specific inbound files
        inbound_dir = app_dir / "adapters" / "inbound"
        for f in expected["files"]:
            assert (inbound_dir / f).exists(), (
                f"Expected {f} not generated for {profile}"
            )

    # Verify manifest
    manifest_path = proj_dir / "agnara.toml"
    with open(manifest_path, "rb") as f:
        manifest = tomllib.load(f)

    for i, (profile, expected) in enumerate(profiles.items()):
        app_name = f"service_{i}"
        assert app_name in manifest["apps"]
        assert set(manifest["apps"][app_name]["exposures"]) == set(
            expected["exposures"]
        )


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


def test_overwrite_flag(temp_dir):
    run_agnara("project", "create", "commerce", cwd=temp_dir)
    # Use --overwrite, it should succeed
    res = run_agnara("project", "create", "commerce", "--overwrite", cwd=temp_dir)
    assert res.returncode == 0, f"--overwrite failed: {res.stderr}"
