import unittest

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

    token = response.json().get('access_token')
    return token

def get_auth_headers():
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json'
    }
    return headers


class TestStudentDashboard(unittest.TestCase):

    def ttest_get_dashboard_success(self):
        headers = get_auth_headers()

        students_dashboard = requests.get(
            url=f'{BASE_URL}/students/dashboard',
            headers=headers
        )

        self.assertEqual(students_dashboard.status_code, 200)

        students_dashboard_json = students_dashboard.json()

        self.assertIn('employees_total', students_dashboard_json)
        self.assertIn('clients_total', students_dashboard_json)
        self.assertIn('accounts_total', students_dashboard_json)
        self.assertIn('tickets_total', students_dashboard_json)
        self.assertIn('transfers_total', students_dashboard_json)


if __name__ == '__main__':
    unittest.main()
else:
    print('__name__', __name__)