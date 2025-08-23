import requests, os
from dotenv import load_dotenv

load_dotenv()


def check_api_status():
    response = requests.get(
        url="https://api.nowpayments.io/v1/status"
    )
    if response.status_code == 200:
        return True
    return False


def get_estimated_price(amount: int, currency_from='ton', currency_to='usd'):
    """
    Из TON в доллары
    """
    x_api_key = os.getenv("api_private_key")
    response = requests.get(
        url=f"https://api.nowpayments.io/v1/estimate?amount={amount}&currency_from={currency_from}&currency_to={currency_to}",
        headers={
            "x-api-key": x_api_key
        }
    )
    if response.status_code == 200:
        return response.json()['estimated_amount']
    else:
        return False
