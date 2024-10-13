from flask import Flask, request, jsonify
import logging

# Create Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Global variable to store the last received data
last_received_data = {}

@app.route('/blind/data', methods=['POST'])
def receive_data():
    global last_received_data  # Use the global variable

    # Get JSON data from request
    data = request.json

    # Validate that the data contains the required fields
    required_fields = ['distance', 'ir_value']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({'status': 'error', 'message': f'Missing fields: {", ".join(missing_fields)}'}), 400

    # Extract sensor data with default values
    distance = data.get('distance', 0)
    ir_value = data.get('ir_value', 1)  # Corrected from 'lr_value'

    # Store the received data in the global variable
    last_received_data = {
        'distance': distance,
        'ir_value': ir_value,
    }

    # Log received data (for debugging or later use)
    logging.info(f"Received data: Distance={distance}, IR={ir_value}")

    # Respond with success message
    return jsonify({'status': 'success', 'message': 'Data received successfully!'}), 200

@app.route('/blind/data', methods=['GET'])
def get_data():
    # Return the last received data
    return jsonify(last_received_data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
