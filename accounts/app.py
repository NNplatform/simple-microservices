from flask import Flask, jsonify, request # type: ignore

app = Flask(__name__)

@app.route("/")
def hello():
    return "Greeting from Accounts Service!"

accounts_data = {
    "1": {"name": "John Doe", "balance": 1000},
    "2": {"name": "Jane Doe", "balance": 1500}
}

@app.route('/api/account/<account_id>', methods=['GET'])
def get_account(account_id):
    account = accounts_data.get(account_id)
    if account:
        return jsonify(account), 200
    else:
        return jsonify({"error": "Account not found"}), 404

@app.route('/api/accounts', methods=['GET'])
def get_accounts():
    return jsonify(accounts_data), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)