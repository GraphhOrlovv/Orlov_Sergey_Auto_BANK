import requests
import allure


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

    with allure.step(f"Get json response"):
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
