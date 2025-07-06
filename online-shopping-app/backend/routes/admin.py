from flask import Blueprint, request, jsonify
from utils.csv_handler import read_csv, write_csv, append_csv
import os
import datetime

admin_bp = Blueprint('admin', __name__)
USERS_CSV = os.path.join('data', 'users.csv')
ORDERS_CSV = os.path.join('data', 'orders.csv')
PRODUCTS_CSV = os.path.join('data', 'products.csv')


@admin_bp.route('/users', methods=['GET'])
def get_users():
    users = read_csv(USERS_CSV)
    return jsonify(users)

@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    from_date = request.args.get("from")
    to_date = request.args.get("to")
    orders = read_csv(ORDERS_CSV)
    
    if from_date and to_date:
        from_dt = datetime.datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.datetime.strptime(to_date, "%Y-%m-%d")
        orders = [
            o for o in orders
            if from_dt <= datetime.datetime.strptime(o['date'], "%Y-%m-%d") <= to_dt
        ]
    return jsonify(orders)

@admin_bp.route('/add-product', methods=['POST'])
def add_product():
    data = request.json
    products = read_csv(PRODUCTS_CSV)
    product_ids = [int(p['id']) for p in products] if products else [0]
    new_id = str(max(product_ids) + 1 if product_ids else 1)
    
    data['id'] = new_id
    append_csv(PRODUCTS_CSV, data, fieldnames=['id', 'name', 'price', 'stock'])
    return jsonify({"message": "Product added", "id": new_id})

@admin_bp.route('/remove-product/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    products = read_csv(PRODUCTS_CSV)
    updated = [p for p in products if p['id'] != product_id]
    if len(products) == len(updated):
        return jsonify({"error": "Product not found"}), 404
    write_csv(PRODUCTS_CSV, updated, fieldnames=['id', 'name', 'price', 'stock'])
    return jsonify({"message": "Product removed"})
