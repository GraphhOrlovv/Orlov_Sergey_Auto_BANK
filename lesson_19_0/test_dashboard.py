import pytest
import requests
import allure

from unittest.mock import Mock


# BASE_URL = 'https://api.bank.easyitlab.tech'

# def get_access_token():
#     response = requests.post(
#         url=f'{BASE_URL}/auth/login',
#         headers={
#             'Content-Type': 'application/json'
#         },
#         json={
#             "email": "seregaorlov.gus@yandex.ru",
#             "password": "8WMZTULaH05V"
#         }
#     )
#
#     assert response.status_code == 200, f"error! status_code: {response.status_code}"
#     response_json = response.json()
#
#     assert isinstance(response_json, dict)
#
#     token = response_json.get('access_token')
#     assert token, "token not found"
#     return token
#
# def get_auth_headers():
#     headers = {
#         'Authorization': f'Bearer {get_access_token()}',
#         'Content-Type': 'application/json'
#     }
#     return headers

@allure.feature("Dashboard")
@allure.story("Get dashboard")
@allure.title("Get dashboard")
@allure.suite("Dashboard API")
@allure.description("Check dashboard")
def test_get_dashboard_success(base_url, auth_headers):
    with allure.step(f"Send GET /students/dashboard"):
        students_dashboard = requests.get(
            url=f'{base_url}/students/dashboard',
            headers=auth_headers
        )

    with allure.step(f"Check status code 200"):
        assert students_dashboard.status_code == 200, f"error! status_code: {students_dashboard.status_code}"

    with allure.step(f"Check json response"):
        students_dashboard_json = students_dashboard.json()

    with allure.step(f"Check employees_total in  students_dashboard_json"):
        assert 'employees_total' in students_dashboard_json

    with allure.step(f"Check clients_total in  students_dashboard_json"):
        assert 'clients_total' in students_dashboard_json

    with allure.step(f"Check accounts_total in  students_dashboard_json"):
        assert 'accounts_total' in students_dashboard_json

    with allure.step(f"Check tickets_total in  students_dashboard_json"):
        assert 'tickets_total' in students_dashboard_json

    with allure.step(f"Check transfers_total in  students_dashboard_json"):
        assert 'transfers_total' in students_dashboard_json


class FakeDashboardResponse:
    status_code = 200

    def json(self):
        return {'accounts_total': 15,
                'clients_total': 5,
                'employees_active': 14,
                'employees_blocked': 1,
                'employees_total': 16,
                'series': [{'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-21',
                            'employees': 0,
                            'tickets': 2},
                           {'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-22',
                            'employees': 0,
                            'tickets': 1},
                           {'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-23',
                            'employees': 0,
                            'tickets': 0},
                           {'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-24',
                            'employees': 0,
                            'tickets': 0},
                           {'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-25',
                            'employees': 13,
                            'tickets': 0},
                           {'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-26',
                            'employees': 0,
                            'tickets': 0},
                           {'accounts': 0,
                            'clients': 0,
                            'day': '2026-09-27',
                            'employees': 0,
                            'tickets': 0}],
                'tickets_total': 13,
                'transfers_total': 0}


@allure.feature("Dashboard")
@allure.story("Mock and monkeypatch")
@allure.title("Get dashboard with stub")
@allure.description("Get dashboard from stub")
def test_get_dashboard_with_stub(monkeypatch, base_url, auth_headers):
    def fake_get(url, headers):
        return FakeDashboardResponse()

    monkeypatch.setattr(requests, 'get', fake_get)

    with allure.step(f"Send GET /students/dashboard"):
        students_dashboard = requests.get(
            url=f'{base_url}/students/dashboard',
            headers=auth_headers
        )

    with allure.step(f"Check status code 200"):
        assert students_dashboard.status_code == 200, f"error! status_code: {students_dashboard.status_code}"

    with allure.step(f"Check json response"):
        students_dashboard_json = students_dashboard.json()

    with allure.step(f"Check employees_total in  students_dashboard_json"):
        assert 'employees_total' in students_dashboard_json

    with allure.step(f"Check clients_total in  students_dashboard_json"):
        assert 'clients_total' in students_dashboard_json

    with allure.step(f"Check accounts_total in  students_dashboard_json"):
        assert 'accounts_total' in students_dashboard_json

    with allure.step(f"Check tickets_total in  students_dashboard_json"):
        assert 'tickets_total' in students_dashboard_json

    with allure.step(f"Check transfers_total in  students_dashboard_json"):
        assert 'transfers_total' in students_dashboard_json


@allure.feature("Dashboard")
@allure.story("Mock and monkeypatch")
@allure.title("Get dashboard with Mock")
@allure.description("Get dashboard from Mock")
def test_get_dashboard_with_mock(monkeypatch, base_url, auth_headers):
    fake_response = Mock()

    fake_response.status_code = 200
    fake_response.json.return_value = {'accounts_total': 15,
                                       'clients_total': 5,
                                       'employees_active': 14,
                                       'employees_blocked': 1,
                                       'employees_total': 16,
                                       'tickets_total': 13,
                                       'transfers_total': 0}

    requests_get_mock = Mock(return_value=fake_response)

    monkeypatch.setattr(requests, 'get', requests_get_mock)

    with allure.step(f"Send GET /students/dashboard"):
        students_dashboard = requests.get(
            url=f'{base_url}/students/dashboard',
            headers=auth_headers
        )

    with allure.step(f"Check status code 200"):
        assert students_dashboard.status_code == 200, f"error! status_code: {students_dashboard.status_code}"

    with allure.step(f"Check json response"):
        students_dashboard_json = students_dashboard.json()

    with allure.step(f"Check employees_total in  students_dashboard_json"):
        assert 'employees_total' in students_dashboard_json

    with allure.step(f"Check clients_total in  students_dashboard_json"):
        assert 'clients_total' in students_dashboard_json

    with allure.step(f"Check accounts_total in  students_dashboard_json"):
        assert 'accounts_total' in students_dashboard_json

    with allure.step(f"Check tickets_total in  students_dashboard_json"):
        assert 'tickets_total' in students_dashboard_json

    with allure.step(f"Check transfers_total in  students_dashboard_json"):
        assert 'transfers_total' in students_dashboard_json

    with allure.step(
            'Check requests.get was called with correct url and headers'
    ):
        requests_get_mock.assert_called_once_with(
            url=f'{base_url}/students/dashboard',
            headers=auth_headers
        )

    with allure.step("Check json method was called"):
        fake_response.json.assert_called_once()


@allure.feature("Dashboard")
@allure.story("Mock and monkeypatch")
@allure.title("Dashboard requests failed")
def test_get_dashboard_requests_failed(monkeypatch, base_url, auth_headers):
    requests_get_mock = Mock(
        side_effect=requests.ConnectionError("Service unavailable")
    )

    monkeypatch.setattr(requests, 'get', requests_get_mock)

    with pytest.raises(requests.ConnectionError):
        requests.get(
            url=f'{base_url}/students/dashboard',
            headers=auth_headers
        )

        requests_get_mock.assert_called_once_with(
            url=f'{base_url}/students/dashboard',
            headers=auth_headers
        )
