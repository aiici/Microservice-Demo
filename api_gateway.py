from flask import Flask, jsonify, request, render_template
import requests

app = Flask(__name__)

CONSUL_URL = "http://localhost:8500/v1/catalog/service"

def get_service(service_name):
    """从 Consul 获取服务信息"""
    service = requests.get(f"{CONSUL_URL}/{service_name}")
    service_info = service.json()
    if len(service_info) > 0:
        address = service_info[0]['ServiceAddress']
        port = service_info[0]['ServicePort']
        return f"http://{address}:{port}"
    return None

# Web 页面路由
@app.route('/')
def index():
    return render_template('index.html')

# 用户 API
@app.route('/users', methods=['GET', 'POST'])
def users():
    user_service_url = get_service("user-service")
    if not user_service_url:
        return jsonify({"error": "User service not found"}), 503
    if request.method == 'GET':
        response = requests.get(f"{user_service_url}/users")
    else:
        response = requests.post(f"{user_service_url}/users", json=request.json)
    return jsonify(response.json()), response.status_code

# 订单 API
@app.route('/orders', methods=['GET', 'POST'])
def orders():
    order_service_url = get_service("order-service")
    if not order_service_url:
        return jsonify({"error": "Order service not found"}), 503
    if request.method == 'GET':
        response = requests.get(f"{order_service_url}/orders")
    else:
        response = requests.post(f"{order_service_url}/orders", json=request.json)
    return jsonify(response.json()), response.status_code

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user_service_url = get_service("user-service")
    if not user_service_url:
        return jsonify({"error": "User service not found"}), 503
    response = requests.delete(f"{user_service_url}/users/{user_id}")
    return jsonify(response.json()), response.status_code

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order_service_url = get_service("order-service")
    if not order_service_url:
        return jsonify({"error": "Order service not found"}), 503
    response = requests.delete(f"{order_service_url}/orders/{order_id}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)