import logging
from flask import Flask, request, jsonify

app = Flask(__name__)

# ...existing code...

@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    message = data['message']
    logging.info(message)
    return jsonify({'status': 'Message logged'}), 200

# ...existing code...

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    app.run(debug=True)
