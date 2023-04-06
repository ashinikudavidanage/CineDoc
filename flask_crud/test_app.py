from app import app
import pytest
import io
from PIL import Image
import json
        
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# POST request to check registration
def test_signup(client):
    data={"name":"name", "email":"email", "phone":"phone", "pwd" : "pwd"}
    json_data = json.dumps(data)
    response = client.post('/register', data=json_data, headers={'content-type': 'application/json'})
    # status code
    assert response.status_code == 200

# POST request to the check false registration
def test_false_signup(client):
    data={"name":None, "email":"email", "phone":None, "pwd" : "pwd"}
    json_data = json.dumps(data)
    response = client.post('/register', data=json_data, headers={'content-type': 'application/json'})
    # status code
    assert response.status_code == 400    

# POST request to the check login
def test_login(client):
    data={"name":"kevin", "pwd" : "1@!45"}
    json_data = json.dumps(data)
    response = client.post('/login', data=json_data, headers={'content-type': 'application/json'})
    # status code
    assert response.status_code == 200

# POST request to the check false login
def test_false_login(client):
    data={"name":"kevin", "pwd" : "1@!45"}
    json_data = json.dumps(data)
    response = client.post('/login', data=json_data, headers={'content-type': 'application/json'})
    # status code
    assert response.status_code == 400
