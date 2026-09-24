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

    assert response.status_code == 200, f"error! status_code: {response.status_code}"
    response_json = response.json()

    assert isinstance(response_json, dict)

    token = response_json.get('access_token')
    assert token, "token not found"
    return token

def get_auth_headers():
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'Content-Type': 'application/json'
    }
    return headers

def test_get_dashboard_success():
    headers = get_auth_headers()
    students_dashboard = requests.get(
        url=f'{BASE_URL}/students/dashboard',
        headers=headers
    )

    assert students_dashboard.status_code == 200, f"error! status_code: {students_dashboard.status_code}"

    students_dashboard_json = students_dashboard.json()

    assert 'employees_total' in students_dashboard_json
    assert 'clients_total' in students_dashboard_json
    assert 'accounts_total' in students_dashboard_json
    assert 'tickets_total' in students_dashboard_json
    assert 'transfers_total' in students_dashboard_json