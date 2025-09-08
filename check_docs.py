import subprocess
import time
import requests
import sys


def start_server():
    print("Starting FastAPI server...")
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app.main:app", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    time.sleep(3)
    return process


def check_docs():
    try:
        response = requests.get("http://localhost:8000/docs")
        if response.status_code == 200:
            print("✓ Swagger UI documentation available at http://localhost:8000/docs")
        else:
            print(f"✗ Swagger UI failed with status {response.status_code}")
            return False

        response = requests.get("http://localhost:8000/redoc")
        if response.status_code == 200:
            print("✓ ReDoc documentation available at http://localhost:8000/redoc")
        else:
            print(f"✗ ReDoc failed with status {response.status_code}")
            return False

        response = requests.get("http://localhost:8000/openapi.json")
        if response.status_code == 200:
            openapi_spec = response.json()
            print(
                f"✓ OpenAPI spec generated with {len(openapi_spec.get('paths', {}))} endpoints"
            )
        else:
            print(f"✗ OpenAPI spec failed with status {response.status_code}")
            return False

        return True

    except requests.exceptions.ConnectionError:
        print("✗ Could not connect to server")
        return False


def main():
    print("Checking API Documentation...")
    print("=" * 40)

    process = start_server()

    try:
        success = check_docs()
        if success:
            print("\n✓ All documentation endpoints working!")
            print(
                "Visit http://localhost:8000/docs to view the interactive API documentation"
            )
        else:
            print("\n✗ Documentation check failed!")
            return False
    finally:
        process.terminate()
        process.wait()

    return success


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
