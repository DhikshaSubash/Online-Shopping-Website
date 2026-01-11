# Quick Start Guide - PostgreSQL Migration

## 🚀 Get Started in 5 Minutes

### Step 1: Install PostgreSQL
```bash
# Windows: Download installer from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Linux: sudo apt-get install postgresql postgresql-contrib
```

### Step 2: Create .env File
Create `backend/.env` with:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=onlineshopping
DB_USER=postgres
DB_PASSWORD=postgres
```
*(Change password to your PostgreSQL password)*

### Step 3: Install Python Packages
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Start the Application
```bash
python app.py
```

That's it! The database will be created and CSV data migrated automatically.

## ✅ Verification

Check if it worked:
```bash
# In another terminal
psql -U postgres -d onlineshopping
```
```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM orders;
\q
```

## 🔧 Troubleshooting

**"Connection refused"**
- Start PostgreSQL service
- Check DB_PORT in .env (default: 5432)

**"Authentication failed"**
- Verify DB_USER and DB_PASSWORD in .env
- Test manually: `psql -U postgres`

**"Database does not exist"**
- The app creates it automatically on first run
- Or create manually: `createdb onlineshopping`

## 📚 More Information

- **Detailed Setup**: See `POSTGRESQL_SETUP.md`
- **Migration Summary**: See `MIGRATION_SUMMARY.md`
- **Full README**: See `README_POSTGRESQL.md`

## 🎯 What Changed?

- ✅ All CSV operations → PostgreSQL
- ✅ Same API endpoints (no frontend changes needed!)
- ✅ CSV files preserved as backup
- ✅ Automatic migration on first run

## 📊 API Endpoints (Unchanged)

All endpoints work exactly the same:
- `/auth/signup`, `/auth/login`, etc.
- `/user/products`, `/user/cart`, etc.
- `/admin/users`, `/admin/orders`, etc.

Frontend code requires **ZERO changes**! 🎉
