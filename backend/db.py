"""
Database connection and utility functions for PostgreSQL
"""
from dotenv import load_dotenv
load_dotenv()
import psycopg2
from psycopg2 import pool, extras
from psycopg2.extras import RealDictCursor
import os
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connection pool
connection_pool: Optional[pool.ThreadedConnectionPool] = None


def get_db_config():
    """Get database configuration from environment variables"""
    return {
        'host': os.getenv('DB_HOST', 'localhost'),
        'port': os.getenv('DB_PORT', '5432'),
        'database': os.getenv('DB_NAME', 'onlineshopping'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'postgres')
    }


def init_db_pool(min_conn=1, max_conn=10):
    """Initialize the connection pool"""
    global connection_pool
    try:
        config = get_db_config()
        connection_pool = pool.ThreadedConnectionPool(
            min_conn, max_conn,
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )
        logger.info("Database connection pool initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing connection pool: {e}")
        raise


def create_database_if_not_exists():
    """Create the database if it doesn't exist"""
    config = get_db_config()
    db_name = config['database']
    
    # Connect to postgres database to create our database
    config_temp = config.copy()
    config_temp['database'] = 'postgres'
    
    try:
        conn = psycopg2.connect(**config_temp)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (db_name,)
        )
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE {db_name}')
            logger.info(f"Database '{db_name}' created successfully")
        else:
            logger.info(f"Database '{db_name}' already exists")
        
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        # Continue anyway, database might already exist


@contextmanager
def get_db_connection():
    """Get a database connection from the pool"""
    if connection_pool is None:
        init_db_pool()
    
    conn = None
    try:
        conn = connection_pool.getconn()
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        logger.error(f"Database connection error: {e}")
        raise
    finally:
        if conn:
            connection_pool.putconn(conn)


@contextmanager
def get_db_cursor(dict_cursor=False):
    """Get a database cursor with optional dict cursor"""
    with get_db_connection() as conn:
        cursor_class = RealDictCursor if dict_cursor else None
        cursor = conn.cursor(cursor_factory=cursor_class)
        try:
            yield cursor, conn
        finally:
            cursor.close()


def execute_query(query: str, params: tuple = None, fetch: bool = False, fetch_one: bool = False):
    """Execute a query and optionally fetch results"""
    with get_db_cursor(dict_cursor=fetch) as (cursor, conn):
        cursor.execute(query, params)
        
        if fetch_one:
            result = cursor.fetchone()
            conn.commit()
            return dict(result) if result and fetch else result
        elif fetch:
            results = cursor.fetchall()
            conn.commit()
            return [dict(row) for row in results]
        else:
            conn.commit()
            return cursor.rowcount


def execute_transaction(queries: List[tuple]):
    """Execute multiple queries in a transaction"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            for query, params in queries:
                cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"Transaction error: {e}")
            raise


def close_db_pool():
    """Close all connections in the pool"""
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None
        logger.info("Database connection pool closed")
