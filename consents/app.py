from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def hello():
    return "Greeting from Consents Service!"

consents_data = {
    "1": {"user": "John Doe", "consent": "granted"},
    "2": {"user": "Jane Doe", "consent": "denied"}
}

@app.route('/api/consent/<consent_id>', methods=['GET'])
def get_consents(consent_id):
    consent = consents_data.get(consent_id)
    if consent:
        return jsonify(consent), 200
    else:
        return jsonify({"error": "Consent not found"}), 404

@app.route('/api/consents', methods=['GET'])
def get_all_consents():
    return jsonify(consents_data), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)