from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

customers = [
    {"id": 1, "name": "Alice Smith", "email": "alice@example.com"},
    {"id": 2, "name": "Bob Jones", "email": "bob@example.com"}
]

@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers)

@app.route('/customers', methods=['POST'])
def create_customer():
    if not request.json or not 'name' in request.json or not 'email' in request.json:
        abort(400, description="Missing 'name' or 'email' for the customer.")
    
    new_customer = {
        'id': customers[-1]['id'] + 1 if customers else 1,
        'name': request.json['name'],
        'email': request.json['email']
    }
    customers.append(new_customer)
    return jsonify(new_customer), 201

@app.route('/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    customer = next((cust for cust in customers if cust['id'] == customer_id), None)
    if not customer:
        abort(404, description="Customer not found.")
    if not request.json:
        abort(400, description="Request must be JSON.")
    
    customer['name'] = request.json.get('name', customer['name'])
    customer['email'] = request.json.get('email', customer['email'])
    return jsonify(customer)

@app.route('/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    global customers
    customers = [cust for cust in customers if cust['id'] != customer_id]
    return jsonify({'result': True})

@app.route('/customers/<int:customer_id>/products', methods=['GET'])
def get_customer_products(customer_id):
    # This is a mock function to simulate getting customer's purchased product IDs.
    purchased_product_ids = [1, 2]  

    products = []
    for product_id in purchased_product_ids:
        response = requests.get(f'http://localhost:5001/products/{product_id}')
        if response.ok:
            products.append(response.json())
        else:
            abort(response.status_code, description="Problem fetching product details.")

    return jsonify(products)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "CUSTOMERS UP"}), 200


if __name__ == '__main__':
    app.run(port=5002)
