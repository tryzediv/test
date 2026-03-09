"""
Тесты для получения ключа авторизации.
"""

import requests
from config import BASE_URL, KEY_ENDPOINT, VALID_EMAIL, VALID_PASS


def test_get_key_valid_credentials():
    """
    Позитивный тест: получение ключа с правильными email и паролем.

    Что проверяем:
    - Можно ли получить ключ с валидными данными
    """
    print("\n=== ТЕСТ: Получение ключа с правильными данными ===")

    url = BASE_URL + KEY_ENDPOINT
    headers = {
        "email": VALID_EMAIL,
        "password": VALID_PASS
    }

    response = requests.get(url, headers=headers)

    # Проверяем статус ответа
    if response.status_code == 200:
        try:
            response_json = response.json()
            if "key" in response_json:
                print("✅ Успех! Ключ получен")
                print(f"Ключ: {response_json['key'][:10]}...")  # Показываем начало ключа
                return True
            else:
                print("❌ Ошибка! В ответе нет поля 'key'")
                return False
        except:
            print("❌ Ошибка! Не удалось разобрать ответ")
            return False
    else:
        print(f"❌ Ошибка! Код ответа: {response.status_code}")
        return False


def test_get_key_invalid_email():
    """
    Негативный тест: получение ключа с неверным email.
    """
    print("\n=== ТЕСТ: Получение ключа с неверным email ===")

    url = BASE_URL + KEY_ENDPOINT
    headers = {
        "email": "wrong_email@example.com",  # Неправильный email
        "password": VALID_PASS
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("✅ Успех! Система не дала ключ с неверным email")
        print(f"Код ответа: {response.status_code}")
        return True
    else:
        print("❌ Ошибка! Ключ получен с неверным email")
        return False


def test_get_key_invalid_password():
    """
    Негативный тест: получение ключа с неверным паролем.
    """
    print("\n=== ТЕСТ: Получение ключа с неверным паролем ===")

    url = BASE_URL + KEY_ENDPOINT
    headers = {
        "email": VALID_EMAIL,
        "password": "wrong_password"  # Неправильный пароль
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("✅ Успех! Система не дала ключ с неверным паролем")
        print(f"Код ответа: {response.status_code}")
        return True
    else:
        print("❌ Ошибка! Ключ получен с неверным паролем")
        return False


def test_get_key_missing_email():
    """
    Негативный тест: получение ключа без email.
    """
    print("\n=== ТЕСТ: Получение ключа без email ===")

    url = BASE_URL + KEY_ENDPOINT
    headers = {
        "password": VALID_PASS
        # email отсутствует!
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("✅ Успех! Система не дала ключ без email")
        print(f"Код ответа: {response.status_code}")
        return True
    else:
        print("❌ Ошибка! Ключ получен без email")
        return False
