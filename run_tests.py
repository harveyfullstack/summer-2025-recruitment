import subprocess
import sys


def run_tests():
    print("Running Resume Fraud Detection System Tests...")
    print("=" * 50)

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            check=True,
            capture_output=True,
            text=True,
        )

        print(result.stdout)
        print("✓ All tests passed!")
        return True

    except subprocess.CalledProcessError as e:
        print(e.stdout if e.stdout else "No stdout")
        print(e.stderr if e.stderr else "No stderr")
        print("✗ Some tests failed!")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
