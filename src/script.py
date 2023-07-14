from config import credentials
from sp_api.base import Marketplaces
from sp_api.api import Orders
from datetime import datetime, timedelta
from sms import send_sms_via_email
from twilio_config import gmail_credentials
import pytz
import json
import schedule
import time

def main():
    # Set up the Sales API client
    orders_client = Orders(credentials=credentials, marketplace=Marketplaces.US)

    # get Pacific Time current date
    local_date = datetime.now(pytz.timezone("US/Pacific"))

    # UTC time zone
    current_date = datetime.now().astimezone(pytz.utc)
    adjusted_date = current_date - timedelta(minutes=3)

    onedayago = local_date - timedelta(days=2)
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

    order_ids = []
    order_count = 0
    total_sales = 0

    number = '7742396843'
    message = 'Total sales has met the threshold of $60.'
    provider = 'Verizon'
    sender_credentials = (gmail_credentials['gmail_username'], gmail_credentials['gmail_password'])

    # Iterate over the orders and extract the order IDs
    for order in response.payload['Orders']:
        #filter out orders that are not fulfilled by Amazon
        # if order['FulfillmentChannel'] != 'AFN': 
        order_ids.append(order['AmazonOrderId'])
        order_count += 1
        print(f'order: {json.dumps(order, indent=4)}')
        if 'OrderTotal' in order:
            sale = float(order['OrderTotal']['Amount'])
            total_sales += sale
    print(f'total_sales: {total_sales}')
    print(f'order_count: {order_count}')


    # If total_sales reaches threshold, send text message
    if total_sales > 60:
        try:
            send_sms_via_email(number, message, provider, sender_credentials)
        except Exception as e:
            print(f'Error: {e}')


    # Exit the function to pause the program
    return {
        'total_sales': [total_sales],
        'order_count': [order_count]
    }

   
def run_program():
    # Run the main function every 5 minutes
    schedule.every(20).seconds.do(main)

    while True:
        schedule.run_pending()
        time.sleep(5)


if __name__ == '__main__':
    run_program()
