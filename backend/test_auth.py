"""Test script to debug authentication issues"""
from db import get_db_cursor

# Test 1: Check if users exist and their passwords
print("=" * 50)
print("Test 1: Checking users in database")
print("=" * 50)
with get_db_cursor() as (cursor, conn):
    cursor.execute("SELECT email, password FROM users LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Email: {row[0]}")
        print(f"Password: '{row[1]}' (length: {len(row[1])})")
        print()

# Test 2: Try to match a specific user
print("=" * 50)
print("Test 2: Testing login match")
print("=" * 50)
test_email = "dhikshasubash22@gmail.com"
test_password = "dhik1234"

with get_db_cursor() as (cursor, conn):
    cursor.execute("SELECT email, password FROM users WHERE email = %s", (test_email,))
    row = cursor.fetchone()
    
    if row:
        print(f"User found: {row[0]}")
        print(f"Stored password: '{row[1]}'")
        print(f"Test password: '{test_password}'")
        print(f"Exact match: {row[1] == test_password}")
        print(f"Stored password type: {type(row[1])}")
        print(f"Test password type: {type(test_password)}")
        
        # Test the query that login uses
        cursor.execute(
            "SELECT email FROM users WHERE email = %s AND password = %s",
            (test_email, test_password)
        )
        match = cursor.fetchone()
        print(f"Query match result: {match is not None}")
        if match:
            print(f"Match email: {match[0]}")
    else:
        print(f"User {test_email} not found!")

# Test 3: Check admin
print("=" * 50)
print("Test 3: Checking admin account")
print("=" * 50)
with get_db_cursor() as (cursor, conn):
    cursor.execute("SELECT email, password FROM admins")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Admin Email: {row[0]}")
        print(f"Admin Password: '{row[1]}'")
        print()
