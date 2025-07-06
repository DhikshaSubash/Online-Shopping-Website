from flask import Blueprint, request, jsonify
from utils.csv_handler import read_csv, append_csv
import os

auth_bp = Blueprint('auth', __name__)
USERS_CSV = os.path.join('data', 'users.csv')
ADMINS_CSV = os.path.join('data', 'admin.csv')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    users = read_csv(USERS_CSV)
    if any(u['email'] == data['email'] for u in users):
        return jsonify({"error": "User already exists"}), 400
    append_csv(USERS_CSV, data, fieldnames=["email", "password"])
    return jsonify({"message": "Signup successful"}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    users = read_csv(USERS_CSV)
    for user in users:
        if user['email'] == data['email'] and user['password'] == data['password']:
            return jsonify({"message": "Login successful"}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@auth_bp.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json
    admins = read_csv(ADMINS_CSV)
    for admin in admins:
        if admin['email'] == data['email'] and admin['password'] == data['password']:
            return jsonify({"message": "Admin login successful"}), 200
    return jsonify({"error": "Invalid admin credentials"}), 401
