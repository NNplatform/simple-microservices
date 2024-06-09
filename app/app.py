from flask import Flask, jsonify, request
from flask_cors import CORS
from elasticsearch import Elasticsearch
from urllib3.util import Retry
import logging
import time

app = Flask(__name__)
CORS(app)

# Initialize Elasticsearch client
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
es = Elasticsearch(['http://elasticsearch:9200'], retry_on_timeout=True, max_retries=retries)

# Check if index exists, if not, create it
def create_index_with_retry(es, index_name, max_retries=5):
    retries = max_retries
    while retries > 0:  # Check if retries remain
        try:
            if not es.indices.exists(index=index_name):
                es.indices.create(index=index_name)
                return
        except Exception as e:
            print(f"Attempt {retries} failed: {e}. Retrying...")
            time.sleep(2 ** (max_retries - retries))  # Exponential backoff
            retries -= 1  # Decrement retries after each attempt
    print("Max retries reached. Failed to create index.")

create_index_with_retry(es, "devfun-app-index")

# Initialize data from Elasticsearch
def init_data_from_es():
    global data
    try:
        result = es.search(index="devfun-app-index", body={"query": {"match_all": {}}})
        data = {hit['_id']: hit['_source'] for hit in result['hits']['hits']}
    except Exception as e:
        print(f"Error initializing data from ES: {e}")

init_data_from_es()

# Define a route to perform Elasticsearch search
@app.route('/search', methods=['GET'])
def search():
    query = {"query": {"match_all": {}}}
    index_name = "devfun-app-index"
    try:
        result = es.search(index=index_name, body=query)
        hits = [hit['_source'] for hit in result['hits']['hits']]
        return jsonify(hits)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Routes for basic CRUD operations
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
    try:
        es.index(index="devfun-app-index", id=user_id, body=user_data)
    except Exception as e:
        return jsonify({"error": f"Failed to index user: {e}"}), 500
    return jsonify({"id": user_id}), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
