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

def test_api_users_https():
    response = requests.get(
        url=f'{BASE_URL}/students/dashboard',
        headers=headers
    )

    assert response.url.startswith('https://')

def get_dashboard():
    response = requests.get(
        url=f'{BASE_URL}/students/dashboard',
        headers=headers
    )

    assert response.url.startswith('https://')
    return response.json()

def test_dashboard_employee_create():
    before = get_dashboard()

    payload = {
        'email': fake.email(),
        'full_name': fake.name()
    }

    requests.post(
        url=f'{BASE_URL}/students/employees',
        headers=headers,
        json=payload
    )

    after = get_dashboard()

    print(after['employees_total'])
    print(before['employees_total'])

    assert after['employees_total'] >= before['employees_total']

# test_dashboard_employee_create()

def get_response_dashboard():
    response = requests.get(
        url=f'{BASE_URL}/students/dashboard',
        headers=headers
    )

    assert response.url.startswith('https://')
    return response

def test_rate_limiting():
    status = 200
    counter = 0
    while status != 429:
        status = get_response_dashboard().status_code
        counter += 1
    return counter

counter = test_rate_limiting()
print(counter)