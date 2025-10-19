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

def test_login_success(client):
    """
    Testa o login de usuário com sucesso.
    """
    client.post('/users', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

    response = client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'

    user = User.query.filter_by(username='testuser').first()

    assert user is not None
    assert user.password != 'testpassword'
    assert bcrypt.checkpw('testpassword'.encode('utf-8'), user.password.encode('utf-8'))

def test_login_missing_fields(client):
  """
  Testa o login com campos ausentes.
  """
  response = client.post('/login', data=json.dumps({}), content_type='application/json')

  assert response.status_code == 400
  assert response.json['error'] == 'Missing JSON body'

def test_login_invalid_credentials(client):
  """
  Testa o login com credenciais inválidas.
  """
  response = client.post('/login', data=json.dumps({
    'username': 'testuser',
    'password': 'invalidpassword'
  }), content_type='application/json')

  assert response.status_code == 401
  assert response.json['error'] == 'Invalid credentials'

def test_logout_success(client):
  """
  Testa o logout de usuário com sucesso.
  """
  client.post('/users', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')

  client.post('/login', data=json.dumps({
        'username': 'testuser',
        'password': 'testpassword'
    }), content_type='application/json')
  
  response = client.get('/logout')

  assert response.status_code == 200
  assert response.json['message'] == 'Logged out successfully'

def test_logout_without_login(client):
  """
  Testa o logout sem estar logado.
  """
  response = client.get('/logout')

  assert response.status_code == 401
  assert response.json['error'] == 'Unauthorized access'

