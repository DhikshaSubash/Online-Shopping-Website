"""
Database initialization script
Creates tables and migrates data from CSV if needed
"""
import psycopg2
import psycopg2.extensions
import pandas as pd
import os
import logging
from db import get_db_config
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_schema():
    """Initialize database schema by reading schema.sql"""
    schema_path = Path(__file__).parent / 'schema.sql'
    
    if not schema_path.exists():
        logger.error("schema.sql not found!")
        return False
    
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    
    config = get_db_config()
    
    try:
        conn = psycopg2.connect(**config)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Execute SQL script statement by statement
        # Split by semicolon, but handle functions and triggers carefully
        statements = []
        current_statement = []
        in_function = False
        dollar_quote_count = 0
        
        lines = schema_sql.split('\n')
        for line in lines:
            # Skip comment lines
            if line.strip().startswith('--'):
                continue
            
            current_statement.append(line)
            
            # Check for function definitions (using $$ delimiters)
            dollar_quotes = line.count('$$')
            dollar_quote_count += dollar_quotes
            
            # If we have an even number of $$, we're not in a function
            if dollar_quote_count % 2 == 0:
                in_function = False
                # Check if line ends a statement
                if line.strip().endswith(';') and not in_function:
                    stmt = '\n'.join(current_statement).strip()
                    if stmt:
                        statements.append(stmt)
                    current_statement = []
            else:
                in_function = True
        
        # Execute each statement
        for stmt in statements:
            try:
                cursor.execute(stmt)
            except psycopg2.Error as e:
                # Ignore "already exists" errors (expected on subsequent runs)
                error_msg = str(e).lower()
                if 'already exists' not in error_msg and 'duplicate' not in error_msg:
                    # Log but continue - some statements might fail if dependencies exist
                    logger.debug(f"Schema statement note: {e}")
        
        cursor.close()
        conn.close()
        
        logger.info("Database schema initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error creating schema: {e}")
        if 'conn' in locals():
            conn.close()
        return False


def migrate_csv_data():
    """Migrate data from CSV files to PostgreSQL"""
    data_dir = Path(__file__).parent / 'data'
    config = get_db_config()
    
    try:
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count > 0:
            logger.info("Data already exists in database. Skipping migration.")
            cursor.close()
            conn.close()
            return True
        
        # Migrate users
        users_csv = data_dir / 'users.csv'
        if users_csv.exists():
            df = pd.read_csv(users_csv)
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO users (email, password) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                    (row['email'], row['password'])
                )
            logger.info(f"Migrated {len(df)} users")
        
        # Migrate admins
        admin_csv = data_dir / 'admin.csv'
        if admin_csv.exists():
            df = pd.read_csv(admin_csv)
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO admins (email, password) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
                    (row['email'], row['password'])
                )
            logger.info(f"Migrated {len(df)} admins")
        
        # Migrate products
        products_csv = data_dir / 'products.csv'
        if products_csv.exists():
            df = pd.read_csv(products_csv)
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO products (id, name, price, stock, image) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (id) DO NOTHING",
                    (int(row['ID']), row['name'], float(row['price']), int(row['stock']), row['image'])
                )
            logger.info(f"Migrated {len(df)} products")
        
        # Migrate orders
        orders_csv = data_dir / 'orders.csv'
        if orders_csv.exists():
            df = pd.read_csv(orders_csv)
            for _, row in df.iterrows():
                cursor.execute(
                    "INSERT INTO orders (order_id, email, amount, date) VALUES (%s, %s, %s, %s) ON CONFLICT (order_id) DO NOTHING",
                    (str(row['order_id']), row['email'], float(row['amount']), row['date'])
                )
            logger.info(f"Migrated {len(df)} orders")
        
        # Note: Cart is not migrated as it's typically session-specific
        # Orders don't have order_items in CSV, so we skip that
        
        conn.commit()
        cursor.close()
        conn.close()
        
        logger.info("CSV data migration completed successfully")
        return True
        
    except Exception as e:
        logger.error(f"Error migrating data: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False


if __name__ == '__main__':
    from db import create_database_if_not_exists
    
    logger.info("Initializing database...")
    create_database_if_not_exists()
    
    logger.info("Creating schema...")
    if init_schema():
        logger.info("Migrating CSV data...")
        migrate_csv_data()
    else:
        logger.error("Schema creation failed. Aborting migration.")
