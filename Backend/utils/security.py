from werkzeug.security import generate_password_hash as werkzeug_generate_password_hash
from werkzeug.security import check_password_hash as werkzeug_check_password_hash
from flask_jwt_extended import create_access_token as jwt_create_access_token

def generate_password_hash(password):
    return werkzeug_generate_password_hash(password)

def check_password_hash(pwhash, password):
    return werkzeug_check_password_hash(pwhash, password)

def generate_token(user_id):
    return jwt_create_access_token(identity=user_id)