"""
Тесты для регистрации новых пользователей.
"""

import requests
from config import BASE_URL, NEW_USER_ENDPOINT, VALID_EMAIL, VALID_PASS


def test_successful_registration():
    """
    Позитивный тест: успешная регистрация с правильными данными.

    Что проверяем:
    - Можно ли зарегистрироваться с валидными email и паролем
    """
    print("\n=== ТЕСТ: Успешная регистрация ===")

    url = BASE_URL + NEW_USER_ENDPOINT

    # Данные для регистрации
    data = {
        "name": "Alice",
        "pass": VALID_PASS,
        "email": VALID_EMAIL
    }

    # Отправляем POST запрос
    response = requests.post(url, data=data)

    # Проверяем результат
    if response.status_code == 200:
        print("✅ Успех! Пользователь зарегистрирован")
        print(f"Код ответа: {response.status_code}")
    else:
        print(f"❌ Ошибка! Код ответа: {response.status_code}")
        print(f"Текст ошибки: {response.text}")

    # Возвращаем результат для общего отчета
    return response.status_code == 200


def test_registration_invalid_email():
    """
    Негативный тест: регистрация с неправильным email (без @).

    Что проверяем:
    - Система не должна регистрировать пользователя с неверным email
    """
    print("\n=== ТЕСТ: Регистрация с неверным email ===")

    url = BASE_URL + NEW_USER_ENDPOINT

    # Email без символа @ - должен быть невалидным
    data = {
        "name": "Bob",
        "pass": VALID_PASS,
        "email": "bobexample.com"  # Неправильный email!
    }

    response = requests.post(url, data=data)

    # Ожидаем, что регистрация НЕ пройдет (код НЕ 200)
    if response.status_code != 200:
        print("✅ Успех! Система не дала зарегистрироваться с неверным email")
        print(f"Код ответа: {response.status_code} (ожидали не 200)")
    else:
        print("❌ Ошибка! Система пропустила регистрацию с неверным email")

    return response.status_code != 200


def test_registration_missing_password():
    """
    Негативный тест: регистрация без пароля.

    Что проверяем:
    - Система требует пароль при регистрации
    """
    print("\n=== ТЕСТ: Регистрация без пароля ===")

    url = BASE_URL + NEW_USER_ENDPOINT

    # Данные без пароля
    data = {
        "name": "Charlie",
        "email": "charlie@example.com"
        # Поле "pass" отсутствует!
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print("✅ Успех! Система не дала зарегистрироваться без пароля")
        print(f"Код ответа: {response.status_code}")
    else:
        print("❌ Ошибка! Система пропустила регистрацию без пароля")

    return response.status_code != 200


def test_registration_long_data():
    """
    Негативный тест: регистрация с очень длинными данными.

    Что проверяем:
    - Система ограничивает длину полей
    """
    print("\n=== ТЕСТ: Регистрация с длинными данными ===")

    url = BASE_URL + NEW_USER_ENDPOINT

    # Создаем очень длинные строки
    long_name = "A" * 1000  # Имя из 1000 букв А
    long_email = "B" * 100 + "@example.com"  # Очень длинный email
    long_pass = "C" * 1000  # Пароль из 1000 символов

    data = {
        "name": long_name,
        "pass": long_pass,
        "email": long_email
    }

    response = requests.post(url, data=data)

    if response.status_code != 200:
        print("✅ Успех! Система отклонила слишком длинные данные")
        print(f"Код ответа: {response.status_code}")
    else:
        print("❌ Ошибка! Система приняла слишком длинные данные")

    return response.status_code != 200
