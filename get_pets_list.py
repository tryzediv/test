import requests
from helper import get_api_key

url = "https://petfriends.skillfactory.ru/api/pets"


def test_get_all_pets():

    headers = {
        "auth_key": get_api_key()
    }

    response = requests.get(url, headers=headers)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    try:
        json_response = response.json()
        assert "pets" in json_response, "\nВ ответе отсутствует поле 'pets'"
        print("\nКоличество питомцев:", len(json_response["pets"]))
    except ValueError:
        raise Exception("\nНевозможно разобрать JSON. Ответ сервера:", response.text)


def test_get_my_pets():

    headers = {
        "auth_key": get_api_key()
    }

    params = {
        "filter": "my_pets"
    }

    response = requests.get(url, headers=headers, params=params)

    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

    try:
        json_response = response.json()
        assert "pets" in json_response, "\nВ ответе отсутствует поле 'pets'"

        if len(json_response["pets"]) > 0:
            print("\nСписок ваших питомцев:")
            for pet in json_response["pets"]:
                print(f"{pet['name']}, {pet['animal_type']}, возраст: {pet['age']}")
        else:
            print("\nУ вас пока нет питомцев")
    except ValueError:
        raise Exception("\nНевозможно разобрать JSON. Ответ сервера:", response.text)


def test_get_pets_with_invalid_filter():

    headers = {
        "auth_key": get_api_key()
    }

    params = {
        "filter": "unknown_filter"
    }

    response = requests.get(url, headers=headers, params=params)

    assert response.status_code == 200 or response.status_code == 400, \
        f"Неожиданный статус-код: {response.status_code}"

    print("Тест пройден: запрос с некорректным фильтром завершён с кодом", response.status_code)
