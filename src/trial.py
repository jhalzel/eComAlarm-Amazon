from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
from flask_cors import CORS, cross_origin
from script import main
from flask import request
import os
import json

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["http://127.0.0.1:5000/", "http://localhost:3000", "https://amazon-ecom-alarm.onrender.com", "https://rainbow-branch--ecom-alarm.netlify.app"])
CORS(app, origins=["http://127.0.0.1:5000/", "http://localhost:3000", "https://amazon-ecom-alarm.onrender.com", "https://rainbow-branch--ecom-alarm.netlify.app"])

# Store the fbm_threshold value
fbm_threshold = None

cur_dir = os.path.dirname(__file__)
config_filename = os.path.join(cur_dir, 'config.json')
event_filename = os.path.join(cur_dir, 'event.json')
event_filename = os.path.join(cur_dir, 'event.json')

@app.route('/')
def home():
    # Your code to render the home page or return some content
    return "Welcome to My App"


# Set the fbm_threshold value
@app.route('/set_threshold', methods=['POST'])
@cross_origin("*", methods=['POST'], headers=['Content-Type'])
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
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
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
@cross_origin("*", methods=['POST'], headers=['Content-Type'])
@cross_origin("*", methods=['POST'], headers=['Content-Type'])
def set_json_data():
    json_filename = os.path.join(cur_dir, 'data.json')
    
    try: 
        data = request.json
        
        data = jsonify(data)

        try:
            with open(json_filename, 'r') as json_file:
                existing_data = json.load(json_file)
            
            print(f'Existing data: {existing_data}')

            # Check if there is data with the same date in the existing entries
            date_to_update = data.get('date')  # Assuming 'date' is a key in your JSON data
            # Check if there is data with the same date in the existing entries
            date_to_update = data.get('date')  # Assuming 'date' is a key in your JSON data

            print(f'Date to update: {date_to_update}')

            parsed_data = [json.loads(entry) for entry in existing_data]

            if date_to_update[0] in [entry['date'][0] for entry in parsed_data]:
                for entry in parsed_data:
                    if entry['date'][0] == date_to_update[0]:
                        # delete the entry
                        existing_data.remove(json.dumps(entry))
                # append the new entry to the end of the list
                existing_data.append(data)

            if date_to_update[0] not in [entry['date'][0] for entry in parsed_data]:
                existing_data.append(data)
            
            # If file is greater than 90 lines, remove the oldest lines to maintain 90 days of data
            if len(existing_data) > 90:
                existing_data = existing_data[:90]
            print(f'Date to update: {date_to_update}')

            parsed_data = [json.loads(entry) for entry in existing_data]

            if date_to_update[0] in [entry['date'][0] for entry in parsed_data]:
                for entry in parsed_data:
                    if entry['date'][0] == date_to_update[0]:
                        # delete the entry
                        existing_data.remove(json.dumps(entry))
                # append the new entry to the end of the list
                existing_data.append(data)

            if date_to_update[0] not in [entry['date'][0] for entry in parsed_data]:
                existing_data.append(data)
            
            # If file is greater than 90 lines, remove the oldest lines to maintain 90 days of data
            if len(existing_data) > 90:
                existing_data = existing_data[:90]

            # Write JSON data to file
            try: 
                with open(json_filename, 'w') as json_file:
                    json.dumps(existing_data, json_file, indent=4)
            # Write JSON data to file
            try: 
                with open(json_filename, 'w') as json_file:
                    json.dumps(existing_data, json_file, indent=4)

            except FileNotFoundError:
                return jsonify({'error': 'Data file not found'}), 404
            
        except FileNotFoundError:
            existing_data = []

    except Exception as e: 
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
    # return jsonify({'message': 'Data updated successfully'})
            except FileNotFoundError:
                return jsonify({'error': 'Data file not found'}), 404
            
        except FileNotFoundError:
            existing_data = []

    except Exception as e: 
        print(str(e))
        return jsonify({'error': 'Internal Server Error'}), 500
    
    # return jsonify({'message': 'Data updated successfully'})


# Route to retrieve the event.json file (GET)
@app.route('/get_event', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def get_event():
    try:
        with open(event_filename, 'r') as json_file:
            event = json.load(json_file)

        # Save the updated 'event' dictionary back to 'event.json'
        with open(event_filename, 'w') as json_file:
            json.dump(event, json_file, indent=4)

        return jsonify(event)
    except Exception as e:
        print(str(e))  # Print the exception for debugging
        return jsonify({'error': 'Internal Server Error'}), 500
# Route to retrieve the event.json file (GET)
@app.route('/get_event', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def get_event():
    try:
        with open(event_filename, 'r') as json_file:
            event = json.load(json_file)

        # Save the updated 'event' dictionary back to 'event.json'
        with open(event_filename, 'w') as json_file:
            json.dump(event, json_file, indent=4)

        return jsonify(event)
    except Exception as e:
        print(str(e))  # Print the exception for debugging
        return jsonify({'error': 'Internal Server Error'}), 500

# Members API Route
@app.route('/members', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
@app.route('/members', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def members():
    status = main()  # Call the main function to execute the code

    print('status', status)

    print("config_filename", config_filename)

    # get the fbm_threshold value from the config.json file
    try:
        with open(config_filename, 'r') as file:
            config = json.load(file)
            fbm_threshold = config.get('fbm_threshold')
            print('fbm_threshold', fbm_threshold)
            print('type(fbm_threshold)', type(fbm_threshold))
    except FileNotFoundError:
        fbm_threshold = 0
        return jsonify({'error': 'Config file not found'}), 404
    

    fba_pending_sales = status['fba_pending_sales']  # Extract the total FBA pending sales value from the dictionary
    fbm_pending_sales = status['fbm_pending_sales']  # Extract the total FBM pending sales value from the dictionary
    total_sales = status['total_sales']  # Extract the total sales value from the dictionary
    fba_sales = status['fba_sales']  # Extract the total FBA sales value from the dictionary
    fbm_sales = status['fbm_sales']  # Extract the total FBM sales value from the dictionary
    order_pending_count = status['order_pending_count']  # Extract the order pending count value from the dictionary
    shipped_order_count = status['shipped_order_count']  # Extract the shipped order count value from the dictionary
    total_order_count = status['total_order_count']  # Extract the order count value from the dictionary
    last_updated = status['last_updated']  # Extract the last updated timestamp value from the dictionary

    fbm_threshold = float(fbm_threshold)  # Convert the fbm_threshold value to a float

    # Create a dictionary containing the data
    data_dict = {
        'fba_sales': fba_sales,
        'fbm_sales': fbm_sales,
        'total_order_count': total_order_count,
        'order_pending_count': order_pending_count,
        'last_updated': last_updated,
        'shipped_order_count': shipped_order_count,
        'total_sales': total_sales,
        'fba_pending_sales': fba_pending_sales,
        'fbm_pending_sales': fbm_pending_sales,
        'fbm_threshold': fbm_threshold  # Assuming fbm_threshold is defined elsewhere
    }

    # Serialize the data to JSON
    json_data = json.dumps(data_dict, indent=4)

    try: 
        # Write the JSON data to 'event.json' file
        with open( event_filename, 'w') as json_file:
            json_file.write(json_data)
    except FileNotFoundError:
        return jsonify({'error': 'Event file not found'}), 404

    # Return the JSON data
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run()