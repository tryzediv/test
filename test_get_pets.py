"""
Тесты для получения списка питомцев.
"""

import requests
from config import BASE_URL, PETS_ENDPOINT
from helpers import get_api_key


def test_get_all_pets():
    """
    Тест получения всех питомцев.
    """
    print("\n=== ТЕСТ: Получение всех питомцев ===")

    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    url = BASE_URL + PETS_ENDPOINT
    headers = {"auth_key": auth_key}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            result = response.json()
            pets = result.get('pets', [])
            print(f"✅ Успех! Получен список питомцев")
            print(f"Всего питомцев: {len(pets)}")

            # Показываем первых 3 питомцев
            if pets:
                print("\nПервые 3 питомца:")
                for i, pet in enumerate(pets[:3]):
                    print(f"  {i + 1}. {pet.get('name', 'Без имени')} "
                          f"({pet.get('animal_type', '?')}, {pet.get('age', '?')} лет)")
            return True
        except:
            print("❌ Ошибка! Не удалось разобрать ответ")
            return False
    else:
        print(f"❌ Ошибка! Код ответа: {response.status_code}")
        return False


def test_get_my_pets():
    """
    Тест получения только своих питомцев.
    """
    print("\n=== ТЕСТ: Получение своих питомцев ===")

    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    url = BASE_URL + PETS_ENDPOINT
    headers = {"auth_key": auth_key}
    params = {"filter": "my_pets"}  # Фильтр "только мои"

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        try:
            result = response.json()
            my_pets = result.get('pets', [])
            print(f"✅ Успех! Получен список ваших питомцев")
            print(f"У вас {len(my_pets)} питомцев")

            if my_pets:
                print("\nВаши питомцы:")
                for i, pet in enumerate(my_pets[:5]):
                    print(f"  {i + 1}. {pet.get('name', 'Без имени')} - {pet.get('id', 'нет ID')}")
            return True
        except:
            print("❌ Ошибка! Не удалось разобрать ответ")
            return False
    else:
        print(f"❌ Ошибка! Код ответа: {response.status_code}")
        return False


def test_get_pets_invalid_filter():
    """
    Тест с несуществующим фильтром.
    """
    print("\n=== ТЕСТ: Получение питомцев с неверным фильтром ===")

    auth_key = get_api_key()

    if not auth_key:
        print("❌ Ошибка! Не удалось получить ключ авторизации")
        return False

    url = BASE_URL + PETS_ENDPOINT
    headers = {"auth_key": auth_key}
    params = {"filter": "такого_фильтра_нет"}  # Неправильный фильтр

    response = requests.get(url, headers=headers, params=params)

    # Проверяем любой код ответа (лишь бы не 500 ошибка сервера)
    if response.status_code < 500:
        print("✅ Успех! Система обработала запрос с неверным фильтром")
        print(f"Код ответа: {response.status_code}")
        return True
    else:
        print("❌ Ошибка! Сервер упал с ошибкой")
        return False
