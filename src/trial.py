from flask import Flask, jsonify
from script import main

app = Flask(__name__)

# status = get_status(total_sales, order_count)

# Members API Route
@app.route('/members')
def members():
    status = main()  # Call the main function to execute the code
    total_sales = status['total_sales']  # Extract the total sales value from the dictionary
    order_count = status['order_count']  # Extract the order count value from the dictionary
    return jsonify({'total_sales': total_sales, 'order_count': order_count})

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
 