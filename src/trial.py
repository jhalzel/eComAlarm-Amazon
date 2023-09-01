from flask import Flask, jsonify, send_file
from flask_cors import CORS
from script import main
from flask import request
import os
import json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["http://localhost:3000"])

# Store the fbm_threshold value
fbm_threshold = None

cur_dir = os.path.dirname(__file__)
config_filename = os.path.join(cur_dir, 'config.json')

@app.route('/')
def home():
    # Your code to render the home page or return some content
    return "Welcome to My App"


# Set the fbm_threshold value
@app.route('/set_threshold', methods=['POST'])
def set_threshold():
    data = request.json
    new_threshold = data.get('fbm_threshold')
    
    # Update the config.json file with the new threshold
    with open(config_filename, 'r') as file:
        config = json.load(file)
        config['fbm_threshold'] = new_threshold

    with open(config_filename, 'w') as file:
        json.dump(config, file)

    return jsonify({'message': f'Threshold is now {config["fbm_threshold"]}'})


# Route to retrieve JSON data (GET)
@app.route('/get_data', methods=['GET'])
def get_json_data():
    json_filename = os.path.join(cur_dir, 'data.json')

    try:
        with open(json_filename, 'r') as json_file:
            data = json.load(json_file)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({'message': 'Data not found'}), 404
    
    
# Route to update JSON data (POST)
@app.route('/set_data', methods=['POST'])
def set_json_data():
    json_filename = os.path.join(cur_dir, 'data.json')
    data = request.json

    try:
        with open(json_filename, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = []

    # Check if there is data with the same date in the existing entries
    date_to_update = data.get('date')  # Assuming 'date' is a key in your JSON data

    for idx, entry in enumerate(existing_data):
        if entry.get('date') == date_to_update:
            # Update the existing entry with the new data
            existing_data[idx] = data
            break

    # Truncate the list if it exceeds a certain length (e.g., 90)
    max_data_length = 90
    if len(existing_data) > max_data_length:
        existing_data = existing_data[-max_data_length:]

    # Write the updated data back to the JSON file
    with open(json_filename, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return jsonify({'message': 'Data updated successfully'})



# Members API Route
@app.route('/members')
def members():
    status = main()  # Call the main function to execute the code
    
    # get the fbm_threshold value from the config.json file
    try:
        with open(config_filename, 'r') as file:
            config = json.load(file)
            fbm_threshold = config['fbm_threshold']
    except FileNotFoundError:
        fbm_threshold = None

    return jsonify({'fba_sales': status['fba_sales'], 
                    'fbm_sales': status['fbm_sales'], 
                    'total_order_count': status['total_order_count'], 
                    'order_pending_count': status['order_pending_count'], 
                    'last_updated': status['last_updated'], 
                    'shipped_order_count': status['shipped_order_count'], 
                    'total_sales': status['total_sales'],
                    'fba_pending_sales': status['fba_pending_sales'],
                    'fbm_pending_sales': status['fba_pending_sales'],
                    'fbm_threshold': fbm_threshold,
                    'date': status['']})

if __name__ == '__main__':
    app.run()