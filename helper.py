from values import *
import requests

# Возвращает ключ авторизации
def get_api_key():

    endpoint = "https://petfriends.skillfactory.ru/api/key"
    headers = {
        "email": VALID_EMAIL,
        "password": VALID_PASS
    }

    response = requests.get(endpoint, headers=headers)
    json_response = response.json()
    return str(json_response["key"])


# Возвращает ID последнего добавленного питомца
def get_my_pets_id():

    endpoint = "https://petfriends.skillfactory.ru/api/pets"
    headers = {
        "auth_key": get_api_key()
    }

    params = {
        "filter": "my_pets"
    }

    response = requests.get(endpoint, headers=headers, params=params)
    json_response = response.json()

    return json_response["pets"][1]["id"]
