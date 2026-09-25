import json

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
