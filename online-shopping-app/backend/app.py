from flask import Flask
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.products import product_bp

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Register all blueprints
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(product_bp, url_prefix="/products")

@app.route("/")
def index():
    return {"message": "Welcome to the Online Shopping Backend"}

if __name__ == "__main__":
    app.run(debug=True)
