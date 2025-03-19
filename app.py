from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# Supabase Configuration
SUPABASE_URL = "https://bzzkdkhwvmzuipfqfvxi.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
SUPABASE_TABLE = "products"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

# Local Storage Backup File
LOCAL_STORAGE_FILE = "local_products.json"

# Function to Save Local Data
def save_local_data(data):
    with open(LOCAL_STORAGE_FILE, "w") as file:
        json.dump(data, file)

# Function to Load Local Data
def load_local_data():
    if os.path.exists(LOCAL_STORAGE_FILE):
        with open(LOCAL_STORAGE_FILE, "r") as file:
            return json.load(file)
    return []

# 📌 **Get All Products**
@app.route('/products', methods=['GET'])
def get_products():
    try:
        response = requests.get(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}", headers=HEADERS)
        if response.status_code == 200:
            return jsonify(response.json()), 200
    except Exception as e:
        print("Error fetching from Supabase:", e)
    
    return jsonify(load_local_data()), 200

# 📌 **Add New Product**
@app.route('/products', methods=['POST'])
def add_product():
    data = request.json
    try:
        response = requests.post(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}", headers=HEADERS, json=[data])
        if response.status_code == 201:
            return jsonify({"message": "Product Added!"}), 201
    except Exception as e:
        print("Supabase Error:", e)
    
    products = load_local_data()
    products.append(data)
    save_local_data(products)
    return jsonify({"message": "Saved Locally!"}), 200

# 📌 **Delete Product**
@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        response = requests.delete(f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?id=eq.{product_id}", headers=HEADERS)
        if response.status_code == 204:
            return jsonify({"message": "Product Deleted!"}), 200
    except Exception as e:
        print("Supabase Error:", e)
    
    products = load_local_data()
    products = [p for p in products if p.get("id") != product_id]
    save_local_data(products)
    return jsonify({"message": "Deleted Locally!"}), 200

# 📌 **Run Flask Server**
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)