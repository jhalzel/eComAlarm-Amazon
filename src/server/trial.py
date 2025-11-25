from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from dotenv import load_dotenv
import base64
import json
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from serviceAbout import find_item_by_upc, find_competitive_pricing, process_upc_batch
import pandas as pd
import tempfile
from werkzeug.utils import secure_filename
import logging


app = Flask(__name__)

# get the .env file path
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

# load the .env file
load_dotenv(dotenv_path)

# Initialize Firebase using default credentials
cred = credentials.ApplicationDefault()

# Get the JSON string from the environment variable
firebase_admin_key_json = os.getenv('FIREBASE_ADMIN_KEY')

# Parse the JSON string into a dictionary
firebase_admin_key_dict = json.loads(base64.b64decode(firebase_admin_key_json).decode('utf-8'))

# Initialize Firebase with the parsed dictionary
service_account_cred = credentials.Certificate(firebase_admin_key_dict)

firebase_admin.initialize_app(service_account_cred, {
    'databaseURL': 'https://notifier-6d1a0-default-rtdb.firebaseio.com'
})

# Store the Firebase app instance in the Flask app's configuration
firebase_config = app.config['firebase_app'] = firebase_admin.get_app()


# Enable CORS for all routes
# CORS(app, origins=["http://127.0.0.1:5000/", "http://localhost:3000", "https://amazon-ecom-alarm.onrender.com", "https://rainbow-branch--ecom-alarm.netlify.app"])
# CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5001/", "http://localhost:3000", "https://amazon-ecom-alarm.onrender.com", "https://rainbow-branch--ecom-alarm.netlify.app"]}})
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://127.0.0.1:5001",
        "http://localhost:3000",
        "https://amazon-ecom-alarm.onrender.com",
        "https://ecom-alarm.netlify.app",           # <-- PRODUCTION
        "https://rainbow-branch--ecom-alarm.netlify.app"  # <-- PREVIEW
    ]}},
    supports_credentials=True
)


@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "https://ecom-alarm.netlify.app"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"]
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"]
    return response


# Store the fbm_threshold value
fbm_threshold = None

cur_dir = os.path.dirname(__file__)
config_filename = os.path.join(cur_dir, 'config.json')
event_filename = os.path.join(cur_dir, 'event.json')


def get_sp_api_credentials():
    """Get Amazon SP-API credentials from environment variables"""
    return {
        "refresh_token": os.environ.get("SP_API_REFRESH_TOKEN"),
        "lwa_app_id": os.environ.get("LWA_APP_ID"),
        "lwa_client_secret": os.environ.get("LWA_CLIENT_SECRET"),
        "aws_access_key": os.environ.get("SP_API_ACCESS_KEY"),
        "aws_secret_key": os.environ.get("SP_API_SECRET_KEY"),
        "role_arn": os.environ.get("SP_API_ROLE_ARN")
    }

@app.route('/')
# @cross_origin("*", methods=['GET'], headers=['Content-Type'])
def home():
    # Your code to render the home page or return some content
    return "Welcome to My App"


@app.route('/set_pause_status', methods=['POST'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def set_pause_status():
    status = request.json

    write_data = {"pause_status": status}
    try: 
        with open(event_filename, 'w') as file:
            json.dump(write_data, file, indent=4)

        return jsonify({'message': f'Pause status updated to {status}'})
    except FileNotFoundError:
        return jsonify({'message': 'Data not found'}), 404


@app.route('/get_pause_status', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def get_pause_status():
    try:
        with open(event_filename, 'r') as json_file:
            data = json.load(json_file).get('pause_status')
        return jsonify(data)

    except FileNotFoundError:
        return jsonify({'message': 'Data not found'}), 404

    
    
# Route to retrieve JSON data (GET)
@app.route('/get_data', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def get_json_data():
    json_filename = os.path.join(cur_dir, 'data.json')

    try:
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)

    except FileNotFoundError:
        return jsonify({'message': 'Data not found'}), 404
    


# Route to retrieve the data from the firebase database (GET)
@app.route('/get_firebase_data', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def get_firebase_data():
    # Get a database reference
    ref = db.reference()
    
    # Read the data at the posts reference (this is a blocking operation)
    data = ref.get()

    return jsonify(data)



# Route to update the data in the firebase database (POST)
@app.route('/set_firebase_data', methods=['POST'])
@cross_origin("*", methods=['POST'])
def set_firebase_data():
    # Access the data sent in the request body
    data = request.json

    print('request from client: ', data)

    fbm_threshold = data.get('fbm_threshold')

    print('fbm_threshold: ', fbm_threshold)

    # Get a database reference
    ref = db.reference()

    database_data = ref.get() 

    print('database_data: ', database_data)

    data_keys = list(database_data.keys())

    if data_keys:
        last_key = data_keys[-1]  # Access the key of the last object
        last_entry = database_data[last_key]  # Access the last object using the key
        threshold = last_entry.get('threshold')
        
        # Update the value in Firebase for the specific child object (last entry)
        ref.child(last_key).update({'threshold': [fbm_threshold]})

    return jsonify({'message': 'Data received'})

@app.route('/api/amazon/find-items-by-upc', methods=['POST'])
@cross_origin("*", methods=['POST'])
def find_items_by_upc():
    """Find Amazon products by UPC codes"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        upcs = data.get('upcs', [])
        costs = data.get('costs', [])
        
        if not upcs or not costs:
            return jsonify({"error": "Both 'upcs' and 'costs' arrays are required"}), 400
            
        if len(upcs) != len(costs):
            return jsonify({"error": "UPCs and costs arrays must have equal length"}), 400
        
        # Format UPCs to 12-digit strings (preserve leading zeros)
        formatted_upcs = [str(int(upc)).zfill(12) for upc in upcs]
        
        # Format costs to floats
        formatted_costs = [float(cost.strip('$')) if isinstance(cost, str) else float(cost) for cost in costs]
        
        # Get credentials and call your function
        credentials = get_sp_api_credentials()
        result_df = find_item_by_upc(formatted_upcs, formatted_costs, credentials)
        
        # Count successful matches
        found_items = len(result_df[result_df['ASIN'] != ''])
        
        return jsonify({
            "success": True,
            "data": result_df.to_dict('records'),
            "summary": {
                "total_upcs": len(upcs),
                "items_found": found_items,
            }
        })
        
    except Exception as e:
        print(f"Find items by UPC error: {str(e)}")
        return jsonify({"error": f"Failed to find items: {str(e)}"}), 500



@app.route('/api/amazon/get-pricing', methods=['POST'])
@cross_origin("*", methods=['POST'])
def get_pricing():
    """Get competitive pricing for ASINs using your find_competitive_pricing function"""
    try:
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        asins = data.get('asins', [])
        
        if not asins:
            return jsonify({"error": "ASINs array is required"}), 400
        
        # Filter out empty ASINs
        valid_asins = [asin for asin in asins if asin and asin.strip()]
        
        if not valid_asins:
            return jsonify({"error": "No valid ASINs provided"}), 400
        
        # Call your existing function
        pricing_dict = find_competitive_pricing(valid_asins)
        
        return jsonify({
            "success": True,
            "pricing": pricing_dict,
            "asins_processed": len(valid_asins),
            "pricing_found": len(pricing_dict)
        })
        
    except Exception as e:
        print(f"Pricing error: {str(e)}")
        return jsonify({"error": f"Failed to get pricing: {str(e)}"}), 500


@app.route('/api/process_upc_batch', methods=['POST'])
@cross_origin("*", methods=['POST'])
def api_process_upc_batch():
    try:
        data = request.get_json()
        upc_list = data['upc_list']
        costs_list = data['costs_list']

        # Make sure credentials are retrieved here if needed
        credentials = get_sp_api_credentials()

        result = process_upc_batch(upc_list, costs_list, credentials)
        print(f"API result: {result}")

        return jsonify(result)

    except Exception as e:
        print(f"Error in /api/process_upc_batch: {e}")
        return jsonify({"error": str(e)}), 500




if __name__ == '__main__':
    app.run(debug=True)