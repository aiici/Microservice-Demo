import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import atexit

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:AiiCi123.456@localhost/order_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 订单模型
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([{'id': order.id, 'item': order.item, 'price': str(order.price)} for order in orders]), 200

@app.route('/orders', methods=['POST'])
def create_order():
    order_data = request.json
    new_order = Order(item=order_data['item'], price=order_data['price'])
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'id': new_order.id, 'item': new_order.item, 'price': str(new_order.price)}), 201

@app.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"}), 200

def register_service():
    """注册服务到 Consul"""
    consul_url = "http://localhost:8500/v1/agent/service/register"
    service_data = {
        "ID": "order-service",
        "Name": "order-service",
        "Address": "localhost",
        "Port": 5002,
        "Check": {
            "HTTP": "http://localhost:5002/health",
            "Interval": "10s"
        }
    }
    requests.put(consul_url, json=service_data)

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查"""
    return jsonify({"status": "UP"}), 200

def deregister_service():
    """从 Consul 注销服务"""
    consul_url = "http://localhost:8500/v1/agent/service/deregister/order-service"
    requests.put(consul_url)

if __name__ == '__main__':
    register_service()
    atexit.register(deregister_service)  # 程序退出时注销服务
    app.run(port=5002)
