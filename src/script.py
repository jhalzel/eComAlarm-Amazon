# Logging and Environment Setup 
import logging 
import logging.handlers 
import os 
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv 
 
# Amazon Seller API 
from sp_api.base import Marketplaces 
from sp_api.api import Orders 
from sp_api.api import Products 
 
# Data Manipulation and Analysis 
from collections import Counter 
from datetime import datetime, timedelta 
import pandas as pd

# Flask Setup
from flask import current_app as app

# Firebase Setup
from firebase_admin import db
from trial import firebase_config

# Communication and Notification 
from sms import send_sms_via_email 

# Timezone Handling 
import pytz 
 
# JSON Handling 
import json 

# call reference to firebase config in trial.py
firebase_config


# Function to calculate total sales and price of each asin
def calculate_pending_sales(asin_counter, asins_list, client):
    total_sales = 0
    qty = 0

    if asins_list != [] and asin_counter:
        pricing_response = client.get_product_pricing_for_asins(asin_list=asins_list, item_condition='New')
        # Pending Product Pricing information
        for asin_data in pricing_response.payload:
            # print the asin data
            print(f'asin_data: {json.dumps(asin_data, indent=4)}')

            #print separator
            print('===============================')

            # Item is available for sale in my account
            if 'Offers'in asin_data['Product']:
                # extract price
                price = asin_data['Product']['Offers'][0]['BuyingPrice']['LandedPrice']['Amount']
                print(f'price: {price}')
                
                #print separator
                print('===============================')
            
                # extract quantity
                print(f'quantity of {asin_data["ASIN"]}: {asin_counter[asin_data["ASIN"]]}')
                # calculate total price
                total_sales += (price * asin_counter[asin_data['ASIN']])
                # print total price
                print(f'total pending sales: {total_sales}')

            # Item is no longer available for sale on my account
            else:
                qty += asin_counter[asin_data['ASIN']]
                print(f'quantity of {asin_data["ASIN"]}: {qty}')
                try: 
                    # get buy-box price listed on Amazon (if available)
                    newest_offer = client.get_item_offers(asin_data['ASIN'], item_condition='New').payload
                    # print(f'newest_offers: {json.dumps(newest_offer, indent=4)}')
                    buy_box_price = newest_offer['Summary']['BuyBoxPrices'][0]['LandedPrice']['Amount']
                    print(f'buy_box_price: {buy_box_price}')
                    total_sales += (buy_box_price * asin_counter[asin_data['ASIN']])
                    print(f'total unavailable on account: {total_sales}')
                except Exception as e:
                    print(f'Offers not found: {e}')
                    continue
                
                #print separator
                print('===============================')

        return total_sales
    else:
        return 0
    

# Function that creates and asin counter object
def get_asin_counter(order_ids, orders_client):
    # Initialize counter object
    asin_counter = Counter()

    for order in order_ids:
        # Initialize response
        response = orders_client.get_order_items(order_id=order)
        order_items = response.payload['OrderItems']

        # Add to counter object
        for item in order_items:
            asin_counter[item['ASIN']] += 1

    return asin_counter

flask_url = 'https://amazon-ecom-alarm.onrender.com/get_pause_status'

def get_pause_status():
    try:
        # Assuming your Flask app is running on localhost:5000
        
        response = requests.get(flask_url)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {'message': 'Failed to get pause status from Flask app'}, response.status_code

    except Exception as e:
        return {'message': f'Error: {str(e)}'}, 500  # Internal Server Error
    

    
def set_pause_status(status):
    try: 
        # flask_url = 'http://127.0.0.1:5000/set_pause_status'
        response = requests.post(flask_url, json=status)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return {'message': 'Failed to set pause status from Flask app'}, response.status_code
    except Exception as e:
        return {'message': f'Error: {str(e)}'}, 500


# Function to check if total_sales reaches threshold & conditionally send text message based on pause_flag
def check_and_send_notifications(pause_flag, fbm_sales, number, message, provider, sender_credentials, threshold):
    print('Check and Send Notifications')

    print(f'pause_flag: {pause_flag}')

    # type check for error handling
    if type(threshold) not in [float, int]:
        threshold = 0
        print('threshold is not a float or int')
    
    # If total_sales reaches threshold, send text message
    if fbm_sales >= threshold and pause_flag == False:
        print('Total sales has met the threshold!')
        try:
            send_sms_via_email(number, message, provider, sender_credentials)
        except Exception as e:
            print(f'Error: {e}')
      
        # Set pause_flag to True to prevent subsequent notifications
        pause_flag = True
        set_pause_status(pause_flag)

    elif fbm_sales < threshold and pause_flag == True:
        # Set pause_flag to False to allow notifications
        pause_flag = False
        set_pause_status(pause_flag)
    else:
        pass


def main():
    # Initialize pause_flag to False
    pause_flag = get_pause_status()

    print(f'pause_flag: {pause_flag}')
    print(f'type of pause_flag: {type(pause_flag)}')
    # Load the environment variables (secret keys set in .env file)
    load_dotenv()

    # Get the current script's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Set up the logger for the script
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(current_dir, "status.log"),
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )

    # Set the logging format
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)


    # Access credentials from the dictionary
    credentials = {
        "refresh_token": os.environ.get("SP_API_REFRESH_TOKEN"),
        "lwa_app_id": os.environ.get("LWA_APP_ID"),
        "lwa_client_secret": os.environ.get("LWA_CLIENT_SECRET"),
        "aws_access_key": os.environ.get("SP_API_ACCESS_KEY"),
        "aws_secret_key": os.environ.get("SP_API_SECRET_KEY"),
        "role_arn": os.environ.get("SP_API_ROLE_ARN")
    }

    # Access gmail credentials from the dictionary
    gmail_credentials = {
        "gmail_username": os.environ.get("GMAIL_USERNAME"),
        "gmail_password": os.environ.get("GMAIL_PASSWORD")
    }

    # Test the credentials with a sample secret
    try:
        SOME_SECRET = os.environ["SOME_SECRET"]
    except KeyError:
        SOME_SECRET = "Token not available!"
        #logger.info("Token not available!")
        #raise

    # Print the token value
    logger.info(f"Token value: {SOME_SECRET}")

    # Set up the Sales API client
    try:
        orders_client = Orders(credentials=credentials, marketplace=Marketplaces.US, timeout=10)
    except Exception as e:
        print(f'Error: {e}')

    # Get the current time in the Eastern timezone (US/Eastern)
    eastern_timezone = pytz.timezone("US/Eastern")
    current_time = datetime.now(eastern_timezone)

    # Check if daylight saving time (DST) is in effect for the current time
    is_dst = current_time.dst() != timedelta(0)

    # Adjust the timezone based on DST
    if is_dst:
        timezone_offset = "-04:00"  # Eastern Daylight Time (EDT) - UTC-4
    else:
        timezone_offset = "-05:00"  # Eastern Standard Time (EST) - UTC-5

    # Format the start_date and end_date with the adjusted timezone offset
    start_date = current_time.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=None).strftime(f"%Y-%m-%dT%H:%M:%S{timezone_offset}")
    adjusted_date = current_time - timedelta(minutes=3)
    end_date = adjusted_date.strftime(f"%Y-%m-%dT%H:%M:%S{timezone_offset}")

    # TO SET UP FOR 1 MONTH OF DATA
    # =============================
    # Set start date to June 1st, 2023
    # start_date = datetime(2023, 6, 1).strftime(f"%Y-%m-%dT%H:%M:%S{timezone_offset}")
    # Subtract 3 minutes from current time
    # adjusted_date = current_time - timedelta(minutes=3)
    # Set end date to July 31st, 2023
    # end_date = datetime(2023, 7, 31).strftime(f"%Y-%m-%dT%H:%M:%S{timezone_offset}")
        
    # Use the modified date values in the API call
    response = orders_client.get_orders(
        CreatedAfter=start_date,
        CreatedBefore=end_date,
        MarketplaceIds=["ATVPDKIKX0DER"]
    )

    # Initialize order data variables
    fba_order_ids = []
    fbm_order_ids = []
    order_count = 0
    shipped_order_count = 0
    order_pending_count = 0
    fba_sales = 0
    fbm_sales = 0

    # Initialize the phone number to send the text message to
    number = '7742396843'

    # Initialize the URL shortener for the text message
    link_url = 'https://apps.apple.com/us/app/amazon-seller/id794141485'
    link_text = "Visit Amazon Seller App"

    # message = f'Total sales has met the threshold of ${threshold}. Please check your Amazon Seller Central account: {anchor_tag}'
    message = ''
    provider = 'Verizon'
    sender_credentials = (gmail_credentials['gmail_username'], gmail_credentials['gmail_password'])

    # Initialize the order lists
    fbm_order_list = []
    fba_order_list = []

    # Iterate over the orders and extract the order IDs
    for order in response.payload['Orders']:
    
        # print the important details from the order data response
        # print order id
        print(f'Order id: {order["AmazonOrderId"]}')
        # print order status
        print(f'Order status: {order["OrderStatus"]}')
        # print fulfillment channel
        print(f'Fulfillment channel: {order["FulfillmentChannel"]}')
        # print order total
        if 'OrderTotal' in order:
            print(f'Order total: {order["OrderTotal"]}')
        else:
            print('Order total: None')

        # print separator
        print('===============================')


         # item is not pending, cancelled, or unfulfillable, means it's shipped
        if 'OrderTotal' in order:
            shipped_order_count += 1
            order_count += 1
        
        # Orders are either fulfilled by Amazon (AFN) or fulfilled by Merchant (MFN)            

            #extract FBA orders (AFN)
            if order['FulfillmentChannel'] == 'AFN' and 'OrderTotal' in order:
                fba_sales += float(order['OrderTotal']['Amount'])
                print(f'fba_sales: {fba_sales}')
                fba_order_list.append(order)

            # extract FBM orders (MFN)
            elif order['FulfillmentChannel'] == 'MFN' and 'OrderTotal' in order:
                fbm_sales += float(order['OrderTotal']['Amount'])
                fbm_order_list.append(order)

             # print separator
            print('===============================')


        # get pending orders' ids
        elif order['OrderStatus'] == 'Pending':
            order_pending_count += 1
            order_count += 1
            if order['FulfillmentChannel'] == 'MFN':
                # FBM PENDING ORDERS
                fbm_order_ids.append(order['AmazonOrderId'])

            elif order['FulfillmentChannel'] == 'AFN':
                # FBA PENDING ORDERS
                fba_order_ids.append(order['AmazonOrderId'])
        else:
            continue

         # print separator
        print('===============================')


    # get counter object of pending order asins
    fbm_pending_counter = get_asin_counter(fbm_order_ids, orders_client)
    fba_pending_counter = get_asin_counter(fba_order_ids, orders_client)
     
    # print the asin counter
    print(f'fba_pending_counter: {fba_pending_counter}')
    print(f'fbm_pending_counter: {fbm_pending_counter}')

    # get asins list
    fba_asins = list(fba_pending_counter.keys())
    fbm_asins = list(fbm_pending_counter.keys())
    # print the asins list

    # grab products pricing information for pending orders
    products_client = Products(credentials=credentials, marketplace=Marketplaces.US)

    # get total sales of FBA pending orders
    fba_pending_sales = calculate_pending_sales(fba_pending_counter, fba_asins, products_client)

    # get total sales of FBM pending orders
    fbm_pending_sales = calculate_pending_sales(fbm_pending_counter, fbm_asins, products_client) 

    # print all the data
    print(f'order_pending_count: {order_pending_count}')   
    print(f'fba_pending_sales: {fba_pending_sales}')
    print(f'fbm_pending_sales: {fbm_pending_sales}')         
    print(f'total_sales: {fba_sales + fbm_sales}')
    print(f'fba_sales: {fba_sales}')
    print(f'fbm_sales: {fbm_sales}')
    print(f'shipped order count: {shipped_order_count}')
    print(f'total order count: {order_count}')
    print(f'eastern_timezone: {eastern_timezone}')
    print(f'end_date: {end_date}')
    print(f'start_date: {start_date}')

    # timestamp format
    custom_format = "%B %d, %H:%M:%S"
    
    # Get the current timestamp when main() is called EST format
    current_timestamp = datetime.now(eastern_timezone)

    # Format the timestamp
    current_timestamp = current_timestamp.strftime(custom_format)

    # Check timestamp for EST
    print(f'current_timestamp: {current_timestamp}')

    # Get the current directory of the script file for threshold
    # config_file_path = os.path.join(current_dir, 'config.json')

    # with open(config_file_path, 'r') as file:
    #         config = json.load(file)
    #         threshold = config.get('fbm_threshold', 0)

    url = 'https://amazon-ecom-alarm.onrender.com/get_threshold'
    # url = 'http://127.0.0.1:5000/get_threshold'
    
    # Get the threshold value from the server 
    try:
        tresponse = requests.get(url)
        threshold = tresponse.json()['threshold']
        print('threshold: ', threshold)
        print("type of threshold: ", type(threshold))
        # Check the response status code
        # Check if threshold is a float
        threshold = int(threshold[0])

        print('data tresponse: ', tresponse)
        print('threshold: ', threshold)
     
    except Exception as e:
        print(f'Error: {e}')
        threshold = 999


    # collect data into a dataframe for the day
    data = {
        'fba_sales': [round(fba_sales,2)],
        'fbm_sales': [round(fbm_sales,2)],
        'total_order_count': [order_count],
        'order_pending_count': [order_pending_count],
        'shipped_order_count': [shipped_order_count],
        'fba_pending_sales': [round(fba_pending_sales,2)],
        'fbm_pending_sales': [round(fbm_pending_sales,2)],
        'total_sales': [round(fbm_sales, 2) + round(fba_sales, 2)],
        'threshold': [round(threshold, 2)],
        'date': [current_time.strftime("%m/%d/%Y")],
        'last_updated': [current_timestamp]
        }

    # convert data to json
    json_data = json.dumps(data)

    print('type of data to be saved: ', type(json_data))

    print('json_data: ', json_data)
    
    cur_date = data['date']
    print('cur_date: ', cur_date)

    # create a reference to the database
    ref = db.reference()

    # Retrieve existing data in the Firebase database
    firebase_db = ref.get()
    
    # if existing data is not None
    if firebase_db is not None:
        existing_data = [(key, value) for key, value in firebase_db.items()]
        # print('existing_data: ', existing_data)

        # Loop through each JSON string in the list and parse it
        for object in existing_data:
            # Parse the JSON string into a Python dictionary
            # print("Type of data is: ", type(object))
            # print('id: ', id)
            # print("object: ", object)

            for key, value in object[1].items():
                if key == 'date':
                    # print(f'{key}: {value}')
                    # print(type(value[0]))
                    if value[0] == cur_date[0]:
                        # print('date matches')
                        # update the data of the key with the new data
                        ref.child(object[0]).update(data)
    
            # spacers
            # print('===============================')

    else:
        # append the data from the data.json file
            # Specify the path to your JSON file
        file_path = os.path.join(current_dir, 'data.json')

        # Read the JSON data from the file
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
            print('json_data: ', json_data)

        for item in json_data:
            item = json.loads(item)
            print('item: ', item)
            
            # append the data to the database
            ref.push(item)    
            
    # get the dates from the database  
    dates = [d['date'] for d in firebase_db.values()]
    print('dates: ', dates)

    if cur_date not in dates:
        print("current date not in list of dates")
        # append json_data to firebase
        ref.push(data)
        

    # To read it back from Firebase
    print('Reading data from Firebase')
    # spacers
    print('===============================')
    # Retrieve the keys (names) of the data
    data_keys = data.keys() 

    # print separator
    print('===============================')
    print(f'threshold: {threshold}')

    threshold = float(round(threshold, 2))

    # Check if total_sales reaches threshold & conditionally send text message based on pause_flag
    check_and_send_notifications(pause_flag, fbm_sales, number, message, provider, sender_credentials, threshold)

    # Exit the function to pause the program
    return data


if __name__ == '__main__':
    main()

