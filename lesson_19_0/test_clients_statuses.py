import requests
import pytest


@pytest.mark.api
@pytest.mark.parametrize(
    'status',
    [
        "NEW",
        "PENDING_VERIFICATION",
        "ACTIVE",
        "SUSPENDED",
        "BLOCKED",
        "CLOSED",
        "ARCHIVED"
    ]
)
def test_get_client_by_status(base_url, auth_headers, status):
    client_by_status = requests.get(
        url=f'{base_url}/students/clients',
        headers=auth_headers,
        params={'status': status}
    )

    assert client_by_status.status_code == 200
    # print(client_by_status.text)

    client_by_status_json = client_by_status.json()

    assert isinstance(client_by_status_json, list)

    for client in client_by_status_json:
        print(client['first_name'])
        assert client['status'] == status
