from flask import Blueprint, request, jsonify

from models.user import User,db
import random
import string
import hashlib
import jwt
import datetime
import redis

auth_bp = Blueprint('auth', __name__)

# Secret key for JWT
SECRET_KEY = "your_secret_key_here"

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Mock Email Service Function
def send_email(email, otp):
    print(f"Sending OTP {otp} to email {email}")

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))

@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"message": "Email is required."}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email is already registered."}), 400

    new_user = User(email=email, password=hashlib.sha256('dummy_password'.encode()).hexdigest())
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful. Please verify your email."}), 201

@auth_bp.route('/api/request-otp', methods=['POST'])
def request_otp():
    data = request.get_json()
    email = data.get('email')

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "Email not registered."}), 400

    otp = generate_otp()

    # Store OTP in Redis with an expiry time of 5 minutes (300 seconds)
    redis_client.setex(email, 300, otp)
    
    send_email(email, otp)
    return jsonify({"message": "OTP sent to your email."}), 200

@auth_bp.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    email = data.get('email')
    otp = data.get('otp')

    stored_otp = redis_client.get(email)

    if not stored_otp:
        return jsonify({"message": "OTP has expired or was not requested."}), 400

    if stored_otp != otp:
        return jsonify({"message": "Invalid OTP."}), 400

    # Generate JWT token
    token = jwt.encode({
        'email': email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, SECRET_KEY, algorithm='HS256')

    # Optionally, delete the OTP from Redis after successful verification
    redis_client.delete(email)

    return jsonify({"message": "Login successful.", "token": token}), 200