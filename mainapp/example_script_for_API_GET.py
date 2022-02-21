import requests

url = 'http://localhost:8000/api/'  # Полный адрес эндпоинта
response = requests.get(url)  # Делаем GET-запрос
# Поскольку данные пришли в формате json, переведем их в python
response_on_python = response.json()
# Запишем полученные данные в файл product.txt
with open('product.txt', 'w') as file:
    for product in response_on_python:
        file.write(
            f"The name of {product['name']} is "
            f"{product['category']}, "
            f"description - {product['description']}\n"
        )
