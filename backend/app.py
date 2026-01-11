from flask import Flask, send_from_directory
from flask_cors import CORS
from auth import auth_bp
from admin import admin_bp
from user import user_bp
import os
from dotenv import load_dotenv
from db import init_db_pool, create_database_if_not_exists
from db_init import init_schema, migrate_csv_data

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/static/images/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

@app.route('/')
def home():
    return {"message": "Backend is running!"}

def initialize_database():
    """Initialize database on application startup"""
    try:
        # Create database if it doesn't exist
        create_database_if_not_exists()
        
        # Initialize connection pool
        init_db_pool()
        
        # Create schema if needed
        init_schema()
        
        # Migrate CSV data if needed
        migrate_csv_data()
        
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        print("Application will continue, but database operations may fail.")

# Initialize database when app starts
initialize_database()

if __name__ == '__main__':
    app.run(debug=True)
