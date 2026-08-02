import requests
from config import PHONE_API_KEY


def get_phone_details(phone_number):
    url = "https://phoneintelligence.abstractapi.com/v1/"

    params = {
        "api_key": PHONE_API_KEY,
        "phone": phone_number
    }

    response = requests.get(url, params=params)

    print("STATUS CODE:", response.status_code)
    print("RESPONSE:")
    print(response.text)

    return response.json()
