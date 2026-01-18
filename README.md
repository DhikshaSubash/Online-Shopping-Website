# Online Shopping Website

A full-stack e-commerce application built with React (frontend) and Flask (backend), providing a complete online shopping experience with user authentication, product browsing, shopping cart, and order management.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Frontend Setup](#frontend-setup)
- [Backend Setup](#backend-setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

This is a modern e-commerce platform that allows users to: 
- Browse and search for products
- Add items to cart
- Place orders
- Track order history
- Manage user accounts

The application is built with a separation of concerns, featuring a React-based frontend for user interface and a Flask backend API for business logic and data management.

## Features

### Frontend Features
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Product Catalog**: Browse products with filters and search functionality
- **Shopping Cart**: Add, remove, and manage items in cart
- **User Authentication**:  Secure login and registration system
- **Order History**: View past orders and order details
- **User Profile**:  Manage user account information

### Backend Features
- **RESTful API**: Well-structured API endpoints for all operations
- **User Management**: Registration, authentication, and profile management
- **Product Management**:  CRUD operations for products
- **Order Processing**: Handle order creation, updates, and tracking
- **Database Integration**:  Persistent data storage with database
- **Input Validation**: Server-side validation for data integrity

## 🛠️ Technology Stack

### Frontend
- **React.js** - UI library for building interactive user interfaces
- **HTML/CSS/JavaScript** - Markup, styling, and scripting
- **Axios/Fetch API** - HTTP client for API communication
- **React Router** - Client-side routing (if implemented)
- **Node.js & npm** - JavaScript runtime and package manager

### Backend
- **Flask** - Python web framework
- **Python** - Programming language
- **Flask-SQLAlchemy** - ORM for database operations
- **Flask-CORS** - Cross-Origin Resource Sharing support
- **Python Virtual Environment** - Isolated Python environment

### Database
- SQLite/PostgreSQL/MySQL (as configured in backend)

## Project Structure

```
Online-Shopping-Website/
│
├── frontend/                    # React frontend application
│   ├── public/                 # Static files
│   ├── src/                    # Source code
│   │   ├── components/         # Reusable React components
│   │   ├── pages/              # Page components
│   │   ├── services/           # API service calls
│   │   ├── App.js              # Main App component
│   │   └── index.js            # Application entry point
│   ├── package.json            # Frontend dependencies
│   └── README. md               # Frontend documentation
│
├── backend/                     # Flask backend application
│   ├── app/                    # Flask application package
│   │   ├── models/             # Database models
│   │   ├── routes/             # API endpoints
│   │   ├── services/           # Business logic
│   │   └── __init__.py         # Flask app initialization
│   ├── config.py               # Configuration settings
│   ├── requirements.txt        # Python dependencies
│   ├── run.py                  # Application entry point
│   └── README.md               # Backend documentation
│
└── README.md                    # Project documentation (this file)
```

## Installation & Setup

### Prerequisites
- **Node.js** (v14+) and npm for the frontend
- **Python** (v3.8+) for the backend
- **Git** for version control
- **Virtual Environment** tool (venv)

### Clone the Repository

```bash
git clone https://github.com/DhikshaSubash/Online-Shopping-Website.git
cd Online-Shopping-Website
```

## Frontend Setup

### Installation Steps

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

   The application will open at `http://localhost:3000` in your browser.

### Available Frontend Scripts

- **`npm start`** - Runs the app in development mode
- **`npm test`** - Launches the test runner
- **`npm run build`** - Builds the app for production
- **`npm run eject`** - Ejects from Create React App (one-way operation)

### Frontend Notes
- The frontend automatically reloads when you make changes
- You may see lint errors in the console during development
- Ensure the backend API is running before starting the frontend

## 🔧 Backend Setup

### Installation Steps

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   **On Windows:**
   ```bash
   venv\Scripts\activate
   ```

   **On macOS/Linux:**
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   Create a `.env` file in the backend directory with:
   ```
   FLASK_ENV=development
   FLASK_APP=run.py
   SECRET_KEY=your-secret-key-here
   DATABASE_URL=sqlite:///app.db
   ```

6. **Initialize the database (if needed):**
   ```bash
   flask db upgrade
   ```

7. **Run the Flask server:**
   ```bash
   python run.py
   ```

   The backend API will be available at `http://localhost:5000`

### Backend Notes
- The Flask development server auto-reloads when you make changes
- Ensure you have activated the virtual environment
- Deactivate the virtual environment when finished:  `deactivate`

## Usage

### Running Both Frontend and Backend

1. **Start the backend:**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   python run.py
   ```

2. **In a new terminal, start the frontend:**
   ```bash
   cd frontend
   npm start
   ```

3. **Open your browser and navigate to:**
   ```
   http://localhost:3000
   ```

### Application Workflow

1. **User Registration/Login** - Create an account or log in
2. **Browse Products** - View available products with details
3. **Add to Cart** - Select desired products and quantities
4. **Review Cart** - Check items and modify quantities
5. **Checkout** - Enter shipping and payment information
6. **Order Confirmation** - Receive order confirmation
7. **View Orders** - Access order history and tracking

## 📡 API Endpoints

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Products
- `GET /api/products` - Get all products
- `GET /api/products/<id>` - Get a specific product
- `POST /api/products` - Create a new product (admin)
- `PUT /api/products/<id>` - Update a product (admin)
- `DELETE /api/products/<id>` - Delete a product (admin)

### Cart
- `GET /api/cart` - Get user's cart
- `POST /api/cart/items` - Add item to cart
- `PUT /api/cart/items/<id>` - Update cart item
- `DELETE /api/cart/items/<id>` - Remove item from cart

### Orders
- `POST /api/orders` - Create a new order
- `GET /api/orders` - Get user's orders
- `GET /api/orders/<id>` - Get order details

### Users
- `GET /api/users/profile` - Get user profile
- `PUT /api/users/profile` - Update user profile

*(Note: API endpoints may vary based on your implementation)*

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

### Guidelines
- Follow the existing code style
- Write meaningful commit messages
- Test your changes thoroughly
- Update documentation if needed

---

**Happy Shopping!  🛍️**

Built by [DhikshaSubash](https://github.com/DhikshaSubash)
