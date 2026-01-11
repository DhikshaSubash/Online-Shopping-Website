# PostgreSQL Setup Instructions

This guide will help you set up PostgreSQL for the Online Shopping Website backend.

## Prerequisites

1. **Install PostgreSQL**
   - **Windows**: Download from [PostgreSQL Official Website](https://www.postgresql.org/download/windows/)
   - **macOS**: `brew install postgresql` or download from the official website
   - **Linux**: `sudo apt-get install postgresql postgresql-contrib` (Ubuntu/Debian)

2. **Verify Installation**
   ```bash
   psql --version
   ```

## Database Setup

### Step 1: Start PostgreSQL Service

- **Windows**: PostgreSQL should start automatically, or start from Services
- **macOS**: `brew services start postgresql`
- **Linux**: `sudo systemctl start postgresql`

### Step 2: Create Database User (if needed)

1. Open PostgreSQL command line:
   ```bash
   psql -U postgres
   ```

2. (Optional) Create a new user:
   ```sql
   CREATE USER your_username WITH PASSWORD 'your_password';
   ALTER USER your_username CREATEDB;
   ```

### Step 3: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your PostgreSQL credentials:
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=onlineshopping
   DB_USER=postgres
   DB_PASSWORD=your_postgres_password
   ```

### Step 4: Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 5: Initialize Database

The application will automatically:
- Create the database if it doesn't exist
- Create all tables and schema
- Migrate existing CSV data to PostgreSQL

Just start the Flask application:

```bash
python app.py
```

**OR** manually run the initialization script:

```bash
python db_init.py
```

## Manual Database Setup (Alternative)

If you prefer to set up the database manually:

1. Create the database:
   ```sql
   psql -U postgres
   CREATE DATABASE onlineshopping;
   \q
   ```

2. Run the schema:
   ```bash
   psql -U postgres -d onlineshopping -f schema.sql
   ```

3. Migrate data:
   ```bash
   python db_init.py
   ```

## Verifying Installation

1. Connect to the database:
   ```bash
   psql -U postgres -d onlineshopping
   ```

2. Check tables:
   ```sql
   \dt
   ```

3. Check data:
   ```sql
   SELECT COUNT(*) FROM users;
   SELECT COUNT(*) FROM products;
   SELECT COUNT(*) FROM orders;
   ```

## Troubleshooting

### Connection Refused
- Ensure PostgreSQL service is running
- Check that the port (default 5432) is correct in `.env`
- Verify firewall settings allow connections

### Authentication Failed
- Verify username and password in `.env`
- Check `pg_hba.conf` for authentication settings
- Try connecting manually: `psql -U postgres -d postgres`

### Database Already Exists
- The application will handle this automatically
- Or drop and recreate: `DROP DATABASE onlineshopping;`

### Permission Denied
- Ensure the database user has CREATE DATABASE privileges
- Or create the database manually as shown in the manual setup section

## Data Migration Notes

- All existing CSV data will be automatically migrated on first run
- CSV files are **NOT deleted** - they remain in `backend/data/` as backup
- The migration is idempotent - running it multiple times is safe
- Only new data (not already in database) will be inserted

## Connection Pooling

The application uses connection pooling for better performance:
- Default: 1-10 connections
- Automatically managed by psycopg2
- Connections are reused efficiently

## Production Considerations

For production deployment:

1. Use environment variables for all credentials (never hardcode)
2. Set up proper backup procedures for PostgreSQL
3. Configure connection pooling appropriately for your load
4. Use SSL/TLS for database connections
5. Set up proper database user with limited privileges (not superuser)
6. Regularly update PostgreSQL and Python dependencies

## Support

If you encounter issues:
1. Check PostgreSQL logs: `sudo tail -f /var/log/postgresql/postgresql-*.log` (Linux)
2. Verify all environment variables are set correctly
3. Ensure Python packages are installed: `pip list | grep psycopg2`
4. Check database connection: `psql -U postgres -d onlineshopping`
