from iebank_api import app
import pytest

def test_root_endpoint(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'


def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_skull_endpoint(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/skull' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/skull')
    assert response.status_code == 200
    assert b'This is the BACKEND SKULL' in response.data

def test_dummy_wrong_path():
    """
    GIVEN a Flask application
    WHEN the '/wrong_path' page is requested (GET)
    THEN check the response is valid
    """
    with app.test_client() as client:
        response = client.get('/wrong_path')
        assert response.status_code == 404

def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check the response is valid
    """
    response = testing_client.post('/accounts', json={
        'name': 'John Doe',
        'currency': '€',
        'country': 'Spain'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John Doe'
    assert data['currency'] == '€'
    assert data['country'] == 'Spain'

def test_get_account_by_id(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is requested (GET)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Jose',
        'currency': '€',
        'country': 'Spain'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, get the account by id
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Jose'
    assert data['currency'] == '€'
    assert data['country'] == 'Spain'
    assert data['id'] == account_id

def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts/<id>' page is updated (PUT)
    THEN check the response is valid
    """
    # First, create an account
    create_response = testing_client.post('/accounts', json={
        'name': 'Bob',
        'currency': '$',
        'country': 'USA'
    })
    assert create_response.status_code == 200
    account_data = create_response.get_json()
    account_id = account_data['id']

    # Now, update the account
    update_response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'Robert'
    })
    assert update_response.status_code == 200
    updated_data = update_response.get_json()
    assert updated_data['name'] == 'Joe'
    assert updated_data['currency'] == '£'
    assert updated_data['country'] == 'UK'
    assert updated_data['id'] == account_id

    # Verify that the account was updated
    get_response = testing_client.get(f'/accounts/{account_id}')
    assert get_response.status_code == 200
    get_data = get_response.get_json()
    assert get_data['name'] == 'Joe'