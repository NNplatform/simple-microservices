from flask import Flask, jsonify, request # type: ignore

app = Flask(__name__)

@app.route("/")
def hello():
    return "Greeting from Dev-fun App Service!"

data = {
    "1": {"name": "John Doe", "age": 30},
    "2": {"name": "Jane Doe", "age": 25}
}

@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify(data), 200

@app.route('/api/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = data.get(user_id)
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/user', methods=['POST'])
def create_user():
    user_id = str(len(data) + 1)
    user_data = request.json
    data[user_id] = user_data
    return jsonify({"id": user_id}), 201

@app.route('/api/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    if user_id in data:
        data[user_id].update(user_data)
        return jsonify(data[user_id]), 200
    else:
        return jsonify({"error": "User not found"}), 404

@app.route('/api/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in data:
        del data[user_id]
        return jsonify({"message": "User deleted"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)