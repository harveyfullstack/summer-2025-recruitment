import asyncio
import httpx
import sys


async def test_health_endpoint():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            print(f"Health check: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"Health check failed: {e}")
            return False


async def test_root_endpoint():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/")
            print(f"Root endpoint: {response.status_code}")
            print(f"Response: {response.json()}")
            return response.status_code == 200
        except Exception as e:
            print(f"Root endpoint failed: {e}")
            return False


async def main():
    print("Testing Resume Fraud Detection API...")

    health_ok = await test_health_endpoint()
    root_ok = await test_root_endpoint()

    if health_ok and root_ok:
        print("\n✅ Basic API tests passed!")
        print("API is ready for resume fraud detection.")
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
