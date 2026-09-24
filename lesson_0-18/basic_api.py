import requests
import pprint
from faker import Faker
fake = Faker()

BASE_URL = 'https://api.bank.easyitlab.tech'

# headers = {
#     'Authorization': f'Bearer {TOKEN}',
#     'Content-Type': 'application/json'
# }
#
# body = {
#     'email': 'erjgoer@efef.ru',
# }

# response = requests.get(
#     url=f'{BASE_URL}/students/employees',
#     headers=headers
# )
#
# print(response.status_code)
# pprint.pprint(response.json())

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

# print(status_code)
# pprint.pprint(json)
# print(TOKEN)

def create_employee():
    print("1. Create Employee")
    body = {
        'email': fake.email(),
        'full_name': fake.name()
    }

    created_employee = requests.post(
        url=f'{BASE_URL}/students/employees',
        headers=headers,
        json=body
    )
    assert created_employee.status_code == 200, f"Что-то пошло не так, статус код: {created_employee.status_code}"
    created_employee_json = created_employee.json()
    employee_id = created_employee_json.get('id')
    return employee_id

def delete_employee(employee_id):
    print("2. Delete Employee")
    deleted_employee = requests.delete(
        url=f'{BASE_URL}/students/employees/{employee_id}',
        headers=headers
    )
    assert deleted_employee.status_code == 200, f"Что-то пошло не так, статус код: {deleted_employee.status_code}"

def test_employee_lifecycle():
    print('3. Start Test')
    employee_id = create_employee()
    delete_employee(employee_id)
    print('4. End Test')

# test_employee_lifecycle()

def generate_employees():
    generated_employees = requests.post(
        url=f'{BASE_URL}/students/entities/generate',
        headers=headers,
        json={
            "confirm_cleanup": True
        }
    )

generate_employees()