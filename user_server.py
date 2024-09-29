import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import atexit

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:AiiCi123.456@localhost/user_service_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

# 创建数据库表
with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users]), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_data = request.json
    new_user = User(name=user_data['name'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'name': new_user.name}), 201

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200

def register_service():
    """注册服务到 Consul"""
    consul_url = "http://localhost:8500/v1/agent/service/register"
    service_data = {
        "ID": "user-service",
        "Name": "user-service",
        "Address": "localhost",
        "Port": 5001,
        "Check": {
            "HTTP": "http://localhost:5001/health",
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
    consul_url = "http://localhost:8500/v1/agent/service/deregister/user-service"
    requests.put(consul_url)

if __name__ == '__main__':
    register_service()
    atexit.register(deregister_service)  # 程序退出时注销服务
    app.run(port=5001)