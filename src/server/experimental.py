# Logging and Environment Setup 
import logging 
import logging.handlers 
import os 
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv 
import itertools
import time
import asyncio
# import aiohttp

# Amazon Seller API 
from sp_api.base import Marketplaces 
from sp_api.api import CatalogItems 
from sp_api.api import Products 
from sp_api.api import ProductFees

# Data Manipulation and Analysis 
from collections import Counter 
from datetime import datetime, timedelta 

# Flask Setup
# from flask import current_app as app
 
# JSON Handling 
import json 

# CSV DataFrames
import pandas as pd
import logging

# Import set_option from pandas
from pandas import set_option

# Set pandas display options using set_option
set_option('display.max_columns', None)  # Show all columns
set_option('display.width', 1000)        # Set the display width to avoid line breaks
set_option('display.max_colwidth', 20) # Show full content of each column
pd.set_option('display.colheader_justify', 'center')  # Center column headers
pd.set_option('display.float_format', '{:,.2f}'.format)  # Set float format



# Helper function to split a list into batches of a specified size
def split_into_batches(lst, batch_size):
    for i in range(0, len(lst), batch_size):
        yield lst[i:i + batch_size]


# Function to find item based on UPC
def find_item_by_upc(upc_list, costs_list, credentials):
    # Initialize lists for DataFrame
    images, upcs, asins, names, manufacturers, sales_ranks, costs, qtys, package_dimensions, weights = [], [], [], [], [], [], [], [], [], []

    # Initialize the SP-API client
    catalog_items_api = CatalogItems(
        credentials=credentials
    )   
    
    # print(f'upc_cost_zip {list(zip(upc_list, costs_list))}')
    i = 1
    for upc, cost in zip(upc_list, costs_list):
        print(f'upc: {upc}')
        try:
            # Use the Catalog Items API to search for the item by UPC
            response = catalog_items_api.search_catalog_items(
                keywords=upc,
                Marketplaces='ATVPDKIKX0DER',  # Replace with the appropriate marketplace ID(s)
                # includedData=['summaries', 'images', 'salesRanks', ]  # Include other data as needed
                includedData=['summaries', 'images', 'salesRanks' ]  # Include other data as needed
            )
            
            # Debugging: Print the entire response payload
            # print("Response payload:", response.payload)

            # Process the response payload
            items = response.payload.get('items', []) if response.payload else []

            if items:
                # Collect ranks
                ranked_items = []

                for item in items:
                    print(f'item: {item}')
                    if 'ranks' in item and 'ranks' in item['ranks'][0] and item['ranks'][0]['ranks']:
                        # print(f'item["ranks"]: {item["ranks"]}')
                        rank = item['ranks'][0]['ranks'][0]['rank']
                        ranked_items.append((rank, item))
                    else:
                        continue

                # Sort ranks in ascending order
                ranked_items.sort(key=lambda x: x[0])

                # Get data for only the three lowest-ranked items
                lowest_ranked_items = ranked_items[:3]

                # print(f'lowest ranked items: {lowest_ranked_items}')

                for rank, item in lowest_ranked_items:
                    sales_ranks.append(rank)
                    costs.append(float(cost))  # Assuming 'cost' is defined elsewhere
                    images.append(item['images'][0].get('link') if 'images' in item and item['images'][0].get('link') else '')
                    upcs.append(upc)  # Assuming 'upc' is defined elsewhere
                    asins.append(item['asin'])
                    names.append(item['summaries'][0].get('itemName') if 'summaries' in item and item['summaries'][0].get('itemName') else '')
                    manufacturers.append(item['summaries'][0].get('manufacturer') if 'summaries' in item and item['summaries'][0].get('manufacturer') else '')

                    # costs.append(float(cost))
                    # images.append(item['images'][0].get('images')[0].get('link') if item['images'][0].get('link') else '')
                    # upcs.append(upc)
                    # asins.append(item['asin'])
                    # names.append(item['summaries'][0].get('itemName') if item['summaries'][0].get('itemName') else '')
                    # manufacturers.append(item['summaries'][0].get('manufacturer') if item['summaries'][0].get('manufacturer') else '')
                    
                    

        except Exception as e:
            # Log the exception and continue with the next UPC
            # print(f"Error processing UPC {upc}: {e}")
            costs.append(0)
            # print('costs: ', costs)
            images.append('')
            upcs.append(upc)
            asins.append('')
            names.append('')
            manufacturers.append('')
            sales_ranks.append(float('Inf'))

        # Set a timer for every 2 UPCs
        if (i + 1) % 2 == 0:
            time.sleep(1)
        i += 1
    
    # Print lengths of arrays used in df
    # print(f"Length of images array: {len(images)}")
    # print(f"Length of upcs array: {len(upcs)}")
    # print(f"Length of asins array: {len(asins)}")
    # print(f"Length of names array: {len(names)}")
    # print(f"Length of names array: {len(costs)}")
    # print(f"Length of manufacturers array: {len(manufacturers)}")
    # print(f"Length of sales_ranks array: {len(sales_ranks)}")


            
    #Create the DataFrame once, after collecting all data
    df = pd.DataFrame({
        # 'Image': images,
        'UPC': upcs,
        'ASIN': asins,
        'Item Name': names,
        'Cost': costs,
        'Manufacturer': manufacturers,
        'Sales Rank': sales_ranks
    })
    
    return df
    
   

def find_competitive_pricing(asin_list):
    # Initialize lists for pricing DataFrame
    # prices, new_offer_counts    = [], []
    pricing_dict = {}

    # Initialize the SP-API client
    products_api = Products(
        credentials=credentials,
        marketplace=Marketplaces.US
    )

    list = split_into_batches(asin_list, 20)
    
    for batch in list:

        # print(f'length of batch: {len(batch)}')

        try:

            time.sleep(4)
            
            # Use the Catalog Items API to search for the item by UPC
            response = products_api.get_competitive_pricing_for_asins(
                asin_list=batch
            )

            products_pricing = response.payload
            # formatted_items = json.dumps(items, indent=4)

            # print(f'response length: {len(products_pricing)}')

            for product_data in products_pricing:

                time.sleep(0.01)

                try:
                    asin = product_data["ASIN"]
                    print(f'asin: {asin}')
                except (KeyError, IndexError): 
                    continue

                try:
                    # Extract the Landed Price
                    landed_price = product_data['Product']['CompetitivePricing']['CompetitivePrices'][0]['Price']['LandedPrice']['Amount'] 
                except (KeyError, IndexError):
                    landed_price = 0  # Default value if not found

                pricing_dict[asin] = [landed_price]

                # print(f'pricing_dict: {pricing_dict}')

                try:
                    # Extract the New Offer Count
                    offer_listings = product_data['Product']['CompetitivePricing']['NumberOfOfferListings']
                    new_offer_count = next((listing['Count'] for listing in offer_listings if listing['condition'] == "New"), 0)
                except (KeyError, IndexError, StopIteration):
                    new_offer_count = float('Inf')  # Default value if not found

                # new_offer_counts.append(new_offer_count)
                pricing_dict[asin].append(new_offer_count)

                # if landed_price == 0 and new_offer_count >= 1:
                #     asin = product_data["ASIN"]
                #     # Find the first offer's pricing
                #     try: 
                #         time.sleep(4)
                #         res = products_api.get_item_offers(
                #             asin=asin,
                #             item_condition='New'
                #         )

                #         missing_pricing = res.payload
                #         # print(f'Missing Pricing: {json.dumps(missing_pricing, indent=4)}')

                #         # Assuming the first item in the list is the desired item
                #         try:
                #             # Extract the Landed Price
                #             lowest_prices = missing_pricing["Summary"]["LowestPrices"]

                #             # List comprehension to extract all "LandedPrice" amounts
                #             landed_prices = [price["LandedPrice"]["Amount"] for price in lowest_prices]

                #             # Find the minimum price
                #             landed_price = min(landed_prices)
                #         except (KeyError, IndexError):
                #             landed_price = 0  # Default value if not found

                #     except (KeyError, IndexError, StopIteration):
                #         print("ERROR")
                    

                 # Append the extracted or default values to the lists
                # prices[len(prices) - 1] = landed_price

                # print('prices length: ', len(prices))
                # print('new_offer_counts length: ', len(new_offer_counts))

        except Exception as e:
            print(f"Error retrieving competitive pricing for batch: {e}")
            continue  # Skip to the next batch if an error occurs

        # Set a timer for every 2 UPCs

        
        # print(f'pricing dict: {pricing_dict}')

        # # Add a delay between each request to avoid hitting the quota limit
        # time.sleep(2)  # Wait for 2 seconds before the next iteration
    
    return pricing_dict


def format_for_fees(pricing_data):
    result = []
    for data in pricing_data:

        asin = data[0]
        pricing = data[1]

        result.append(dict(id_type='ASIN', id_value=asin, price=pricing, is_fba=True))
    
    # print(f'length of formatted fees: {len(result)}')

    return result


def getFees(fee_calculation_list):


    fees_dict = {
        # asin : (fee, referral_fee)
    }

    # print(type(fee_calculation_list))
    # print(type(fee_calculation_list[0]))

    try: 

        # Initialize the SP-API client
        fees_api = ProductFees(
            credentials=credentials,
            marketplace=Marketplaces.US
        )

    except Exception as e: 
        print(f'Could not parse fees_api: {e}')

    fee_lists = split_into_batches(fee_calculation_list, 20)

    # print(f'fee_lists: {fee_lists}')

    # for fee in fee_lists: 

    # count = 0
    for list in fee_lists:

        # print(f'list: {list}')

        try:
            time.sleep(4)

            # Use the Catalog Items API to search for the item by UPC
            response = fees_api.get_product_fees_estimate(
                estimate_requests=list
            )

            fees = response.payload

            # print(f'fees: {fees}')

            for fee in fees: 
                
                if "FeesEstimateIdentifier" in fee:
                    asin = fee["FeesEstimateIdentifier"]["IdValue"]
                    # print(f'asin: {asin}')
                    fees_dict[asin] = []
                else: 
                    continue

                if "FeesEstimate" in fee:

                    total_fees = fee["FeesEstimate"]["TotalFeesEstimate"]["Amount"]
                    fees_dict[asin].append(total_fees)

                    # print(f'fees_dict: {fees_dict} ')

                    if "FeeDetailList" in fee["FeesEstimate"]:
                        fee_detail_list = fee["FeesEstimate"]["FeeDetailList"]
                        # referral_fee = fee_detail_list[0].get("FeeAmount", {}).get("Amount", "N/A")
                        referral_fee = fee_detail_list[0]["FeeAmount"]["Amount"]
                    else:
                        referral_fee = 0

                    fees_dict[asin].append(referral_fee) 

            #     else:
            #         fees_dict[asin][0] = 0
            #         fees_dict[asin][1] = 0

        except Exception as e:
            print(f"Error retrieving catalog batch: {e}")


    # print(f"fees_dict: {fees_dict}")

    # print(f'total_fees_list: {total_fees_list}')
    # print(f'referal_fees_list: {referal_fees_list}')
    # print(f'total_fees_list length: {len(total_fees_list)}')
    # print(f'referal_fees_list length: {len(referal_fees_list)}')

    return fees_dict
    


# Access credentials from the dictionary
credentials = {
    "refresh_token": os.environ.get("SP_API_REFRESH_TOKEN"),
    "lwa_app_id": os.environ.get("LWA_APP_ID"),
    "lwa_client_secret": os.environ.get("LWA_CLIENT_SECRET"),
    "aws_access_key": os.environ.get("SP_API_ACCESS_KEY"),
    "aws_secret_key": os.environ.get("SP_API_SECRET_KEY"),
    "role_arn": os.environ.get("SP_API_ROLE_ARN")
}

def main():

    # Load the environment variables (secret keys set in .env file)
    load_dotenv()

    # Read the CSV file
    csv_file_path = './csv_files/test_batch.csv'  # Replace with the actual path to your CSV file
    df = pd.read_csv(csv_file_path)

    # Get the titles of the CSV columns
    csv_titles = df.columns.tolist()

    # Prompt the user to specify the column name
    item_id_column = input(f"Please enter the column name for UPCs (e.g., {csv_titles}): ")

    costs_column = input(f'Please enter the column name for Costs from {csv_titles}: ')

    # Extract the upc_list from the specified column
    if item_id_column in df.columns and costs_column in df.columns:
         # Filter out rows where either column has missing values
        filtered_df = df[[item_id_column, costs_column]].dropna()

        # UPC's
        upc_list = filtered_df[item_id_column].tolist()

        # Remove missing UPCs and ensure UPCs are strings to preserve leading zeros
        upc_list = [str(int(upc)).zfill(12) for upc in upc_list if pd.notna(upc)]
        
        # Cost's
        costs_list = filtered_df[costs_column].tolist()

        # print("UPCs and Costs have been extracted successfully!")
        # print("UPCs:", upc_list)
        # print("Costs:", costs_list)

    else:
        if item_id_column not in df.columns:
            print(f"Column '{item_id_column}' not found in the CSV file.")
        if costs_column not in df.columns:
            print(f"Column '{costs_column}' not found in the CSV file.")

    costs_list = [float(cost.strip('$')) if isinstance(cost, str) else float(cost) for cost in costs_list]    

    # print('costs_list: ', costs_list)
    # CREATE KEYWORD LIST TO USE IN CASE UPC LIST DOESN"T WORK

    # upc_list = ['766218005632','017158260323','075691739607','733739070234','733739023810','733739004819','733739074232','733739070227','733739076656','733739022486','733739001399','733739056955','733739042361','733739042217','733739002129','733739081025','733739079060','733739021854', '733739070746', '733739031594']

    # print('upc_list: ', upc_list )
   
    upc_asin_map = find_item_by_upc(upc_list, costs_list, credentials=credentials)

    # upc_asin_map['Costs'] = costs_list

    # print('items: ', upc_asin_map)
    # pd.display(upc_asin_map)
    # print('asins:', asins)

    # # Merge ASINs onto the DataFrame of UPCs
    # # df = pd.DataFrame([(upc, asin) for upc, asins in upc_asin_map.items() for asin in asins], columns=['UPC', 'ASIN'])

    # # Print the merged DataFrame
    # # ispdisplay(df

    asins = upc_asin_map['ASIN']

    # print('asins: ', asins)
   
    # # asins = ['B0002APS0A','B00119SXJ4','B003JW69B0','B003FBRVHQ','B00J7G9Z7C','B01IA96R86','B01IA96TMU','B01IA96VQO','B01IA96YZW','B01IA9799W','B00IEFJSQK','B0029PT4KG','B0002APS0A','B00119SXJ4','B003JW69B0','B003FBRVHQ','B00J7G9Z7C','B01IA96R86','B01IA96TMU','B01IA96VQO','B01IA96YZW','B01IA9799W','B00IEFJSQK','B0029PT4KG']

    pricing = find_competitive_pricing(asin_list=asins)

    # print('pricing:', pricing)
    # print(f'pricing length: {len(pricing)}')
    # print('new offer count:', offers)
    # print(f'new_offer length: {len(offers)}')

    df = upc_asin_map

    # Add 'Listing Price' and 'New Offer Count' to the DataFrame
    df['Listing Price'] = df['ASIN'].apply(lambda x: pricing[x][0] if x in pricing else None)
    df['New Offer Count'] = df['ASIN'].apply(lambda x: pricing[x][1] if x in pricing else None)

    print(df)

    # upc_asin_map['Listing Price'] = pricing``
    # upc_asin_map['New Offer Count'] = offers

    # # Display the upc_asin_map DataFrame
    # print(upc_asin_map)

    # Creating a list of tuples (ASIN, Listing Price, New Offer Count)
    pricing_data = [(asin, values[0]) for asin, values in pricing.items()]

    # print(f'pricing_data: {pricing_data}')
 
    # pricing_data = list(zip(pricing, asins))
    # pricing_data = list(pricing_data)


    # print(f'pricing_data: {pricing_data}')

    fee_calculation_list = format_for_fees(pricing_data)

    # print(f'fee_calculation_list: {fee_calculation_list}')

    # print('fee_calc_format: ', json.dumps(fee_calculation_list, indent=4))

    # # estimate_requests = [
    # # {
    # #     'id_type': 'ASIN',
    # #     'id_value': 'B012345678',
    # #     'price': '50'
    # # },
    # # {
    # #     'id_type': 'ASIN',
    # #     'id_value': 'B012345678',
    # #     'price': '50'
    # # }
    # # ]

    # # print(f'New Request: {json.dumps(requests, indent=4)}')

    # # Convert the list to a JSON string
    # # estimate_requests_json = json.dumps(estimate_requests)

    fee_dict = getFees(fee_calculation_list)

    print(f'fee_dict: {fee_dict}')
    
    # Correct the lambda functions to properly check the presence of ASIN in fee_dict and handle empty strings
    df['FBA Fees'] = df['ASIN'].apply(lambda x: fee_dict[x][0] if x and x in fee_dict and fee_dict[x] else None)
    df['FBM Fees'] = df['ASIN'].apply(lambda x: fee_dict[x][1] if x and x in fee_dict and len(fee_dict[x]) > 1 else None)

    # print(f'first df:\n {df}\n')

    # Fields: UPC, ASIN, Name, Sell Price, Buy Price, Fees, Profit 

    df['FBA Fees'] = pd.to_numeric(df['FBA Fees'], errors='coerce')
    df['Cost'] = pd.to_numeric(df['Cost'], errors='coerce')
    df['Total Costs'] = df['FBA Fees'] + upc_asin_map['Cost']
    df['Net Profit'] = df['Listing Price'] - upc_asin_map['Total Costs']
    df['ROI (%)'] = df.apply(lambda row: f"{(row['Net Profit'] / row['Cost']):.2%}" if row['Cost'] != 0 else "N/A", axis=1)


    print(f'final df:\n {df}\n')

    # Export upc_asin_map to CSV
    output_file_path = './csv_file/test_sample.csv'  # Replace with the desired output file path
    df.to_csv(output_file_path, index=False)
    print(f"Exported upc_asin_map to {output_file_path}")


if __name__ == '__main__':
    main()

