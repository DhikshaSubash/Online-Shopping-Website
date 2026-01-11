# PostgreSQL Migration Complete

The backend has been successfully migrated from CSV-based storage to PostgreSQL.

## What Changed

- ✅ All CSV file operations replaced with PostgreSQL queries
- ✅ Proper relational database schema with foreign keys and indexes
- ✅ Connection pooling for better performance
- ✅ Automatic database initialization on first run
- ✅ CSV data automatically migrated to PostgreSQL
- ✅ All API endpoints maintain exact same response format
- ✅ Frontend requires **NO changes**

## Quick Start

### 1. Install PostgreSQL
- Download and install from https://www.postgresql.org/download/
- Default port: 5432
- Default user: postgres
- Set a password during installation

### 2. Configure Environment
Create a `.env` file in the `backend` directory:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=onlineshopping
DB_USER=postgres
DB_PASSWORD=your_postgres_password
```

### 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```

The application will automatically:
- Create the database if it doesn't exist
- Create all tables and schema
- Migrate existing CSV data

## File Structure

```
backend/
├── db.py              # Database connection and utilities
├── db_init.py         # Database initialization and migration
├── schema.sql         # PostgreSQL schema definition
├── seed.sql           # Seed data script (optional)
├── app.py             # Main Flask app (updated)
├── auth.py            # Authentication routes (updated)
├── user.py            # User routes (updated)
├── admin.py           # Admin routes (updated)
├── .env.example       # Environment variables template
└── POSTGRESQL_SETUP.md # Detailed setup instructions
```

## Database Schema

The database includes the following tables:
- **users** - User accounts
- **admins** - Admin accounts
- **products** - Product catalog
- **cart** - Shopping cart items
- **orders** - Order headers
- **order_items** - Order line items
- **reset_codes** - Password reset codes

All tables have proper:
- Primary keys
- Foreign keys with constraints
- Indexes for performance
- Timestamps for auditing

## API Compatibility

All API endpoints work exactly the same as before:

- `POST /auth/signup`
- `POST /auth/login`
- `POST /auth/forgot-password`
- `POST /auth/reset-password`
- `GET /user/products`
- `POST /user/cart`
- `GET /user/cart/<email>`
- `POST /user/place-order`
- `POST /user/cart/remove`
- `GET /user/orders/<email>`
- `GET /admin/users`
- `GET /admin/orders`
- `POST /admin/add-product`
- `GET /admin/products`
- `DELETE /admin/remove-product/<product_id>`

## CSV Files

- CSV files in `backend/data/` are **NOT deleted**
- They serve as backup and reference
- Data is automatically migrated on first run
- Future operations use PostgreSQL only

## Troubleshooting

### Connection Issues
1. Ensure PostgreSQL service is running
2. Verify credentials in `.env`
3. Check firewall settings

### Migration Issues
1. Delete the database and recreate: `DROP DATABASE onlineshopping;`
2. Run `python db_init.py` manually
3. Check logs for specific error messages

### Data Not Showing
1. Verify migration ran: Check if tables have data
2. Check CSV files exist in `backend/data/`
3. Verify database connection is working

## Performance Improvements

- **Connection Pooling**: Reuses database connections efficiently
- **Indexes**: Faster queries on email, product_id, order_id, etc.
- **Prepared Statements**: Protection against SQL injection
- **Transactions**: Ensures data consistency

## Production Notes

For production:
1. Use environment variables (never hardcode credentials)
2. Set up database backups
3. Configure SSL/TLS for database connections
4. Use a dedicated database user with limited privileges
5. Monitor connection pool usage
6. Set up database replication if needed

## Support

For detailed setup instructions, see `POSTGRESQL_SETUP.md`
