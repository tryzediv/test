import requests
from helper import *

url = f"https://petfriends.skillfactory.ru/api/pets/{get_my_pets_id()}"

# Тест: удаление существующего питомца
def test_delete_existing_pet():

    headers = {
        "auth_key": get_api_key()
    }

    response = requests.delete(url, headers=headers)
    assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"


# Негативный тест 1: попытка удалить несуществующего питомца
def test_delete_nonexistent_pet():

    endpoint = "https://petfriends.skillfactory.ru/api/pets/nonexistent_pet_id"
    headers = {
        "auth_key": get_api_key()
    }

    response = requests.delete(endpoint, headers=headers)
    assert response.status_code != 200, "Сервер вернул 200 при удалении несуществующего питомца"
    print(f"Тест пройден: удаление несуществующего питомца завершено с кодом {response.status_code}")
