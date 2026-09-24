from pprint import pprint
from faker import Faker
fake = Faker()

import requests

BASE_URL = 'https://api.bank.easyitlab.tech'

def get_access_token():
    response = requests.post(
        url=f'{BASE_URL}/auth/login',
        headers={
            'Content-Type': 'application/json'
        },
        json={
            "email": "seregaorlov.gus@yandex.ru",
            "password": "8WMZTULaH05V"
        }
    )
    return response

response = get_access_token()
status_code = response.status_code
json = response.json()

TOKEN = json.get('access_token')

headers = {
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
}

# get_users = requests.get(
#     url=f'{BASE_URL}/students/clients',
#     headers=headers
# )

# pprint(get_users.json())

# get_users_filter = requests.get(
#     url=f'{BASE_URL}/students/clients?status=ACTIVE&NEW',
#     headers=headers
# )

params = {
    'status': 'SUSPENDED',
}

get_users_filter = requests.get(
    url=f'{BASE_URL}/students/clients',
    headers=headers,
    params=params
)

pprint(get_users_filter.json())

# def test_clients_status_suspended():
#     params = {
#             'status': 'SUSPENDED',
#         }
#     get_users_filter = requests.get(
#         url=f'{BASE_URL}/students/clients',
#         headers=headers,
#         params=params
#     )
#
#     for user in get_users_filter.json():
#         assert user['status'] == 'SUSPENDED', user
#     print("test success")
#
# test_clients_status_suspended()