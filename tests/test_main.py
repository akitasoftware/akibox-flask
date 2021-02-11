import copy
import json
import pytest

from flaskr.main import User, app
from akita_flask.testing import HarClient

@pytest.fixture(scope="module")
def client():
    app.config['TESTING'] = True
    app.test_client_class = HarClient

    with app.test_client() as client:
        yield client

def test_default_users(client):
    rv = client.get('/users')
    data = json.loads(rv.data.decode('utf-8'))
    assert len(data['users']) == 2

def test_default_files(client):
    rv = client.get('/users')
    users = json.loads(rv.data.decode('utf-8'))
    for user_json in users['users']:
        user = User.parse_obj(user_json)
        rv = client.get(f'/users/{user.id}/files')
        file_data = json.loads(rv.data.decode('utf-8'))
        assert len(file_data['files']) == 0

def test_user_crud(client):
    kent = {
        "first_name": "Kent",
        "last_name": "Bazemore",
        "email": "kent@warriors.com",
        "phone": "415-111-2233",
    }

    # Create user
    response = client.post('/users', data=json.dumps(kent), content_type="application/json")
    expected = copy.deepcopy(kent)
    expected["id"] = response.json["id"]

    assert response.json == expected
    assert response.status_code == 201

    # Get user
    response = client.get(f'/users/{expected["id"]}')
    assert response.json == expected
    assert response.status_code == 200

    # Update user
    expected["phone"] = "415-999-8877"
    response = client.put(f'/users/{expected["id"]}', data=json.dumps(expected), content_type='application/json')
    assert response.json == expected
    assert response.status_code == 200

    # Delete user
    response = client.delete(f'/users/{expected["id"]}')
    assert response.status_code == 204

    # Try to get user, should fail
    response = client.get(f'/users/{expected["id"]}')
    assert response.status_code == 404

