import pytest
import json
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

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