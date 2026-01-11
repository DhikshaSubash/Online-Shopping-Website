from flask import Blueprint, request, jsonify
import datetime
import random
from email_service import send_email
from db import get_db_cursor, execute_query

user_bp = Blueprint('user', __name__)

@user_bp.route('/products', methods=['GET'])
def get_products():
    query = request.args.get('search')
    
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            if query:
                cursor.execute(
                    "SELECT id AS ID, name, price, stock, image FROM products WHERE name ILIKE %s",
                    (f'%{query}%',)
                )
            else:
                cursor.execute("SELECT id AS ID, name, price, stock, image FROM products")
            
            products = cursor.fetchall()
            # Convert to list of dicts and ensure proper types
            result = []
            for row in products:
                result.append({
                    'ID': int(row['id']),
                    'name': row['name'],
                    'price': float(row['price']),
                    'stock': int(row['stock']),
                    'image': row['image']
                })
            return jsonify(result)
    except Exception as e:
        return jsonify([])

@user_bp.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    email = data.get('email')
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not email or product_id is None:
        return jsonify({'error': 'Email and product_id are required'}), 400

    try:
        with get_db_cursor() as (cursor, conn):
            # Check if item already exists in cart
            cursor.execute(
                "SELECT quantity FROM cart WHERE email = %s AND product_id = %s",
                (email, product_id)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update quantity
                new_quantity = existing[0] + quantity
                cursor.execute(
                    "UPDATE cart SET quantity = %s WHERE email = %s AND product_id = %s",
                    (new_quantity, email, product_id)
                )
            else:
                # Insert new item
                cursor.execute(
                    "INSERT INTO cart (email, product_id, quantity) VALUES (%s, %s, %s)",
                    (email, product_id, quantity)
                )
            conn.commit()
            return jsonify({'message': 'Added to cart'})
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/cart/<email>', methods=['GET'])
def get_cart(email):
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            cursor.execute(
                "SELECT email, product_id, quantity FROM cart WHERE email = %s",
                (email,)
            )
            cart_items = cursor.fetchall()
            
            result = []
            for row in cart_items:
                result.append({
                    'email': row['email'],
                    'product_id': int(row['product_id']),
                    'quantity': int(row['quantity'])
                })
            return jsonify(result)
    except Exception as e:
        return jsonify([])

@user_bp.route('/place-order', methods=['POST'])
def place_order():
    email = request.json.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    try:
        with get_db_cursor() as (cursor, conn):
            # Get user's cart items
            cursor.execute(
                "SELECT product_id, quantity FROM cart WHERE email = %s",
                (email,)
            )
            cart_items = cursor.fetchall()

            if not cart_items:
                return jsonify({'error': 'Cart is empty'}), 400

            total = 0
            order_items_data = []

            # Validate stock and calculate total
            for product_id, quantity in cart_items:
                cursor.execute(
                    "SELECT id, name, price, stock FROM products WHERE id = %s",
                    (product_id,)
                )
                product = cursor.fetchone()

                if not product:
                    conn.rollback()
                    return jsonify({'error': f'Product ID {product_id} not found'}), 400

                prod_id, prod_name, prod_price, prod_stock = product
                if quantity > prod_stock:
                    conn.rollback()
                    return jsonify({'error': f'Only {prod_stock} in stock for {prod_name}'}), 400

                item_total = float(prod_price) * quantity
                total += item_total
                order_items_data.append((prod_id, quantity, prod_price))

            # Generate order ID and date
            order_id = str(random.randint(10000, 99999))
            # Ensure unique order_id
            cursor.execute("SELECT order_id FROM orders WHERE order_id = %s", (order_id,))
            while cursor.fetchone():
                order_id = str(random.randint(10000, 99999))
                cursor.execute("SELECT order_id FROM orders WHERE order_id = %s", (order_id,))

            date = datetime.date.today().isoformat()

            # Create order
            cursor.execute(
                "INSERT INTO orders (order_id, email, amount, date) VALUES (%s, %s, %s, %s)",
                (order_id, email, total, date)
            )

            # Create order items and update stock
            for prod_id, quantity, price_at_purchase in order_items_data:
                # Insert order item
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (%s, %s, %s, %s)",
                    (order_id, prod_id, quantity, price_at_purchase)
                )
                
                # Update product stock
                cursor.execute(
                    "UPDATE products SET stock = stock - %s WHERE id = %s",
                    (quantity, prod_id)
                )

            # Clear user's cart
            cursor.execute("DELETE FROM cart WHERE email = %s", (email,))

            conn.commit()

            # Send email
            send_email(email, f"Order #{order_id} confirmed.\nTotal: ₹{total:.2f}\nDate: {date}")

            return jsonify({'message': 'Order placed', 'order_id': order_id})

    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    data = request.json
    email = data.get('email')
    product_id = data.get('product_id')

    if not email or product_id is None:
        return jsonify({'error': 'Email and product_id are required'}), 400

    try:
        with get_db_cursor() as (cursor, conn):
            cursor.execute(
                "DELETE FROM cart WHERE email = %s AND product_id = %s",
                (email, product_id)
            )
            conn.commit()
            return jsonify({'message': 'Item removed from cart'})
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@user_bp.route('/orders/<email>', methods=['GET'])
def get_user_orders(email):
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Get all orders for the user
            cursor.execute(
                "SELECT order_id, email, amount, date FROM orders WHERE email = %s ORDER BY date DESC",
                (email,)
            )
            orders = cursor.fetchall()

            result = []
            for order in orders:
                order_id = order['order_id']
                date = str(order['date'])
                amount = float(order['amount'])

                # Get order items from order_items table
                cursor.execute(
                    """SELECT oi.quantity, oi.price_at_purchase, p.name 
                       FROM order_items oi 
                       JOIN products p ON oi.product_id = p.id 
                       WHERE oi.order_id = %s""",
                    (order_id,)
                )
                order_items = cursor.fetchall()

                items = []
                for item in order_items:
                    quantity = int(item['quantity'])
                    price_at_purchase = float(item['price_at_purchase'])
                    items.append({
                        'name': item['name'],
                        'quantity': quantity,
                        'price': price_at_purchase * quantity
                    })

                result.append({
                    'order_id': order_id,
                    'date': date,
                    'amount': amount,
                    'items': items
                })

            return jsonify(result)
    except Exception as e:
        return jsonify([])
