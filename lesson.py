import requests

data = {
    "title": "новый пост",
    "body": "это текст поста",
    "userId": 1
}

response = requests.post("https://jsonplaceholder.typicode.com/posts", json=data)

print(response.status_code)

print(response.json())