from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import random
from flask import Flask, request, jsonify
from utils.email_utils import send_email
import redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)
app = Flask(__name__)

app.config.from_object(Config)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
db = SQLAlchemy()
db.init_app(app)

    
from routes.auth import auth_bp
app.register_blueprint(auth_bp)
    

def generate_otp():
    return str(random.randint(100000, 999999))

@app.route('/send-otp', methods=['POST'])
def send_otp_route():
    data = request.json
    recipient = data.get('email')
    
    if recipient:
        otp = generate_otp()
        email_subject = "Your OTP for Login"
        email_body = f"Your OTP is: {otp}. It will expire in 5 minutes."
        
        # Store OTP in Redis with 5-minute expiration
        redis_client.setex(f"otp:{recipient}", 300, otp)
        
        send_email(email_subject, email_body, recipient)
        return jsonify({'message': 'OTP sent!'}), 200
    return jsonify({'message': 'Missing email!'}), 400

@app.route('/verify-otp', methods=['POST'])
def verify_otp_route():
    data = request.json
    email = data.get('email')
    user_otp = data.get('otp')
    
    if not email or not user_otp:
        return jsonify({'message': 'Missing email or OTP!'}), 400
    
    stored_otp = redis_client.get(f"otp:{email}")
    if stored_otp is None:
        return jsonify({'message': 'OTP expired or not found!'}), 400
    
    if user_otp == stored_otp.decode():
        redis_client.delete(f"otp:{email}")
        return jsonify({'message': 'OTP verified successfully!'}), 200
    else:
        return jsonify({'message': 'Invalid OTP!'}), 400


if __name__ == '__main__':
   
    with app.app_context():
        db.create_all()
    app.run(debug=True)