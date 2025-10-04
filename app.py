from flask import Flask, request, jsonify
from flask_migrate import Migrate
from database import db
from models.meal import Meal
from models.user import User
from datetime import datetime
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
  return jsonify({"error": "Unauthorized access"}), 401

migrate = Migrate(app, db)

@app.route('/users', methods=["POST"])
def create_user():
  data = request.get_json()
  username = data.get('username')
  password = data.get('password')

  if not username or not password:
    return jsonify({"error": "Missing required fields"}), 400
  
  existing_user = User.query.filter_by(username=username).first()
  if existing_user:
    return jsonify({"error": "Username already exists"}), 400
  
  hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
  user = User(username=username, password=hashed_password)
  db.session.add(user)
  db.session.commit()

  return jsonify({"message": "User created", "user": {
    "id": user.id,
    "username": user.username
  }}), 201

@app.route('/login', methods=["POST"])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
      login_user(user)
      return jsonify({"message": "Login successful"})
  
  return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout', methods=["GET"])
@login_required
def logout():
  logout_user()
  return jsonify({"message": "Logged out successfully"}), 200

@app.route('/meals', methods=["POST"])
@login_required
def create_meal():
  data = request.get_json()
  name = data.get('name')
  description = data.get('description')
  datetime_value = data.get('datetime')
  isInDiet = data.get('isInDiet')
  userId = current_user.id

  if not name or not description or not userId or isInDiet is None:
    return jsonify({"error": "Missing required fields"}), 400
  
  if datetime_value:
    meal_datatetime = datetime.fromisoformat(datetime_value)
    meal= Meal(name=name, description=description, datetime=meal_datatetime, isInDiet=isInDiet, user_id=userId)
  else:
    meal= Meal(name=name, description=description, isInDiet=isInDiet, user_id=userId)
  
  db.session.add(meal)
  db.session.commit()
  return jsonify({"message": "Meal created", "meal": meal.to_dict()}), 201

@app.route('/meal/<int:id_meal>', methods=["GET"])
@login_required
def get_meal(id_meal):
  meal = Meal.query.get(id_meal)

  if meal and meal.user_id != current_user.id:
    return jsonify({"error": "Unauthorized"}), 403

  if meal:
    return jsonify(meal.to_dict()), 200
  
  return jsonify({"error": "Meal not found"}), 404

@app.route('/meals', methods=["GET"])
@login_required
def list_meals():
  meals = Meal.query.filter_by(user_id=current_user.id)
  meals_list = [meal.to_dict() for meal in meals]

  return jsonify(meals_list), 200

@app.route('/meal/<int:id_meal>', methods=["PUT"])
@login_required
def update_meal(id_meal):
  meal = Meal.query.get(id_meal)

  if not meal:
    return jsonify({"error": "Meal not found"}), 404
  
  if meal.user_id != current_user.id:
    return jsonify({"error": "Unauthorized"}), 403
  
  data = request.json
  meal.name = data.get('name')
  meal.description = data.get('description')
  if 'datetime' in data:
    meal.datetime = datetime.fromisoformat(data.get('datetime'))
  meal.isDiet = data.get('isDiet')
  db.session.commit()

  return jsonify({"message": "Meal updated", "meal": meal.to_dict()}), 200

@app.route('/meal/<int:id_meal>', methods=["DELETE"])
@login_required
def delete_meal(id_meal):
  meal = Meal.query.get(id_meal)

  if not meal:
    return jsonify({"error": "Meal not found"}), 404
  
  if meal.user_id != current_user.id:
    return jsonify({"error": "Unauthorized"}), 403
  
  db.session.delete(meal)
  db.session.commit()

  return jsonify({"message": "Meal deleted"}), 200

if __name__ == '__main__':
  app.run(debug=True)
