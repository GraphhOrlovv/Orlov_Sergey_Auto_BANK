import allure
import requests
import pytest
from faker import Faker
fake = Faker()


@pytest.fixture(scope='session')
def base_url():
    base_url = 'https://api.bank.easyitlab.tech'
    return base_url

@pytest.fixture(scope='session')
def access_token(base_url):
    response = requests.post(
        url=f'{base_url}/auth/login',
        headers={
            'Content-Type': 'application/json'
        },
        json={
            "email": "seregaorlov.gus@yandex.ru",
            "password": "8WMZTULaH05V"
        }
    )

    assert response.status_code == 200, f"error! status_code: {response.status_code}"
    response_json = response.json()

    assert isinstance(response_json, dict)

    access_token = response_json.get('access_token')
    assert access_token, "token not found"
    return access_token

@pytest.fixture
def auth_headers(access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    return headers

@pytest.fixture(scope='function')
def created_employee(base_url, auth_headers):
    email = fake.email()
    full_name = fake.name()

    payload = {
        'email': email,
        'full_name': full_name
    }

    created_employee = requests.post(
        url=f'{base_url}/students/employees',
        headers=auth_headers,
        json=payload
    )

    assert created_employee.status_code == 200

    created_employee_json = created_employee.json()

    assert created_employee_json['email'] == email
    assert created_employee_json['full_name'] == full_name

    # print(created_employee_json['id'])

    yield (
        created_employee_json['id'],
        created_employee_json['email'],
        created_employee_json['full_name']
    )
    with allure.step(f"DELETE /students/employees/{created_employee_json['id']}"):
        requests.delete(
            url=f'{base_url}/students/employees/{created_employee_json["id"]}',
            headers=auth_headers
        )

        # print(deleted_employee.text)