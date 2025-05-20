from values import *
import requests

def get_api_key():

    endpoint = "https://petfriends.skillfactory.ru/api/key"
    headers = {
        "email": VALID_EMAIL,
        "password": VALID_PASS
    }

    response = requests.get(endpoint, headers=headers)
    json_response = response.json()
    return str(json_response["key"])