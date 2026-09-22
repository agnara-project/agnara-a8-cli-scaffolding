import subprocess
import sys


def main():
    print("Running Smoke Validation for Agnara CLI 0.1.0a8...")
    result = subprocess.run(
        ["agnara", "--version"], capture_output=True, text=True, check=False
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    print(f"Verified version: {result.stdout.strip()}")
    print("Smoke check passed successfully.")


if __name__ == "__main__":
    main()
