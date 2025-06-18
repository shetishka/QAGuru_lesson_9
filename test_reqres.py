import json

import requests
from jsonschema import validate
from schemas import create_user, successful_registration, unsuccessful_registration, update_user, full_user_info



url = 'https://reqres.in'

def test_GET_one_user():
    end_point = "/api/users/2"
    payload = {}

    response = requests.request("GET", url + end_point, data=payload)
    body = response.json()

    assert response.status_code == 200
    assert "data" in body
    assert body["data"]["id"] == 2

def test_POST_user():
    end_point = '/api/users'
    job = "master"
    name = "morpheus"

    response = requests.post(url + end_point,
                             {"name": name, "job": job})
    body = response.json()

    assert response.status_code == 201
    assert body["name"] == name
    assert body["job"] == job


def test_PUT_user():
    end_point = '/api/users/2'
    payload = {"job": "zion resident", "name": "morpheus"}

    response = requests.put(url + end_point, data=payload)

    body = response.json()
    assert response.status_code == 200
    assert body["name"] == payload["name"]
    assert body["job"] == payload["job"]
    assert "updatedAt" in body


def test_DELETE_request():
    end_point = '/api/users/2'

    response = requests.delete(url + end_point)

    assert response.status_code == 204


def test_GET_with_incorrect_end_point():
    incorrect_end_point = "/api/users/100"

    response = requests.get(url + incorrect_end_point)

    assert response.status_code == 404

def test_POST_unsuccessful_registration_with_no_password():
    end_point = '/api/register'

    response = requests.post(url + end_point)

    assert response.status_code == 400


def test_schema_add_user():
    end_point = '/api/users/2'
    payload = {"job": "zion resident", "name": "Olga"}

    response = requests.post(url + end_point, data=payload)
    print(response.status_code)
    body = response.json()
    validate(body, schema=create_user)


def test_schema_Update_user():
    end_point = '/api/users'
    payload = {"job": "leader", "name": "morpheus"}

    response = requests.post(url + end_point, data=payload)

    body = response.json()
    validate(body, schema=update_user)


def test_schema_get_users_info():
    end_point = '/api/users/2'

    response = requests.get(url + end_point)

    body = response.json()
    validate(body, schema=full_user_info)


def test_schema_successful_registration():
    end_point = '/api/register'
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(url + end_point, data=payload)

    body = response.json()
    validate(body, schema=successful_registration)


def test_schema_unsuccessful_registration():
    end_point = '/api/register'
    payload = {"email": "sydney@fife"}
    response = requests.post(url + end_point, data=payload)

    body = response.json()
    validate(body, schema=unsuccessful_registration)


def test_list_of_users_per_page():
    page = 2
    per_page = 6
    url = "https://reqres.in/api/users"
    with step("API Request"):
        result = requests.get(
            url=url,
            params={"page": page, "per_page": per_page}
        )
        allure.attach(body=json.dumps(result.json(), indent=4, ensure_ascii=True), name="Response", attachment_type=AttachmentType.JSON, extension="json")
    assert result.json()["per_page"] == per_page
    assert len(result.json()['data']) == per_page
