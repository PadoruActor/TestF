"""
Integration tests for Tron Address Info API.

Tests both direct Tron API access and FastAPI service endpoints.
"""

import requests
import json


def test_tron_api():
    """
    Run integration tests for the Tron Address Info API.

    Tests both direct Tron API access and the FastAPI service endpoints.
    """
    FASTAPI_URL = "http://localhost:8000/address-info/"
    TRON_ADDRESS = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"  # Testnet address

    try:
        # 1. Test direct Tron API connection
        print("1. Testing direct connection to Tron API...")
        tron_response = requests.post(
            "https://api.shasta.trongrid.io/wallet/getaccount",
            headers={'Content-Type': 'application/json'},
            json={"address": TRON_ADDRESS, "visible": True},
            timeout=5
        )
        print(f"Status: {tron_response.status_code}")
        print("Tron API response (first 200 chars):")
        print(json.dumps(tron_response.json())[:200] + "...")

        # 2. Test FastAPI service
        print("\n2. Testing FastAPI service...")
        your_response = requests.post(
            FASTAPI_URL,
            headers={'Content-Type': 'application/json'},
            json={"address": TRON_ADDRESS, "visible": True},
            timeout=5
        )

        if your_response.status_code == 200:
            print("Service response:")
            print(json.dumps(your_response.json(), indent=2))
        else:
            print(f"Error {your_response.status_code}:")
            print(your_response.text)

    except Exception as e:
        print(f"Test failed: {str(e)}")


if __name__ == "__main__":
    test_tron_api()