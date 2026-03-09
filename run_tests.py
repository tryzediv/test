"""
Главный файл для запуска всех тестов.
Простой и понятный для начинающих.
"""

# Импортируем все тесты
from test_registration import *
from test_api_key import *
from test_create_pet import *
from test_get_pets import *
from test_delete_pet import *


def print_header(text):
    """Печатает красивый заголовок."""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)


def print_result(test_name, success):
    """Печатает результат теста."""
    if success:
        print(f"  ✅ {test_name} - УСПЕХ")
    else:
        print(f"  ❌ {test_name} - ПРОВАЛ")


def run_all_tests():
    """
    Запускает все тесты по порядку и собирает статистику.
    """
    print_header("ЗАПУСК ВСЕХ ТЕСТОВ")

    # Список всех тестов с их названиями
    tests = [
        # Тесты регистрации
        ("Регистрация (успех)", test_successful_registration),
        ("Регистрация (неверный email)", test_registration_invalid_email),
        ("Регистрация (без пароля)", test_registration_missing_password),
        ("Регистрация (длинные данные)", test_registration_long_data),

        # Тесты получения ключа
        ("Получение ключа (успех)", test_get_key_valid_credentials),
        ("Получение ключа (неверный email)", test_get_key_invalid_email),
        ("Получение ключа (неверный пароль)", test_get_key_invalid_password),
        ("Получение ключа (без email)", test_get_key_missing_email),

        # Тесты создания питомца
        ("Создание питомца (успех)", test_create_pet_success),
        ("Создание питомца (неверный ключ)", test_create_pet_invalid_auth),
        ("Создание питомца (без ключа)", test_create_pet_without_auth),

        # Тесты получения списка
        ("Получение всех питомцев", test_get_all_pets),
        ("Получение своих питомцев", test_get_my_pets),
        ("Получение с неверным фильтром", test_get_pets_invalid_filter),

        # Тесты удаления
        ("Удаление питомца (успех)", test_delete_existing_pet),
        ("Удаление несуществующего", test_delete_nonexistent_pet),
        ("Удаление без авторизации", test_delete_pet_without_auth),
    ]

    # Запускаем тесты и собираем статистику
    results = []
    passed = 0
    failed = 0

    for test_name, test_function in tests:
        print(f"\n▶ Запуск: {test_name}")
        print("-" * 40)

        try:
            # Запускаем тест
            success = test_function()

            # Сохраняем результат
            results.append((test_name, success))

            if success:
                passed += 1
            else:
                failed += 1

        except Exception as e:
            # Если тест упал с ошибкой
            print(f"❌ Ошибка при выполнении теста: {e}")
            results.append((test_name, False))
            failed += 1

        print("-" * 40)

    # Выводим итоговую статистику
    print_header("ИТОГИ ТЕСТИРОВАНИЯ")

    print("\nРезультаты по каждому тесту:")
    for test_name, success in results:
        print_result(test_name, success)

    print(f"\nВсего тестов: {len(tests)}")
    print(f"✅ Успешно: {passed}")
    print(f"❌ Провалено: {failed}")

    if failed == 0:
        print("\n🎉 ПОЗДРАВЛЯЮ! Все тесты пройдены успешно!")
    else:
        print(f"\n⚠️ Внимание: {failed} тестов не пройдены.")

    print("\n" + "=" * 60)


def run_specific_test(test_name):
    """
    Запускает конкретный тест по имени.

    Аргументы:
        test_name: имя тестовой функции
    """
    # Словарь всех доступных тестов
    all_tests = {
        # Тесты регистрации
        "test_successful_registration": test_successful_registration,
        "test_registration_invalid_email": test_registration_invalid_email,
        "test_registration_missing_password": test_registration_missing_password,
        "test_registration_long_data": test_registration_long_data,

        # Тесты получения ключа
        "test_get_key_valid_credentials": test_get_key_valid_credentials,
        "test_get_key_invalid_email": test_get_key_invalid_email,
        "test_get_key_invalid_password": test_get_key_invalid_password,
        "test_get_key_missing_email": test_get_key_missing_email,

        # Тесты создания питомца
        "test_create_pet_success": test_create_pet_success,
        "test_create_pet_invalid_auth": test_create_pet_invalid_auth,
        "test_create_pet_without_auth": test_create_pet_without_auth,

        # Тесты получения списка
        "test_get_all_pets": test_get_all_pets,
        "test_get_my_pets": test_get_my_pets,
        "test_get_pets_invalid_filter": test_get_pets_invalid_filter,

        # Тесты удаления
        "test_delete_existing_pet": test_delete_existing_pet,
        "test_delete_nonexistent_pet": test_delete_nonexistent_pet,
        "test_delete_pet_without_auth": test_delete_pet_without_auth,
    }

    if test_name in all_tests:
        print_header(f"ЗАПУСК ТЕСТА: {test_name}")
        try:
            success = all_tests[test_name]()
            print_result(test_name, success)
        except Exception as e:
            print(f"❌ Ошибка при выполнении теста: {e}")
    else:
        print(f"❌ Тест '{test_name}' не найден")
        print("\nДоступные тесты:")
        for name in all_tests.keys():
            print(f"  - {name}")


# Если файл запускают напрямую
if __name__ == "__main__":
    import sys

    # Проверяем, передан ли аргумент командной строки
    if len(sys.argv) > 1:
        # Если есть аргумент, запускаем конкретный тест
        test_name = sys.argv[1]
        run_specific_test(test_name)
    else:
        # Если нет аргументов, запускаем все тесты
        run_all_tests()
