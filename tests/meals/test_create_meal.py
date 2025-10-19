import pytest
import json
import sys
import os

# Adiciona a raiz do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from app import app, db
from models.meal import Meal

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

def test_create_meal(client):
    """
    Testa a criação de uma refeição.
    """
    client.post('/users', data=json.dumps({
      'username': 'testuser',
      'password': 'testpassword'
  }), content_type='application/json')

    client.post('/login', data=json.dumps({
          'username': 'testuser',
          'password': 'testpassword'
      }), content_type='application/json')

    response = client.post("/meals", data=json.dumps({
        'name':"Café da manhã",
        'description':"Pão integral e café preto",
        'datetime':"2025-10-05T08:30:00",
        'isInDiet':True
    }), content_type='application/json')

    assert response.status_code == 201
    
    meal = Meal.query.first()
    assert meal is not None

    data = json.loads(response.data)
    assert data['message'] == 'Meal created'
    assert data['meal']['name'] == 'Café da manhã'
    assert data['meal']['user_id'] == 1