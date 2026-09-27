import json
import pprint
from unittest.mock import Mock

import allure
import requests
from faker import Faker

from helpers.allure_helper import attach_json

fake = Faker()


@allure.feature("Employee")
@allure.story("Get employees")
@allure.title("Get employees")
@allure.suite("Employee API")
@allure.description("Check list of employees")
def test_get_employees_success(base_url, auth_headers):
    with allure.step(f"Send GET /students/employees"):
        employees = requests.get(
            url=f'{base_url}/students/employees',
            headers=auth_headers
        )
    with allure.step(f"Check status code 200"):
        assert employees.status_code == 200, (
            f"error! status_code: {employees.status_code}"
        )

    with allure.step(f"Get json response"):
        employees_json = employees.json()
    with allure.step(f"Check body answer is list"):
        assert isinstance(employees_json, list)


@allure.feature("Employee")
@allure.story("Created employee")
@allure.title("Created employee")
@allure.suite("Employee API")
@allure.description("Check created employee")
def test_created_employee(base_url, auth_headers):
    with allure.step("Prepare payload"):
        email = fake.email()
        full_name = fake.name()

        payload = {
            'email': email,
            'full_name': full_name
        }

    attach_json(json.dumps(payload), "Payload")

    with allure.step(f"Send POST /students/employees"):
        created_employee = requests.post(
            url=f'{base_url}/students/employees',
            headers=auth_headers,
            json=payload
        )

    with allure.step(f"Check status code 200"):
        assert created_employee.status_code == 200

    with allure.step(f"Get json response"):
        created_employee_json = created_employee.json()

    with allure.step(f"Check email employee"):
        assert created_employee_json['email'] == email

    with allure.step(f"Check full_name employee"):
        assert created_employee_json['full_name'] == full_name

    with allure.step(f"DELETE /students/employees/{created_employee_json['id']}"):
        requests.delete(
            url=f'{base_url}/students/employees/{created_employee_json["id"]}',
            headers=auth_headers
        )


@allure.feature("Employee")
@allure.story("Get employee")
@allure.title("Get employee")
@allure.suite("Employee API")
@allure.description("Check created employee")
def test_get_employee(base_url, auth_headers, created_employee):
    id_employee, email, full_name = created_employee
    with allure.step(f"Send GET /students/employees/{id_employee}"):
        employee = requests.get(
            url=f'{base_url}/students/employees/{id_employee}',
            headers=auth_headers
        )

    # with allure.step("Attach response body to Allure report"):
    #     allure.attach(
    #         employee.text,
    #         name="Response body",
    #         attachment_type=allure.attachment_type.JSON
    #     )

    attach_json(employee.text, "Response body")

    with allure.step(f"Check status code 200"):
        assert employee.status_code == 200

    with allure.step(f"Get json response"):
        employee_json = employee.json()

    with allure.step(f"Check email employee"):
        assert employee_json['email'] == email

    with allure.step(f"Check full_name employee"):
        assert employee_json['full_name'] == full_name


@allure.feature("Employee")
@allure.story("Mock and monkeypatch")
@allure.title("Create employee with Mock")
def test_create_employee_with_mock(monkeypatch, base_url, auth_headers):
    with allure.step("Prepare payload"):
        email = fake.email()
        full_name = fake.name()

        payload = {
            'email': email,
            'full_name': full_name
        }

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {'clients_count': 0,
                                       'created_at': '2026-09-27T15:22:50.360131Z',
                                       'email': email,
                                       'first_name': 'Ricky',
                                       'full_name': full_name,
                                       'id': 'st-0631',
                                       'is_active': True,
                                       'is_blocked': False,
                                       'last_login_at': None,
                                       'last_name': 'Abbott',
                                       'status': 'ACTIVE',
                                       'tickets_count': 0,
                                       'updated_at': '2026-09-27T15:22:50.360131Z',
                                       'username': 'patricia44@example.net',
                                       'uuid': 'b54f0361-2870-4846-ac69-ce26ad786f2d'}

    requests_post_mock = Mock(return_value=fake_response)

    monkeypatch.setattr(requests, 'post', requests_post_mock)

    with allure.step(f"Send POST /students/employees"):
        created_employee = requests.post(
            url=f'{base_url}/students/employees',
            headers=auth_headers,
            json=payload
        )

    with allure.step(f"Check status code 200"):
        assert created_employee.status_code == 200

    with allure.step(f"Get json response"):
        created_employee_json = created_employee.json()

    with allure.step(f"Check email employee"):
        assert created_employee_json['email'] == email

    with allure.step(f"Check full_name employee"):
        assert created_employee_json['full_name'] == full_name

    with allure.step("Check requests.post was called with correct payload"):
        requests_post_mock.assert_called_once_with(
            url=f'{base_url}/students/employees',
            headers=auth_headers,
            json=payload
        )

    with allure.step("Check json method was called"):
        fake_response.json.assert_called_once()