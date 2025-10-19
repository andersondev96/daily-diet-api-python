import pytest
import json
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app import app, db

# Helpers
def create_user(client, username, password):
    """Cria um usuário via API"""
    client.post(
        '/users',
        data=json.dumps({'username': username, 'password': password}),
        content_type='application/json'
    )

def login_user(client, username, password):
    """Faz login de um usuário via API, mantendo sessão"""
    client.post(
        '/login',
        data=json.dumps({'username': username, 'password': password}),
        content_type='application/json'
    )

def logout_user(client):
    """Faz logout de um usuário via API"""
    client.get('/logout')

# Fixtures
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

@pytest.fixture
def default_user(client):
    """Cria e loga um usuário padrão"""
    create_user(client, 'testuser', 'testpassword')
    login_user(client, 'testuser', 'testpassword')
    return {'username': 'testuser', 'password': 'testpassword'}

# Tests
def test_get_meal_success(client, default_user):
    """Testa a obtenção de uma refeição existente com sucesso"""
    with client:
        # Criação da refeição
        meal = client.post("/meals", data=json.dumps({
            'name': "Café da manhã",
            'description': "Pão integral e café preto",
            'datetime': "2025-10-05T08:30:00",
            'isInDiet': True
        }), content_type='application/json')

        meal_id = meal.json['meal']['id']

        # Obtenção da refeição
        response = client.get(f"/meal/{meal_id}")
        assert response.status_code == 200
        assert response.json['name'] == "Café da manhã"
        assert response.json['user_id'] == 1

def test_get_meal_unauthorized(client):
    """Testa a obtenção de uma refeição sem login"""
    with client:
        response = client.get("/meal/1")
        assert response.status_code == 401
        assert response.json['error'] == "Unauthorized access"

def test_get_meal_user_not_authorized(client):
    """Testa a obtenção de uma refeição com usuário não autorizado"""
    with client:
        # Criação de dois usuários
        create_user(client, 'user1', 'pass1')
        create_user(client, 'user2', 'pass2')

        # User1 cria a refeição
        login_user(client, 'user1', 'pass1')
        meal = client.post("/meals", data=json.dumps({
            'name': "Almoço",
            'description': "Arroz e feijão",
            'datetime': "2025-10-05T12:00:00",
            'isInDiet': True
        }), content_type='application/json')
        meal_id = meal.json['meal']['id']

        # Logout user1
        logout_user(client)

        # User2 tenta acessar a refeição de user1
        login_user(client, 'user2', 'pass2')
        response = client.get(f"/meal/{meal_id}")
        assert response.status_code == 403
        assert response.json['error'] == "Unauthorized"

def test_get_meal_not_found(client):
    """Testa a obtenção de uma refeição que não existe"""
    with client:
        create_user(client, 'testuser', 'testpassword')
        login_user(client, 'testuser', 'testpassword')

        response = client.get("/meal/999")
        assert response.status_code == 404
        assert response.json['error'] == "Meal not found"
