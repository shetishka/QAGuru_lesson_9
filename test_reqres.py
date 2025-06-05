import json
from schemas import post_users
import requests
from jsonschema import validate


url = "https://reqres.in/api/users"

payload = {"name": "morpheus", "job": "leader"}

response = requests.request("POST", url, data=payload)

print(response.text)

def test_schema_validate_from_file():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "master"})
    body = response.json()

    assert response.status_code == 201
    with open("post_users.json") as file:
        validate(body, schema=json.loads(file.read()))


def test_post_with_schema_variable():

    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "leader"})
    body = response.json()
    assert response.status_code == 201
    validate(body, schema=post_users)


def test_schema_validate_from_variable():
    response = requests.post("https://reqres.in/api/users", data={"name": "morpheus", "job": "master"})
    body = response.json()

    assert response.status_code == 201
    validate(body, schema=post_users)