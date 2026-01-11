from flask import Blueprint, request, jsonify
from utils import generate_code
from email_service import send_email, send_reset_code_email
from db import get_db_cursor, execute_query
from datetime import datetime, timedelta


auth_bp = Blueprint('auth', __name__)  

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    try:
        with get_db_cursor() as (cursor, conn):
            # Check if email already exists
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({'error': 'Email already exists'}), 400

            # Insert new user
            cursor.execute(
                "INSERT INTO users (email, password) VALUES (%s, %s)",
                (email, password)
            )
            conn.commit()
            return jsonify({'message': 'Signup successful'}), 200
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
        # If it's a unique constraint violation, user already exists
        if 'unique' in str(e).lower() or 'duplicate' in str(e).lower():
            return jsonify({'error': 'Email already exists'}), 400
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    is_admin = data.get('admin', False)

    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    # Strip whitespace from email and normalize
    email = email.strip().lower() if email else email
    password = password.strip() if password else password

    # Debug: Log the received data (remove in production)
    print(f"Login attempt - Email: '{email}', Password length: {len(password) if password else 0}, Admin: {is_admin}")

    try:
        table = 'admins' if is_admin else 'users'
        with get_db_cursor() as (cursor, conn):
            # First check if user exists (case-insensitive email comparison)
            cursor.execute(f"SELECT email, password FROM {table} WHERE LOWER(email) = LOWER(%s)", (email,))
            user = cursor.fetchone()
            
            if not user:
                print(f"User not found in {table}: {email}")
                return jsonify({'error': 'Invalid credentials'}), 401
            
            # Check password match (exact match)
            stored_password = user[1]
            if stored_password != password:
                print(f"Password mismatch for {email}")
                print(f"  Stored password: '{stored_password}' (length: {len(stored_password)})")
                print(f"  Received password: '{password}' (length: {len(password)})")
                return jsonify({'error': 'Invalid credentials'}), 401
            
            print(f"Login successful for {email}")
            return jsonify({'message': 'Login successful'}), 200
    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Internal server error'}), 500
    
@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    # Strip whitespace from email
    email = email.strip().lower()

    print(f"Forgot password request for: {email}")

    try:
        # Check if user exists
        with get_db_cursor() as (cursor, conn):
            cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                print(f"User not found: {email}")
                # Don't reveal if email exists or not for security
                return jsonify({'message': 'Reset code sent to your email'}), 200

        code = generate_code()
        expires_at = datetime.now() + timedelta(minutes=15)  # Code expires in 15 minutes

        print(f"Generated reset code for {email}: {code}")

        with get_db_cursor() as (cursor, conn):
            # Delete old codes for this email
            cursor.execute("DELETE FROM reset_codes WHERE email = %s", (email,))
            # Insert new code
            cursor.execute(
                "INSERT INTO reset_codes (email, code, expires_at) VALUES (%s, %s, %s)",
                (email, code, expires_at)
            )
            conn.commit()
            print(f"Reset code saved to database")

        send_reset_code_email(email, code)
        print(f"Reset code email sent to {email}")
        return jsonify({'message': 'Reset code sent to your email'}), 200
    except Exception as e:
        print(f"Forgot password error: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    new_pass = data.get('new_password')

    if not email or not code or not new_pass:
        return jsonify({'error': 'Email, code, and new_password are required'}), 400

    # Strip whitespace
    email = email.strip().lower() if email else email
    code = code.strip() if code else code
    new_pass = new_pass.strip() if new_pass else new_pass

    print(f"Reset password request - Email: {email}, Code: {code}")

    try:
        with get_db_cursor() as (cursor, conn):
            # Verify code and check if it's not expired
            cursor.execute(
                "SELECT email, code, expires_at FROM reset_codes WHERE LOWER(email) = LOWER(%s) AND code = %s",
                (email, code)
            )
            reset_record = cursor.fetchone()

            if not reset_record:
                print(f"Reset code not found for {email} with code {code}")
                return jsonify({'error': 'Invalid code'}), 400

            # Check if code is expired
            expires_at = reset_record[2]
            if datetime.now() > expires_at:
                print(f"Reset code expired for {email}. Expires at: {expires_at}, Now: {datetime.now()}")
                cursor.execute("DELETE FROM reset_codes WHERE LOWER(email) = LOWER(%s)", (email,))
                conn.commit()
                return jsonify({'error': 'Code has expired'}), 400

            # Update password
            cursor.execute(
                "UPDATE users SET password = %s WHERE LOWER(email) = LOWER(%s)",
                (new_pass, email)
            )
            if cursor.rowcount == 0:
                print(f"User not found: {email}")
                return jsonify({'error': 'User not found'}), 404

            # Delete the used code
            cursor.execute("DELETE FROM reset_codes WHERE LOWER(email) = LOWER(%s)", (email,))
            conn.commit()

            print(f"Password reset successful for {email}")
            return jsonify({'message': 'Password reset successful'}), 200
    except Exception as e:
        print(f"Reset password error: {str(e)}")
        import traceback
        traceback.print_exc()
        if 'conn' in locals():
            conn.rollback()
        return jsonify({'error': 'Internal server error'}), 500