"""
Вспомогательные функции для работы с API.
"""

import requests
from config import BASE_URL, KEY_ENDPOINT, PETS_ENDPOINT, VALID_EMAIL, VALID_PASS


def get_api_key(email=VALID_EMAIL, password=VALID_PASS):
    """
    Получает ключ авторизации по email и паролю.

    Аргументы:
        email: email пользователя
        password: пароль пользователя

    Возвращает:
        строку с ключом авторизации или None в случае ошибки
    """
    url = BASE_URL + KEY_ENDPOINT
    headers = {
        "email": email,
        "password": password
    }

    try:
        response = requests.get(url, headers=headers)

        # Проверяем, успешно ли выполнен запрос
        if response.status_code != 200:
            print(f"Ошибка при получении ключа: статус {response.status_code}")
            return None

        # Пробуем преобразовать ответ в JSON
        response_json = response.json()

        # Проверяем, есть ли ключ в ответе
        if "key" not in response_json:
            print("Ошибка: в ответе нет поля 'key'")
            return None

        return response_json["key"]

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения: {e}")
        return None
    except ValueError as e:
        print(f"Ошибка при разборе JSON: {e}")
        return None


def get_my_pets_ids(auth_key):
    """
    Получает список ID всех питомцев пользователя.

    Аргументы:
        auth_key: ключ авторизации

    Возвращает:
        список ID питомцев
    """
    url = BASE_URL + PETS_ENDPOINT
    headers = {"auth_key": auth_key}
    params = {"filter": "my_pets"}

    try:
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Ошибка при получении списка питомцев: статус {response.status_code}")
            return []

        response_json = response.json()

        if "pets" not in response_json:
            return []

        # Извлекаем ID каждого питомца
        pet_ids = []
        for pet in response_json["pets"]:
            if "id" in pet:
                pet_ids.append(pet["id"])

        return pet_ids

    except Exception as e:
        print(f"Ошибка при получении списка питомцев: {e}")
        return []


def print_response_info(response, test_name=""):
    """
    Печатает информацию об ответе сервера для отладки.

    Аргументы:
        response: объект ответа requests
        test_name: название теста
    """
    print(f"\n--- Информация об ответе {test_name} ---")
    print(f"Статус код: {response.status_code}")

    try:
        # Пробуем получить JSON
        json_response = response.json()
        print("Тело ответа (JSON):")
        # Красиво выводим JSON
        for key, value in json_response.items():
            if isinstance(value, dict) or isinstance(value, list):
                print(f"  {key}: {str(value)[:100]}...")  # Обрезаем длинные списки
            else:
                print(f"  {key}: {value}")
    except:
        print(f"Тело ответа (текст): {response.text[:200]}")  # Первые 200 символов

    print("-" * 40)
