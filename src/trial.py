from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
from script import main
from flask import request
import os
import json

app = Flask(__name__)

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
    
    
# Route to update JSON data (POST)
@app.route('/set_data', methods=['POST'])
@cross_origin("*", methods=['POST'], headers=['Content-Type'])
def set_data():
     # Get the path to the JSON file
    json_filename = os.path.join(cur_dir, 'data.json')

    # Get the JSON data from the request (String format)
    data = request.json

    # Convert the JSON data to a dictionary
    loaded_data = json.loads(data)

    # Print the loaded data
    print(f'Loaded data: {loaded_data}')

   
    # try to load the existing data from the file
    try:
        # Load existing data from the file, if it exists
        with open(json_filename, 'r') as json_file:
            existing_data = json.load(json_file)


            # Iterate through each string entry in the list
            entry_dict = [json.loads(entry) for entry in existing_data]
            print(f'Entry dict: {entry_dict}')

            # Access the latest date value from the list
            date_to_update = entry_dict[-1].get('date')[0]

            # print the date value
            print(f'Date to update: {date_to_update}')

            # print the loaded data date value
            print(f'Loaded data date: {loaded_data.get("date")[0]}')

            # If the date value is the same as the loaded data, remove the last entry from the list
            if date_to_update == loaded_data.get('date')[0]:
                existing_data.pop()
                print(f'Existing data: {existing_data}')

    except FileNotFoundError:
        existing_data = []

    # Append the new entry to the end of the list
    existing_data.append(data)
        
    with open(json_filename, 'w') as json_file:
            json.dump(existing_data, json_file) 


    return jsonify({'message': 'Data updated successfully'})

   # Read existing JSON data from the file, or initialize an empty list if the file doesn't exist
    # try:
    #     with open(json_filename, 'r') as json_file:
    #         existing_data = json.load(json_file)
    # except FileNotFoundError:
    #     existing_data = []

    # print(f'existing_data: {existing_data}')

    # # # Check if there is data with the same date in the existing entries
    # date_to_update = data.get('date')  # Assuming 'date' is a key in your JSON data

    # print(f'date_to_update: {date_to_update[0]}')

    # parsed_data = [json.loads(entry) for entry in existing_data]

    # print(f'parsed_data: {parsed_data}')

    # if date_to_update[0] in [entry['date'][0] for entry in parsed_data]:
    #     for entry in parsed_data:
    #         if entry['date'][0] == date_to_update[0]:
    #             # delete the entry
    #             existing_data.remove(json.dumps(entry))
    #     # append the new entry to the end of the list
    #     existing_data.append(data)

    # if date_to_update[0] not in [entry['date'][0] for entry in parsed_data]:
    #     existing_data.append(data)
    
    # # If file is greater than 90 lines, remove the oldest lines to maintain 90 days of data
    # if len(existing_data) > 90:
    #     existing_data = existing_data[:90]

    # # Write JSON data to file
    # with open(json_filename, 'w') as json_file:
    #     json.dump(existing_data, json_file, indent=4)
    
        


    # try:
    #     # data = request.json

    #     with open(json_filename, 'r') as json_file:
    #         existing_data = json.load(json_file)

    #     print(f'Existing data: {existing_data}')

    #     return jsonify({'message': 'Data updated successfully'})
    
    # except Exception as e: 
    #     print(str(e))
    #     return jsonify({'error': 'Internal Server Error'}), 500

    #     # try:
        #     with open(json_filename, 'r') as json_file:
        #         existing_data = json.load(json_file)
            
        #     print(f'Existing data: {existing_data}')

        #     # Check if there is data with the same date in the existing entries
        #     date_to_update = data.get('date')  # Assuming 'date' is a key in your JSON data

        #     print(f'Date to update: {date_to_update}')

        #     parsed_data = [json.loads(entry) for entry in existing_data]

        #     if date_to_update[0] in [entry['date'][0] for entry in parsed_data]:
        #         for entry in parsed_data:
        #             if entry['date'][0] == date_to_update[0]:
        #                 # delete the entry
        #                 existing_data.remove(json.dumps(entry))
        #         # append the new entry to the end of the list
        #         existing_data.append(data)

        #     if date_to_update[0] not in [entry['date'][0] for entry in parsed_data]:
        #         existing_data.append(data)
            
        #     # If file is greater than 90 lines, remove the oldest lines to maintain 90 days of data
        #     if len(existing_data) > 90:
        #         existing_data = existing_data[:90]

        #     # Write JSON data to file
        #     try: 
        #         with open(json_filename, 'w') as json_file:
        #             json.dumps(existing_data, json_file, indent=4)

        #     except FileNotFoundError:
        #         return jsonify({'error': 'Data file not found'}), 404
            
        # except FileNotFoundError:
        #     existing_data = []

    # except Exception as e: 
    #     print(str(e))
    #     return jsonify({'error': 'Internal Server Error'}), 500
    
    # return jsonify({'message': 'Data updated successfully'})



# Members API Route
@app.route('/members', methods=['GET'])
@cross_origin("*", methods=['GET'], headers=['Content-Type'])
def members():
    status = main()  # Call the main function to execute the code
    
    # get the fbm_threshold value from the config.json file
    try:
        with open(config_filename, 'r') as file:
            config = json.load(file)
            fbm_threshold = config['fbm_threshold']
            print('fbm_threshold: ', fbm_threshold)
    except FileNotFoundError:
        fbm_threshold = None

    fba_pending_sales = status['fba_pending_sales']  # Extract the total FBA pending sales value from the dictionary
    fbm_pending_sales = status['fbm_pending_sales']  # Extract the total FBM pending sales value from the dictionary
    total_sales = status['total_sales']  # Extract the total sales value from the dictionary
    fba_sales = status['fba_sales']  # Extract the total FBA sales value from the dictionary
    fbm_sales = status['fbm_sales']  # Extract the total FBM sales value from the dictionary
    order_pending_count = status['order_pending_count']  # Extract the order pending count value from the dictionary
    shipped_order_count = status['shipped_order_count']  # Extract the shipped order count value from the dictionary
    total_order_count = status['total_order_count']  # Extract the order count value from the dictionary
    last_updated = status['last_updated']  # Extract the last updated timestamp value from the dictionary
    return jsonify({'fba_sales': fba_sales, 
                    'fbm_sales': fbm_sales, 
                    'total_order_count': total_order_count, 
                    'order_pending_count': order_pending_count, 
                    'last_updated': last_updated, 
                    'shipped_order_count': shipped_order_count, 
                    'total_sales': total_sales,
                    'fba_pending_sales': fba_pending_sales,
                    'fbm_pending_sales': fbm_pending_sales,
                    'fbm_threshold': fbm_threshold
                    })

if __name__ == '__main__':
    app.run()