-- Seed data script for PostgreSQL
-- This script can be used to manually seed the database if needed
-- Note: db_init.py handles automatic migration from CSV files

-- Clear existing data (use with caution!)
-- TRUNCATE TABLE reset_codes CASCADE;
-- TRUNCATE TABLE order_items CASCADE;
-- TRUNCATE TABLE orders CASCADE;
-- TRUNCATE TABLE cart CASCADE;
-- TRUNCATE TABLE products CASCADE;
-- TRUNCATE TABLE admins CASCADE;
-- TRUNCATE TABLE users CASCADE;

-- Example seed data (actual data should come from CSV migration via db_init.py)
-- Users
-- INSERT INTO users (email, password) VALUES
-- ('test@example.com', 'password123')
-- ON CONFLICT (email) DO NOTHING;

-- Admins
-- INSERT INTO admins (email, password) VALUES
-- ('admin@hexcart.com', 'Hex@1234')
-- ON CONFLICT (email) DO NOTHING;

-- Products
-- INSERT INTO products (id, name, price, stock, image) VALUES
-- (1, 'Wireless Mouse', 499.99, 13, 'wireless_mouse.jpg')
-- ON CONFLICT (id) DO NOTHING;

-- Note: Run db_init.py to automatically migrate all CSV data to PostgreSQL
