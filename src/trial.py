from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from flask import request
from dotenv import load_dotenv
import base64
import os
import json


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
CORS(app, resources={r"/*": {"origins": ["http://127.0.0.1:5000/", "http://localhost:3000", "https://amazon-ecom-alarm.onrender.com", "https://rainbow-branch--ecom-alarm.netlify.app"]}})


# Store the fbm_threshold value
fbm_threshold = None

cur_dir = os.path.dirname(__file__)
config_filename = os.path.join(cur_dir, 'config.json')
event_filename = os.path.join(cur_dir, 'event.json')


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
        print("Last entry:", last_entry)
        threshold = last_entry.get('threshold')
        print('threshold: ', threshold)
        
        # Update the threshold value in the last entry
        # last_entry['threshold'] = [fbm_threshold]

        # Update the value in Firebase for the specific child object (last entry)
        ref.child(last_key).update({'threshold': [fbm_threshold]})

    return jsonify({'message': 'Data received'})


if __name__ == '__main__':
    app.run(debug=True)