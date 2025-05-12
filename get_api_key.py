import requests
from values import *

url = "https://petfriends.skillfactory.ru/api/key"


def test_get_api_key_valid_user():

    headers = {
        "email": VALID_EMAIL,
        "password": VALID_PASS
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    try:
        json_response = response.json()
        assert "key" in json_response, "В ответе отсутствует поле 'key'"
        print("\nПолучен API-ключ:", json_response["key"])
    except ValueError:
        raise Exception("\nНевозможно разобрать JSON. Ответ сервера:", response.text)

    print("Тест пройден: авторизация успешна и API-ключ получен")


def test_get_api_key_invalid_email():

    headers = {
        "email": "invalid_email@example.com",
        "password": VALID_PASS
    }

    response = requests.get(url, headers=headers)

    assert response.status_code != 200, "Доступ не должен быть предоставлен при неверном email"

    print("\nТест пройден: запрос с неверным email завершён с кодом", response.status_code)


def test_get_api_key_invalid_password():

    headers = {
        "email": VALID_EMAIL,
        "password": "wrong_password"
    }

    response = requests.get(url, headers=headers)

    assert response.status_code != 200, "Доступ не должен быть предоставлен при неверном пароле"

    print("\nТест пройден: запрос с неверным паролем завершён с кодом", response.status_code)


def test_get_api_key_missing_email():

    headers = {
        "password": VALID_PASS
    }

    response = requests.get(url, headers=headers)

    assert response.status_code != 200, "Сервер должен вернуть ошибку, если email не указан"

    print("\nТест пройден: запрос без email завершён с кодом", response.status_code)


def test_get_api_key_empty_credentials():

    headers = {
        "email": "",
        "password": ""
    }

    response = requests.get(url, headers=headers)

    assert response.status_code != 200, "Сервер должен вернуть ошибку при пустых email и password"

    print("\nТест пройден: запрос с пустыми данными завершён с кодом", response.status_code)
