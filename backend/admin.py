from flask import Blueprint, request, jsonify
import os
from datetime import datetime, timedelta
from db import get_db_cursor

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
def get_users():
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            cursor.execute("SELECT email, password FROM users")
            users = cursor.fetchall()
            result = [{'email': row['email'], 'password': row['password']} for row in users]
            return jsonify(result)
    except Exception as e:
        return jsonify([])

@admin_bp.route('/orders', methods=['GET'])
def get_orders():
    date = request.args.get('date')
    
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            if date:
                cursor.execute(
                    "SELECT order_id, email as user_email, amount as total_price, date FROM orders WHERE date = %s",
                    (date,)
                )
            else:
                cursor.execute(
                    "SELECT order_id, email as user_email, amount as total_price, date FROM orders"
                )
            
            orders = cursor.fetchall()
            result = []
            for row in orders:
                result.append({
                    'order_id': row['order_id'],
                    'user_email': row['user_email'],
                    'total_price': float(row['total_price']),
                    'date': str(row['date'])
                })
            return jsonify(result)
    except Exception as e:
        return jsonify([])


@admin_bp.route('/add-product', methods=['POST'])
def add_product():
    name = request.form.get('name')
    price = request.form.get('price')
    stock = request.form.get('stock')
    image = request.files.get('image')

    if not all([name, price, stock, image]):
        return jsonify({'error': 'Missing fields'}), 400

    filename = image.filename
    image_path = os.path.join('static', 'images', filename)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)
    image.save(image_path)

    try:
        with get_db_cursor() as (cursor, conn):
            # Get the next ID
            cursor.execute("SELECT COALESCE(MAX(id), 0) + 1 FROM products")
            new_id = cursor.fetchone()[0]

            # Insert new product
            cursor.execute(
                "INSERT INTO products (id, name, price, stock, image) VALUES (%s, %s, %s, %s, %s)",
                (new_id, name, float(price), int(stock), filename)
            )
            conn.commit()
            return jsonify({'message': 'Product added'}), 200
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500

@admin_bp.route('/products', methods=['GET'])
def get_products():
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            cursor.execute("SELECT id AS ID, name, price, stock, image FROM products")
            products = cursor.fetchall()
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

@admin_bp.route('/remove-product/<product_id>', methods=['DELETE'])
def remove_product(product_id):
    try:
        with get_db_cursor() as (cursor, conn):
            cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                return jsonify({'message': f'Product {product_id} removed'})
            else:
                return jsonify({'message': f'Product {product_id} not found'}), 404
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500


# ============= ANALYTICS ENDPOINTS =============

@admin_bp.route('/analytics/revenue', methods=['GET'])
def get_revenue_analytics():
    """Get revenue analytics - total, daily, weekly, monthly"""
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Total revenue
            cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM orders")
            total_revenue = float(cursor.fetchone()['total'] or 0)
            
            # Revenue per day (last 30 days)
            cursor.execute("""
                SELECT date, COALESCE(SUM(amount), 0) as revenue
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY date
                ORDER BY date
            """)
            daily_revenue = [{'date': str(row['date']), 'revenue': float(row['revenue'])} for row in cursor.fetchall()]
            
            # Revenue per week (last 12 weeks)
            cursor.execute("""
                SELECT 
                    DATE_TRUNC('week', date)::DATE as week,
                    COALESCE(SUM(amount), 0) as revenue
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '84 days'
                GROUP BY DATE_TRUNC('week', date)
                ORDER BY week
            """)
            weekly_revenue = [{'week': str(row['week']), 'revenue': float(row['revenue'])} for row in cursor.fetchall()]
            
            # Revenue per month (last 12 months)
            cursor.execute("""
                SELECT 
                    DATE_TRUNC('month', date)::DATE as month,
                    COALESCE(SUM(amount), 0) as revenue
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY DATE_TRUNC('month', date)
                ORDER BY month
            """)
            monthly_revenue = [{'month': str(row['month']), 'revenue': float(row['revenue'])} for row in cursor.fetchall()]
            
            return jsonify({
                'total_revenue': total_revenue,
                'daily_revenue': daily_revenue,
                'weekly_revenue': weekly_revenue,
                'monthly_revenue': monthly_revenue
            })
    except Exception as e:
        print(f"Revenue analytics error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/analytics/orders', methods=['GET'])
def get_orders_analytics():
    """Get orders analytics - total, daily orders"""
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Total orders
            cursor.execute("SELECT COUNT(*) as total FROM orders")
            total_orders = int(cursor.fetchone()['total'])
            
            # Orders per day (last 30 days)
            cursor.execute("""
                SELECT date, COUNT(*) as order_count
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY date
                ORDER BY date
            """)
            daily_orders = [{'date': str(row['date']), 'count': int(row['order_count'])} for row in cursor.fetchall()]
            
            return jsonify({
                'total_orders': total_orders,
                'daily_orders': daily_orders
            })
    except Exception as e:
        print(f"Orders analytics error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/analytics/products', methods=['GET'])
def get_product_analytics():
    """Get product analytics - top selling, least selling, distribution"""
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Top selling products (by quantity sold)
            cursor.execute("""
                SELECT 
                    p.id,
                    p.name,
                    COALESCE(SUM(oi.quantity), 0) as total_sold,
                    COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) as total_revenue
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                GROUP BY p.id, p.name
                ORDER BY total_sold DESC
                LIMIT 10
            """)
            top_products = [{
                'id': int(row['id']),
                'name': row['name'],
                'total_sold': int(row['total_sold']),
                'total_revenue': float(row['total_revenue'])
            } for row in cursor.fetchall()]
            
            # Least selling products
            cursor.execute("""
                SELECT 
                    p.id,
                    p.name,
                    COALESCE(SUM(oi.quantity), 0) as total_sold
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                GROUP BY p.id, p.name
                ORDER BY total_sold ASC, p.name
                LIMIT 10
            """)
            least_products = [{
                'id': int(row['id']),
                'name': row['name'],
                'total_sold': int(row['total_sold'])
            } for row in cursor.fetchall()]
            
            # Product distribution (for pie chart - top 10 products by revenue)
            cursor.execute("""
                SELECT 
                    p.name,
                    COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) as revenue
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                GROUP BY p.id, p.name
                ORDER BY revenue DESC
                LIMIT 10
            """)
            product_distribution = [{
                'name': row['name'],
                'revenue': float(row['revenue'])
            } for row in cursor.fetchall()]
            
            return jsonify({
                'top_products': top_products,
                'least_products': least_products,
                'product_distribution': product_distribution
            })
    except Exception as e:
        print(f"Product analytics error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/analytics/customers', methods=['GET'])
def get_customer_analytics():
    """Get customer analytics - total users, new users per month, repeat vs new"""
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Total users
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = int(cursor.fetchone()['total'])
            
            # New users per month (last 12 months)
            cursor.execute("""
                SELECT 
                    DATE_TRUNC('month', created_at)::DATE as month,
                    COUNT(*) as new_users
                FROM users
                WHERE created_at >= CURRENT_DATE - INTERVAL '12 months'
                GROUP BY DATE_TRUNC('month', created_at)
                ORDER BY month
            """)
            monthly_new_users = [{'month': str(row['month']), 'count': int(row['new_users'])} for row in cursor.fetchall()]
            
            # Repeat vs New customers
            cursor.execute("""
                SELECT 
                    CASE 
                        WHEN order_count > 1 THEN 'Repeat Customers'
                        WHEN order_count = 1 THEN 'Single Order Customers'
                        ELSE 'No Orders'
                    END as customer_type,
                    COUNT(*) as count
                FROM (
                    SELECT u.email, COALESCE(COUNT(o.order_id), 0) as order_count
                    FROM users u
                    LEFT JOIN orders o ON u.email = o.email
                    GROUP BY u.email
                ) as user_orders
                GROUP BY customer_type
            """)
            
            customer_types = {row['customer_type']: int(row['count']) for row in cursor.fetchall()}
            
            # Count users who placed orders
            cursor.execute("SELECT COUNT(DISTINCT email) as count FROM orders")
            users_with_orders = int(cursor.fetchone()['count'] or 0)
            
            return jsonify({
                'total_users': total_users,
                'monthly_new_users': monthly_new_users,
                'customer_types': customer_types,
                'users_with_orders': users_with_orders
            })
    except Exception as e:
        print(f"Customer analytics error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/analytics/conversion', methods=['GET'])
def get_conversion_metrics():
    """Get conversion metrics - users vs customers, conversion rate"""
    try:
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Total users
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = int(cursor.fetchone()['total'])
            
            # Users who placed orders
            cursor.execute("SELECT COUNT(DISTINCT email) as count FROM orders")
            users_with_orders = int(cursor.fetchone()['count'] or 0)
            
            # Calculate conversion rate
            conversion_rate = (users_with_orders / total_users * 100) if total_users > 0 else 0
            
            return jsonify({
                'total_users': total_users,
                'users_with_orders': users_with_orders,
                'users_without_orders': total_users - users_with_orders,
                'conversion_rate': round(conversion_rate, 2)
            })
    except Exception as e:
        print(f"Conversion metrics error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@admin_bp.route('/analytics/overview', methods=['GET'])
def get_analytics_overview():
    """Get all analytics data in one call - optimized single query approach"""
    try:
        # Get all data with efficient queries
        with get_db_cursor(dict_cursor=True) as (cursor, conn):
            # Revenue
            cursor.execute("SELECT COALESCE(SUM(amount), 0) as total FROM orders")
            total_revenue = float(cursor.fetchone()['total'] or 0)
            
            cursor.execute("""
                SELECT date, COALESCE(SUM(amount), 0) as revenue
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY date
                ORDER BY date
            """)
            daily_revenue = [{'date': str(row['date']), 'revenue': float(row['revenue'])} for row in cursor.fetchall()]
            
            # Orders
            cursor.execute("SELECT COUNT(*) as total FROM orders")
            total_orders = int(cursor.fetchone()['total'])
            
            cursor.execute("""
                SELECT date, COUNT(*) as order_count
                FROM orders
                WHERE date >= CURRENT_DATE - INTERVAL '30 days'
                GROUP BY date
                ORDER BY date
            """)
            daily_orders = [{'date': str(row['date']), 'count': int(row['order_count'])} for row in cursor.fetchall()]
            
            # Products
            cursor.execute("""
                SELECT 
                    p.id, p.name,
                    COALESCE(SUM(oi.quantity), 0) as total_sold,
                    COALESCE(SUM(oi.quantity * oi.price_at_purchase), 0) as total_revenue
                FROM products p
                LEFT JOIN order_items oi ON p.id = oi.product_id
                GROUP BY p.id, p.name
                ORDER BY total_sold DESC
                LIMIT 10
            """)
            top_products = [{
                'id': int(row['id']),
                'name': row['name'],
                'total_sold': int(row['total_sold']),
                'total_revenue': float(row['total_revenue'])
            } for row in cursor.fetchall()]
            
            # Customers
            cursor.execute("SELECT COUNT(*) as total FROM users")
            total_users = int(cursor.fetchone()['total'])
            
            cursor.execute("SELECT COUNT(DISTINCT email) as count FROM orders")
            users_with_orders = int(cursor.fetchone()['count'] or 0)
            
            conversion_rate = (users_with_orders / total_users * 100) if total_users > 0 else 0
            
            return jsonify({
                'revenue': {
                    'total_revenue': total_revenue,
                    'daily_revenue': daily_revenue
                },
                'orders': {
                    'total_orders': total_orders,
                    'daily_orders': daily_orders
                },
                'products': {
                    'top_products': top_products
                },
                'customers': {
                    'total_users': total_users,
                    'users_with_orders': users_with_orders
                },
                'conversion': {
                    'total_users': total_users,
                    'users_with_orders': users_with_orders,
                    'conversion_rate': round(conversion_rate, 2)
                }
            })
    except Exception as e:
        print(f"Analytics overview error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500
