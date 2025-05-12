import requests
from values import *

url = "https://petfriends.skillfactory.ru/api/create_pet_simple"


def get_api_key():

    endpoint = "https://petfriends.skillfactory.ru/api/key"
    headers = {
        "email": VALID_EMAIL,
        "password": VALID_PASS
    }

    response = requests.get(endpoint, headers=headers)
    json_response = response.json()
    return str(json_response["key"])

# Тест1: успешное создание питомца
def test_create_pet_simple_valid_data():

    headers = {
        "auth_key": get_api_key()
    }

    data = {
        "name": "Барсик",
        "animal_type": "кот",
        "age": "3"
    }

    response = requests.post(url, headers=headers, data=data)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    try:
        json_response = response.json()
        assert json_response["name"] == data["name"], "Имя питомца не совпадает"
        assert json_response["animal_type"] == data["animal_type"], "Тип животного не совпадает"
        assert json_response["age"] == data["age"], "Возраст питомца не совпадает"
        assert "id" in json_response, "В ответе отсутствует ID питомца"
        print("\nПитомец успешно создан")
        print("ID питомца:", json_response["id"])
        return json_response["id"]
    except ValueError:
        raise Exception("Невозможно разобрать JSON. Ответ сервера:", response.text)


# Тест2: Неверный или отсутствующий auth_key
def test_create_pet_invalid_auth_key():

    headers = {
        "auth_key": "invalid_or_missing_key"
    }

    data = {
        "name": "Лютик",
        "animal_type": "собака",
        "age": "5"
    }

    response = requests.post(url, headers=headers, data=data)

    assert response.status_code != 200, "Создание питомца прошло с невалидным ключом — это неправильно"

    print("\nТест пройден: создание питомца с неверным auth_key завершено с кодом", response.status_code)

