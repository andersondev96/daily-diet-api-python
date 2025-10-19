import pytest
import json
import sys
import os
import bcrypt

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from models.user import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    ctx = app.app_context()
    ctx.push()
    db.create_all()

    yield app.test_client()

    db.session.remove()
    db.drop_all()
    ctx.pop()

def test_create_user_success(client):
    """
    Testa a criação de um novo usuário com sucesso.
    """
    response = client.post('/users', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'User created'
    assert data['user']['username'] == 'testuser'

    user = User.query.filter_by(username='testuser').first()

    assert user is not None
    assert user.password != 'testpassword'
    assert bcrypt.checkpw('testpassword'.encode('utf-8'), user.password.encode('utf-8'))

def test_create_user_failed(client):
    """
    Testa a criação de um novo usuário com falhas
    """
    response = client.post('/users', data=json.dumps({
        'username': 'testuser',
    }), content_type='application/json')

    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['error'] == 'Missing required fields'

def test_create_user_username_exists(client):
    """
    Testa a criação de um novo usuário com username já existente
    """
    response1 = client.post('/users', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

    assert response1.status_code == 201

    response2 = client.post('/users', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

    assert response2.status_code == 400
    data = json.loads(response2.data)
    assert data['error'] == 'Username already exists'