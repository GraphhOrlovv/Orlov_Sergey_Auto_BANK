from pprint import pprint

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

def get_employee_id():
    response = requests.get(
        url=f'{BASE_URL}/students/employees',
        headers=headers
    )
    employee_id = response.json()[0].get('id')
    return employee_id

pprint(get_employee_id())

# employees = get_employees()

def delete_employee(employee_id):
    deleted_employee = requests.delete(
        url=f'{BASE_URL}/students/employees/{employee_id}',
        headers=headers
    )
    assert deleted_employee.status_code == 200, f"Что-то пошло не так, статус код: {deleted_employee.status_code}"

delete_employee(get_employee_id())