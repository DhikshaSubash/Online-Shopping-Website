from flask import Blueprint, jsonify, request
from utils.csv_handler import read_csv
import os

product_bp = Blueprint('product', __name__)
PRODUCTS_CSV = os.path.join('data', 'products.csv')

@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = read_csv(PRODUCTS_CSV)
    return jsonify(products)

@product_bp.route('/search', methods=['GET'])
def search_product():
    query = request.args.get("q", "").lower()
    products = read_csv(PRODUCTS_CSV)
    results = [p for p in products if query in p['name'].lower()]
    return jsonify(results)
