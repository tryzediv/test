"""
Тесты для удаления питомцев.
"""

import requests
import random
from config import BASE_URL, PETS_ENDPOINT, CREATE_PET_ENDPOINT
from helpers import get_api_key, get_my_pets_ids


def create_test_pet(auth_key):
    """
    Создает тестового питомца и возвращает его ID.

    Аргументы:
        auth_key: ключ авторизации

    Возвращает:
        ID созданного питомца или None
    """
    url = BASE_URL + CREATE_PET_ENDPOINT
    headers = {"auth_key": auth_key}

    # Данные для тестового питомца
    pet_data = {
        "name": f"Тестовый_{random.randint(1, 999)}",
        "animal_type": "тестовый",
        "age": "1"
    }

    response = requests.post(url, headers=headers, data=pet_data)

    if response.status_code == 200:
        try:
            result = response.json()
            return result.get('id')
        except:
            return None
    return None


def test_delete_existing_pet():
    """
    Позитивный тест: удаление существующего питомца.

    Что проверяем:
    - Можно ли удалить питомца
    - Пропадает ли он из списка после удаления
    """
    print("\n=== ТЕСТ: Удаление питомца ===")

    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    # Сначала создаем питомца для удаления
    pet_id = create_test_pet(auth_key)

    if not pet_id:
        print("❌ Ошибка! Не удалось создать тестового питомца")
        return False

    print(f"Создан тестовый питомец с ID: {pet_id}")

    # Удаляем питомца
    url = f"{BASE_URL}{PETS_ENDPOINT}/{pet_id}"
    headers = {"auth_key": auth_key}

    delete_response = requests.delete(url, headers=headers)

    if delete_response.status_code == 200:
        print("✅ Успех! Питомец удален")

        # Проверяем, что питомец действительно удален
        # Получаем список своих питомцев
        my_pets_ids = get_my_pets_ids(auth_key)

        if pet_id not in my_pets_ids:
            print("✓ Питомец отсутствует в списке - всё правильно")
            return True
        else:
            print("✗ Питомец всё еще в списке - ошибка!")
            return False
    else:
        print(f"❌ Ошибка при удалении! Код ответа: {delete_response.status_code}")
        return False


def test_delete_nonexistent_pet():
    """
    Негативный тест: удаление несуществующего питомца.
    """
    print("\n=== ТЕСТ: Удаление несуществующего питомца ===")

    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    # Придумываем несуществующий ID
    fake_id = "несуществующий_id_12345"
    url = f"{BASE_URL}{PETS_ENDPOINT}/{fake_id}"
    headers = {"auth_key": auth_key}

    response = requests.delete(url, headers=headers)

    if response.status_code != 200:
        print("✅ Успех! Система не дала удалить несуществующего питомца")
        print(f"Код ответа: {response.status_code}")
        return True
    else:
        print("❌ Ошибка! Система сообщила об удалении несуществующего питомца")
        return False


def test_delete_pet_without_auth():
    """
    Негативный тест: удаление питомца без авторизации.
    """
    print("\n=== ТЕСТ: Удаление питомца без авторизации ===")

    # Получаем ключ только для создания питомца
    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    # Создаем питомца
    pet_id = create_test_pet(auth_key)

    if not pet_id:
        print("❌ Ошибка! Не удалось создать тестового питомца")
        return False

    print(f"Создан тестовый питомец с ID: {pet_id}")

    # Пытаемся удалить без ключа авторизации
    url = f"{BASE_URL}{PETS_ENDPOINT}/{pet_id}"
    # headers отсутствуют!

    response = requests.delete(url)

    if response.status_code != 200:
        print("✅ Успех! Система не дала удалить питомца без авторизации")
        print(f"Код ответа: {response.status_code}")

        # Очистка: удаляем питомца с ключом
        headers = {"auth_key": auth_key}
        requests.delete(url, headers=headers)

        return True
    else:
        print("❌ Ошибка! Питомец удален без авторизации")

        # Очистка на всякий случай
        headers = {"auth_key": auth_key}
        requests.delete(url, headers=headers)

        return False
