import requests

# отдельные методы для тестирования всех эндпойнтов, данные генерировать или запрашивать с клавиатуры
def test_get_authors():
    url = "http://localhost:5000/api/authors"
    response = requests.get(url)
    print(response.json())

def test_create_authors():
    url = "http://localhost:5000/api/authors"
    response = requests.get(url)
    print(response.json())
    data = {
        'name': 'tolsddddtoy lev nikolevich',
    }
    response = requests.post(url, json=data)
    print(response)

    response = requests.get(url)
    print(response.json())

def test_update_authors():
    url = "http://localhost:5000/api/authors"
    response = requests.get(url)
    print(response.json())

    author_id = 1
    author_data = requests.get('{url}/{author_id}')
    author_data = {
        'biography': 'tolsddddtoy lev nikolevich',
    }
    response = requests.put(url, json=author_data)
    print(response)

    response = requests.get(url)
    print(response.json())

def test_delete_author():
    url = "http://localhost:5000/api/authors"
    response = requests.get(url)
    print(response.json())

    author_id = 1

    requests.delete(f'{url}/{author_id}')

    response = requests.get(url)
    print(response.json())


# отдельные тестовые методы для остальных моделей и хендлеров (кроме книги)

if __name__ == "__main__":
    test_authors()