import subprocess
import sys
import tempfile
from pathlib import Path


def main():
    print("Running Smoke Validation for Agnara CLI 0.1.0a8...")

    with tempfile.TemporaryDirectory() as d:
        temp_dir = Path(d)

        # 1. Check version
        v_res = subprocess.run(
            ["agnara", "--version"], capture_output=True, text=True, check=False
        )
        if v_res.returncode != 0:
            print(f"Error checking version: {v_res.stderr}")
            sys.exit(1)
        print(f"Verified version: {v_res.stdout.strip()}")

        # 2. Project create
        p_res = subprocess.run(
            ["agnara", "project", "create", "demo_smoke"],
            cwd=temp_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if p_res.returncode != 0:
            print(f"Error creating project: {p_res.stderr}")
            sys.exit(1)

        proj_dir = temp_dir / "demo_smoke"
        if not (proj_dir / "agnara.toml").exists():
            print("Error: agnara.toml not found")
            sys.exit(1)

        # 3. App create
        a_res = subprocess.run(
            ["agnara", "app", "create", "inventory"],
            cwd=proj_dir,
            capture_output=True,
            text=True,
            check=False,
        )
        if a_res.returncode != 0:
            print(f"Error creating app: {a_res.stderr}")
            sys.exit(1)

        app_dir = proj_dir / "src" / "demo_smoke" / "apps" / "inventory"
        if not app_dir.exists() or not (app_dir / "domain").exists():
            print("Error: app 'inventory' or 'domain' layer not properly generated")
            sys.exit(1)

        print(
            "Smoke check passed successfully. Clean up automatic via TemporaryDirectory."
        )


if __name__ == "__main__":
    main()
