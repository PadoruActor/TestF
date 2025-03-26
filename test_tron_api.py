# test_tron_api.py
import requests
import json


def test_tron_api():
    FASTAPI_URL = "http://localhost:8000/address-info/"
    TRON_ADDRESS = "TZ4UXDV5ZhNW7fb2AMSbgfAEZ7hWsnYS2g"

    try:
        # 1. Тест прямого запроса к Tron API
        print("1. Тестируем прямое подключение к Tron API...")
        tron_response = requests.post(
            "https://api.shasta.trongrid.io/wallet/getaccount",
            headers={'Content-Type': 'application/json'},
            json={"address": TRON_ADDRESS, "visible": True},
            timeout=5
        )
        print(f"Status: {tron_response.status_code}")
        print("Ответ Tron API (первые 200 символов):")
        print(json.dumps(tron_response.json())[:200] + "...")

        # 2. Тест вашего FastAPI сервиса
        print("\n2. Тестируем ваш FastAPI сервис...")
        your_response = requests.post(
            FASTAPI_URL,
            headers={'Content-Type': 'application/json'},
            json={"address": TRON_ADDRESS, "visible": True},
            timeout=5
        )

        if your_response.status_code == 200:
            print("Успешный ответ от вашего сервиса:")
            print(json.dumps(your_response.json(), indent=2))
        else:
            print(f"Ошибка {your_response.status_code}:")
            print(your_response.text)

    except Exception as e:
        print(f"Ошибка при выполнении теста: {str(e)}")


if __name__ == "__main__":
    test_tron_api()