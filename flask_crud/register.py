from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    
    username = request.json.get('username')
    phone = request.json.get('phone')
    password = request.json.get('password')
    email = request.json.get('email')

    
    if not username or not phone or not password or not email :
        return jsonify({'error': 'Missing required data'}), 400


    return jsonify({'message': 'User registered successfully'}), 201
