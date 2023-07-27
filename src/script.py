# Logging and Environment Setup 
import logging 
import logging.handlers 
import os 
from dotenv import load_dotenv 
 
# Amazon Seller API 
from sp_api.base import Marketplaces 
from sp_api.api import Orders 
from sp_api.api import Products 
 
# Data Manipulation and Analysis 
from collections import Counter 
from datetime import datetime, timedelta 

 
# Communication and Notification 
from sms import send_sms_via_email 

# Timezone Handling 
import pytz 
 
# JSON Handling 
import json 


load_dotenv()

# Get the current script's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    os.path.join(current_dir, "status.log"),
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
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

gmail_credentials = {
    "gmail_username": os.environ.get("GMAIL_USERNAME"),
    "gmail_password": os.environ.get("GMAIL_PASSWORD")
}

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
except KeyError:
    SOME_SECRET = "Token not available!"
    #logger.info("Token not available!")
    #raise




def calculate_total_sales(asin_counter, asins_list, client):
    price_total = 0
    total_sales = 0
    qty = 0

    if asins_list != [] and asin_counter:
        pricing_response = client.get_product_pricing_for_asins(asin_list=asins_list, item_condition='New')
        # Pending Product Pricing information
        for asin_data in pricing_response.payload:
            # print the asin data
            print(f'asin_data: {json.dumps(asin_data, indent=4)}')
            
            # Item is available for sale in my account
            if 'Offers'in asin_data['Product']:
                # extract price
                price = asin_data['Product']['Offers'][0]['BuyingPrice']['LandedPrice']['Amount']
                # extract quantity
                # print quantity of each asin
                # print(f'quantity of {asin_data["ASIN"]}: {qty}')
                # calculate total price
                price_total += (price * asin_counter[asin_data['ASIN']])
                # print total price
                print(f'price_total: {price_total}')

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
                    price_total += (buy_box_price * asin_counter[asin_data['ASIN']])
                    print(f'price_total: {price_total}')
                except Exception as e:
                    print(f'Offers not found: {e}')
                    continue
                

            total_sales += price_total

        return total_sales
    else:
        return 0



def get_asin_counter(order_ids, orders_client):
    asin_counter = Counter()

    for order in order_ids:
        # Initialize response
        response = orders_client.get_order_items(order_id=order)
        order_items = response.payload['OrderItems']

        # Add to counter object
        for item in order_items:
            asin_counter[item['ASIN']] += 1

    return asin_counter


# Define the function to check if total_sales reaches threshold & conditionally send text message based on pause_flag
def check_and_send_notifications(pause_flag, fba_sales, number, message, provider, sender_credentials, threshold):
    # If total_sales reaches threshold, send text message
    if fba_sales > threshold and not pause_flag:
        try:
            send_sms_via_email(number, message, provider, sender_credentials)
        except Exception as e:
            print(f'Error: {e}')
        # Set pause_flag to True to prevent subsequent notifications
        pause_flag = True


# Initialize the global variable
pause_flag = False


def main():
    # Access the global variable inside the main function
    global pause_flag

    # Print the token value
    logger.info(f"Token value: {SOME_SECRET}")
    # Set up the Sales API client
    orders_client = Orders(credentials=credentials, marketplace=Marketplaces.US)

            
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

        
    # Use the modified values in the API call
    response = orders_client.get_orders(
        CreatedAfter=start_date,
        CreatedBefore=end_date,
        MarketplaceIds=["ATVPDKIKX0DER"]
    )

    fba_order_ids = []
    fbm_order_ids = []
    order_count = 0
    shipped_order_count = 0
    order_pending_count = 0
    fba_sales = 0
    fbm_sales = 0
    
    number = '7742396843'
    message = 'Total sales has met the threshold of $60.'
    provider = 'Verizon'
    sender_credentials = (gmail_credentials['gmail_username'], gmail_credentials['gmail_password'])

    # Iterate over the orders and extract the order IDs
    for order in response.payload['Orders']:

        # print the order data
        print(f'order: {json.dumps(order, indent=4)}')
        
         # item is not pending, cancelled, or unfulfillable
        if 'OrderTotal' in order:
            shipped_order_count += 1
            order_count += 1
        # Orders are either fulfilled by Amazon (FBA) or fulfilled by Merchant (FBM)
            
            #extract FBA orders (AFN)
            if order['FulfillmentChannel'] == 'AFN' and 'OrderTotal' in order:
                fba_sales += float(order['OrderTotal']['Amount'])
                print(f'fba_sales: {fba_sales}')

            # extract FBM orders (MFN)
            elif order['FulfillmentChannel'] == 'MFN' and 'OrderTotal' in order:
                fbm_sales += float(order['OrderTotal']['Amount'])


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

    # get counter object of asins
    fbm_asin_counter = get_asin_counter(fbm_order_ids, orders_client)
    fba_asin_counter = get_asin_counter(fba_order_ids, orders_client)
     
    # print the asin counter
    print(f'fba_asin_counter: {fba_asin_counter}')
    print(f'fbm_asin_counter: {fbm_asin_counter}')

    # get asins list
    fba_asins = list(fba_asin_counter.keys())
    fbm_asins = list(fbm_asin_counter.keys())
    # print the asins list
    # print(f'asins: {asins}') 

    # grab products pricing information for pending orders
    products_client = Products(credentials=credentials, marketplace=Marketplaces.US)

    #calculate fbm sales
    fbm_pending_sales = calculate_total_sales(fbm_asin_counter, fbm_asins, products_client)

    #calculate fba sales
    fba_pending_sales = calculate_total_sales(fba_asin_counter,fba_asins, products_client)

    print(f'fbm_pending_sales: {fbm_pending_sales}')
    print(f'fba_pending_sales: {fba_pending_sales}')

    # add pending sales to total sales
    fba_sales += fba_pending_sales
    fbm_sales += fbm_pending_sales

    print(f'order_pending_count: {order_pending_count}')            
    print(f'total_sales: {fba_sales + fbm_sales}')
    print(f'fba_sales: {fba_sales}')
    print(f'fbm_sales: {fbm_sales}')
    print(f'shipped order count: {shipped_order_count}')
    print(f'total order count: {order_count}')
    print(f'eastern_timezone: {eastern_timezone}')
    print(f'end_date: {end_date}')
    print(f'start_date: {start_date}')

    # Set the threshold value
    threshold = 60

    # Check if total_sales reaches threshold & conditionally send text message based on pause_flag
    check_and_send_notifications(pause_flag, fba_sales, number, message, provider, sender_credentials, threshold)

    custom_format = "%B %d, %H:%M:%S"
    
    # Get the current timestamp when main() is called
    current_timestamp = datetime.now()

    # Format the timestamp
    current_timestamp = current_timestamp.strftime(custom_format)

    # Exit the function to pause the program
    return {
        'fba_pending_sales': [fba_pending_sales],
        'fbm_pending_sales': [fbm_pending_sales],
        'total_sales': [fbm_sales + fba_sales], 
        'fbm_sales': [fbm_sales],
        'fba_sales': [fba_sales],
        'shipped_order_count': [shipped_order_count],
        'order_pending_count': [order_pending_count],
        'total_order_count': [order_count],
        'last_updated': [current_timestamp]
    }


if __name__ == '__main__':
    main()
