from flask import Blueprint, request, jsonify
from utils.csv_handler import read_csv, write_csv, append_csv
import os
import datetime
import uuid
import ast

user_bp = Blueprint('user', __name__)
PRODUCTS_CSV = os.path.join('data', 'products.csv')
CART_CSV = os.path.join('data', 'cart.csv')
ORDERS_CSV = os.path.join('data', 'orders.csv')

@user_bp.route('/cart', methods=['GET'])
def view_cart():
    email = request.args.get("email")
    cart = read_csv(CART_CSV)
    return jsonify([item for item in cart if item['user_email'] == email])

@user_bp.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    data = request.json
    cart = read_csv(CART_CSV)
    # Remove existing entry if exists
    cart = [item for item in cart if not (item['user_email'] == data['user_email'] and item['product_id'] == data['product_id'])]
    cart.append(data)
    write_csv(CART_CSV, cart, fieldnames=["user_email", "product_id", "quantity"])
    return jsonify({"message": "Item added to cart"})

@user_bp.route('/place-order', methods=['POST'])
def place_order():
    data = request.json  # expects {"user_email": "xyz@example.com"}
    cart = read_csv(CART_CSV)
    products = read_csv(PRODUCTS_CSV)
    user_cart = [item for item in cart if item['user_email'] == data['user_email']]

    total = 0
    order_items = []

    # For storing product_id -> quantity for order file
    item_map = {}

    for item in user_cart:
        prod = next((p for p in products if p['id'] == item['product_id']), None)
        if not prod:
            return jsonify({"error": f"Product ID {item['product_id']} not found"}), 400
        if int(prod['stock']) < int(item['quantity']):
            return jsonify({"error": f"Only {prod['stock']} of {prod['name']} left"}), 400

        quantity = int(item['quantity'])
        total += float(prod['price']) * quantity
        order_items.append((prod, quantity))
        item_map[item['product_id']] = quantity

    # Update product stock
    for prod, qty in order_items:
        prod['stock'] = str(int(prod['stock']) - qty)
    write_csv(PRODUCTS_CSV, products, fieldnames=["id", "name", "price", "stock"])

    # Save order with item mapping as string
    order_id = str(uuid.uuid4())
    append_csv(ORDERS_CSV, {
        "order_id": order_id,
        "user_email": data['user_email'],
        "total_price": f"{total:.2f}",
        "date": datetime.date.today().isoformat(),
        "items": str(item_map)
    }, fieldnames=["order_id", "user_email", "total_price", "date", "items"])

    # Clear user's cart
    cart = [item for item in cart if item['user_email'] != data['user_email']]
    write_csv(CART_CSV, cart, fieldnames=["user_email", "product_id", "quantity"])

    return jsonify({"message": "Order placed", "order_id": order_id})


@user_bp.route('/latest-order/<user_email>', methods=['GET'])
def latest_order(user_email):
    orders = read_csv(ORDERS_CSV)
    products = read_csv(PRODUCTS_CSV)

    # Filter orders for the user
    user_orders = [o for o in orders if o['user_email'] == user_email]
    if not user_orders:
        return jsonify({"error": "No orders found"}), 404

    # Sort by date descending
    user_orders.sort(key=lambda x: x['date'], reverse=True)
    latest = user_orders[0]

    try:
        item_map = ast.literal_eval(latest['items'])  # e.g., {"1": 2, "3": 1}
    except:
        item_map = {}

    id_to_product = {p['id']: p for p in products}
    items = []

    for pid, qty in item_map.items():
        product = id_to_product.get(pid)
        if product:
            items.append({
                'name': product['name'],
                'price': float(product['price']),
                'quantity': int(qty)
            })

    return jsonify({
        'order_id': latest['order_id'],
        'date': latest['date'],
        'total_price': float(latest['total_price']),
        'items': items
    })
