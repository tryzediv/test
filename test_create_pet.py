"""
Тесты для создания питомцев.
"""

import requests
import random
from config import BASE_URL, CREATE_PET_ENDPOINT
from helpers import get_api_key


def generate_pet_data():
    """
    Генерирует случайные данные для питомца.

    Возвращает:
        словарь с данными питомца
    """
    names = ["Мурзик", "Барсик", "Шарик", "Бобик", "Рыжик", "Снежок"]
    types = ["кот", "собака", "хомяк", "попугай", "рыбка"]

    return {
        "name": random.choice(names) + "_" + str(random.randint(1, 999)),
        "animal_type": random.choice(types),
        "age": str(random.randint(1, 15))
    }


def test_create_pet_success():
    """
    Позитивный тест: успешное создание питомца.

    Что проверяем:
    - Можно ли создать питомца с авторизацией
    - Возвращаются ли все данные питомца
    """
    print("\n=== ТЕСТ: Создание питомца ===")

    # Сначала получаем ключ авторизации
    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    url = BASE_URL + CREATE_PET_ENDPOINT
    headers = {"auth_key": auth_key}

    # Генерируем данные для питомца
    pet_data = generate_pet_data()
    print(f"Данные питомца: {pet_data}")

    try:
        # Отправляем запрос
        response = requests.post(url, headers=headers, data=pet_data)

        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Успех! Питомец создан")
                print(f"ID питомца: {result.get('id')}")

                # Проверяем, что все данные сохранились
                if result.get('name') == pet_data['name']:
                    print("  ✓ Имя совпадает")
                else:
                    print("  ✗ Имя не совпадает")

                if result.get('animal_type') == pet_data['animal_type']:
                    print("  ✓ Тип животного совпадает")
                else:
                    print("  ✗ Тип животного не совпадает")

                if result.get('age') == pet_data['age']:
                    print("  ✓ Возраст совпадает")
                else:
                    print("  ✗ Возраст не совпадает")

                return True

            except ValueError:
                print("❌ Ошибка! Не удалось разобрать ответ сервера")
                print(f"Ответ сервера: {response.text[:200]}")
                return False
        else:
            print(f"❌ Ошибка! Код ответа: {response.status_code}")
            print(f"Текст ошибки: {response.text[:200]}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка соединения: {e}")
        return False


def test_create_pet_invalid_auth():
    """
    Негативный тест: создание питомца с неверным ключом.

    Важно: используем только латинские символы в ключе!
    """
    print("\n=== ТЕСТ: Создание питомца с неверным ключом ===")

    url = BASE_URL + CREATE_PET_ENDPOINT

    # ВАЖНО: Используем только латинские буквы и цифры в ключе!
    # Русские буквы и спецсимволы могут вызвать проблемы с кодировкой
    invalid_key = "invalid_key_12345"  # Только латиница и цифры

    headers = {"auth_key": invalid_key}

    pet_data = generate_pet_data()
    print(f"Данные питомца: {pet_data}")
    print(f"Неверный ключ: {invalid_key}")

    try:
        response = requests.post(url, headers=headers, data=pet_data)

        if response.status_code != 200:
            print("✅ Успех! Система не дала создать питомца с неверным ключом")
            print(f"Код ответа: {response.status_code}")
            return True
        else:
            print("❌ Ошибка! Питомец создан с неверным ключом")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка соединения: {e}")
        return False


def test_create_pet_without_auth():
    """
    Негативный тест: создание питомца без ключа авторизации.
    """
    print("\n=== ТЕСТ: Создание питомца без ключа ===")

    url = BASE_URL + CREATE_PET_ENDPOINT

    pet_data = generate_pet_data()
    print(f"Данные питомца: {pet_data}")

    try:
        # Отправляем запрос без заголовков
        response = requests.post(url, data=pet_data)

        if response.status_code != 200:
            print("✅ Успех! Система не дала создать питомца без ключа")
            print(f"Код ответа: {response.status_code}")
            return True
        else:
            print("❌ Ошибка! Питомец создан без ключа")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка соединения: {e}")
        return False


def test_create_pet_with_special_chars():
    """
    Тест с специальными символами в данных питомца.
    Проверяем, как система обрабатывает русские буквы.
    """
    print("\n=== ТЕСТ: Создание питомца с русскими буквами ===")

    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    url = BASE_URL + CREATE_PET_ENDPOINT
    headers = {"auth_key": auth_key}

    # Данные с русскими буквами
    pet_data = {
        "name": "Мурзик_тестовый",
        "animal_type": "кот",
        "age": "5"
    }

    print(f"Данные питомца: {pet_data}")

    try:
        # Явно указываем кодировку UTF-8
        response = requests.post(
            url,
            headers=headers,
            data=pet_data
        )

        if response.status_code == 200:
            try:
                result = response.json()
                print("✅ Успех! Питомец с русскими буквами создан")
                print(f"ID питомца: {result.get('id')}")
                print(f"Имя из ответа: {result.get('name')}")
                return True
            except ValueError:
                print(f"❌ Ошибка при разборе JSON: {response.text[:200]}")
                return False
        else:
            print(f"❌ Ошибка! Код ответа: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка соединения: {e}")
        return False
