from flask import Flask, jsonify
from script import main

app = Flask(__name__)

# status = get_status(total_sales, order_count)

# Members API Route
@app.route('/members')
def members():
    status = main()  # Call the main function to execute the code
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
                    'fbm_pending_sales': fbm_pending_sales})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
 