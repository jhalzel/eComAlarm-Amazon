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

    return jsonify({'message': 'Threshold updated successfully'})

# Get Json Data
@app.route('/get_json_data')
def get_json_data():
    json_filename = os.path.join(cur_dir, 'data.json')
    return send_file(json_filename)


# Members API Route
@app.route('/members')
def members():
    global fbm_threshold
    status = main()  # Call the main function to execute the code
    fbm_threshold = status['threshold']  # Extract the fbm_threshold value from the dictionary
    fba_pending_sales = status['fba_pending_sales']  # Extract the total FBA pending sales value from the dictionary
    fbm_pending_sales = status['fbm_pending_sales']  # Extract the total FBM pending sales value from the dictionary
    total_sales = status['total_sales']  # Extract the total sales value from the dictionary
    fba_sales = status['fba_sales']  # Extract the total FBA sales value from the dictionary
    fbm_sales = status['fbm_sales']  # Extract the total FBM sales value from the dictionary
    order_pending_count = status['order_pending_count']  # Extract the order pending count value from the dictionary
    shipped_order_count = status['shipped_order_count']  # Extract the shipped order count value from the dictionary
    total_order_count = status['total_order_count']  # Extract the order count value from the dictionary
    last_updated = status['last_updated']  # Extract the last updated timestamp value from the dictionary
    return jsonify({'fba_sales': fba_sales, 'fbm_sales': fbm_sales, 
                    'total_order_count': total_order_count, 
                    'order_pending_count': order_pending_count, 
                    'last_updated': last_updated, 
                    'shipped_order_count': shipped_order_count, 
                    'total_sales': total_sales,
                    'fba_pending_sales': fba_pending_sales,
                    'fbm_pending_sales': fbm_pending_sales,
                    'fbm_threshold': fbm_threshold}
                    )

if __name__ == '__main__':
    app.run()