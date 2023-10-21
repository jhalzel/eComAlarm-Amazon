from flask import Flask, jsonify, send_file
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
CORS(app, origins=["http://127.0.0.1:5000/", "http://localhost:3000", "https://amazon-ecom-alarm.onrender.com", "https://rainbow-branch--ecom-alarm.netlify.app"])


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


# Set the fbm_threshold value
@app.route('/set_threshold', methods=['POST'])
@cross_origin("*", methods=['POST'], headers=['Content-Type'])
def set_threshold():
    data = request.json
    new_threshold = data.get('fbm_threshold')
    
    # Create a dictionary with the new threshold
    data_to_write = {"fbm_threshold": new_threshold}
    
    # Write the new threshold to the config.json file
    with open(config_filename, 'w') as file:
        json.dump(data_to_write, file, indent=4)    

    return jsonify({'message': f'Threshold updated to {new_threshold}'})

@app.route('/get_threshold', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def get_threshold():
    try:
        with open(config_filename, 'r') as file:
            config = json.load(file)
            fbm_threshold = config.get('fbm_threshold')
            return jsonify({'fbm_threshold': fbm_threshold})
    except FileNotFoundError:
        return jsonify({'error': 'Config file not found'})
    
    
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
@cross_origin("*", methods=['POST'], headers=['Content-Type'])
def set_firebase_data():
    # Get new threshold
    new_threshold = request.json.get('fbm_threshold')

    if new_threshold is None:
        return jsonify({'error': 'fbm_threshold not found'}), 400

    print(f'New threshold: {new_threshold}')

    # Get a database reference
    ref = db.reference()

    # Convert the JSON data to a dictionary
    loaded_data = ref.get()

    # Get the last entry from the list
    last_entry = loaded_data[-1]

    print(f'Last entry: {last_entry}')

    return jsonify({'message': 'Data updated successfully'})


    # # update the last entries threshold value
    # last_entry['fbm_threshold'] = ref.update({'fbm_threshold': new_threshold})

    # # Write the new data to the database
    # ref.set(loaded_data)

    # return jsonify({'message': 'Data updated successfully'})





if __name__ == '__main__':
    app.run(debug=True)