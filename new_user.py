import requests
from values import *

url = "https://petfriends.skillfactory.ru/new_user"

# Позитивный тест
def test_register_new_user_success():

    data = {
        "name": "Alice",
        "pass": VALID_PASS,
        "email": VALID_EMAIL
    }

    response = requests.post(url, data=data)

    assert response.status_code == 200, f"Ожидается статус-код 200, получен {response.status_code}"

    print("\nПользователь успешно зарегистрирован")

# Негативный, не валидный емейл
def test_register_with_invalid_email():

    data = {
        "name": "Bob",
        "pass": VALID_PASS,
        "email": "bobexample.com"
    }

    response = requests.post(url, data=data)

    assert response.status_code != 200, \
        "Регистрация прошла, хотя email невалидный"

    print("\nТест пройден: регистрация с неверным email не удалась")
    print(f"Ответ сервера - {response.status_code}")

# Негативный, отсутствует пароль
def test_register_missing_password():

    data = {
        "name": "Charlie",
        "email": "charlie@example.com"
        # pass отсутствует
    }

    response = requests.post(url, data=data)

    assert response.status_code != 200, \
        "Регистрация прошла, хотя отсутствует пароль"

    print("\nТест пройден: регистрация без пароля не удалась")
    print(f"Ответ сервера - {response.status_code}")

# # Негативный, слишком длинные строки
def test_register_with_very_long_data():

    long_name = "A" * 1000
    long_email = "B" * 100 + "@example.com"
    long_pass = "C" * 1000

    data = {
        "name": long_name,
        "pass": long_pass,
        "email": long_email
    }

    response = requests.post(url, data=data)

    assert response.status_code != 200, \
        "Регистрация прошла, хотя были переданы слишком длинные данные"

    print("\nТест пройден: система корректно обработала длинные поля")
    print(f"Ответ сервера - {response.status_code}")


all_tests = [
    test_register_new_user_success,
    test_register_with_invalid_email,
    test_register_missing_password,
    test_register_with_very_long_data,
]

# Оборачиваем в try/except для того, чтобы тесты выполнялись стабильно набором
for test in all_tests:
    try:
        test()
    except AssertionError as e:
        print(f"[FAIL] Тест {test.__name__} упал с ошибкой: {e}")
    except Exception as e:
        print(f"[ERROR] Непредвиденная ошибка в тесте {test.__name__}: {e}")
    else:
        print(f"[OK] Тест {test.__name__} успешно пройден")
    print("-" * 50)
