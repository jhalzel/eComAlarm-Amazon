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



def main():
    logger.info(f"Token value: {SOME_SECRET}")
    # Set up the Sales API client
    orders_client = Orders(credentials=credentials, marketplace=Marketplaces.US)

    # get Pacific Time current date
    # local_date = datetime.now(pytz.timezone("US/Pacific"))

    # UTC time zone
    current_date = datetime.now().astimezone(pytz.utc)
    adjusted_date = current_date - timedelta(minutes=3)
    eastern_date = datetime.now(pytz.timezone("US/Eastern"))
    # hours_from_midnight = (eastern_date - eastern_date.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds() / 3600.0
    

    # adjust for Eastern time by adding 4 hours
    onedayago = current_date - timedelta(hours=23, minutes=30, seconds=59)
    # print(f"current_date: {current_date}")  
    # print(f"onedayago: {onedayago}")

    start_date = onedayago.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_date = adjusted_date.strftime("%Y-%m-%dT%H:%M:%SZ")

    # Use the modified values in the API call
    response = orders_client.get_orders(
        CreatedAfter=start_date,
        CreatedBefore=end_date,
        MarketplaceIds=["ATVPDKIKX0DER"]
    )

    fba_order_ids = []
    fbm_order_ids = []
    order_count = 0
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
            order_count += 1
        # Orders are either fulfilled by Amazon (FBA) or fulfilled by Merchant (FBM)
            
            #extract FBA orders (AFN)
            if order['FulfillmentChannel'] == 'AFN' and 'OrderTotal' in order:
                fba_sales += float(order['OrderTotal']['Amount'])

            # extract FBM orders (MFN)
            elif order['FulfillmentChannel'] == 'MFN' and 'OrderTotal' in order:
                fbm_sales += float(order['OrderTotal']['Amount'])


        # get pending orders' ids
        elif order['OrderStatus'] == 'Pending':
            order_pending_count += 1
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
    fbm_sales = calculate_total_sales(fbm_asin_counter, fbm_asins, products_client)

    #calculate fba sales
    fba_sales = calculate_total_sales(fba_asin_counter,fba_asins, products_client)

    

    print(f'fbm_sales: {fbm_sales}')
    print(f'fba_sales: {fba_sales}')
   
    # add price_total to total_sales                
    # total_sales += price_total
    
    print(f'order_pending_count: {order_pending_count}')            
    print(f'total_sales: {fba_sales}')
    print(f'fba_sales: {fba_sales}')
    print(f'fbm_sales: {fbm_sales}')
    print(f'order_count: {order_count}')
    print(f'current_date: {current_date}')
    print(f'eastern_date: {eastern_date}')
    print(f'one_day_ago: {onedayago}')


    # If total_sales reaches threshold, send text message
    if fbm_sales > 60:
        try:
            send_sms_via_email(number, message, provider, sender_credentials)
        except Exception as e:
            print(f'Error: {e}')
    
    # Get the current timestamp when main() is called
    current_timestamp = datetime.now().strftime("%m - %d %H:%M:%S")

    # Exit the function to pause the program
    return {
        'fbm_sales': [fbm_sales],
        'fba_sales': [fba_sales],
        'order_pending_count': [order_pending_count],
        'order_count': [order_count],
        'last_updated': [current_timestamp]
    }

   
# def run_program():
#     # Run the main function every 5 minutes
#     schedule.every(20).seconds.do(main)

#     while True:
#         schedule.run_pending()
#         time.sleep(5)


if __name__ == '__main__':
    main()
