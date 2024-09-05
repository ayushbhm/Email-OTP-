import redis
import secrets
from flask import current_app
from datetime import timedelta

def get_redis_client():
    return redis.Redis.from_url(current_app.config['REDIS_URL'])

def generate_otp(user_id):
    redis_client = get_redis_client()
    otp = secrets.randbelow(100000)
    otp_str = f"{otp:05d}"
    key = f"otp:{user_id}"
    redis_client.setex(key,timedelta(minutes = 5),otp_str)
    
    return otp_str

def verify_otp(user_id, otp):
    redis_client = get_redis_client()
    key = f"otp:{user_id}"
    stored_otp = redis_client.get(key)
    if stored_otp and stored_otp.decode() == otp:
        redis_client.delete(key)  # Delete after successful verification
        return True
    return False

def is_rate_limited(user_id):
    redis_client = get_redis_client()
    key = f"otp_request:{user_id}"
    request_count = redis_client.get(key)
    if request_count is None:
        redis_client.setex(key, timedelta(hours=1), 1)
        return False
    if int(request_count) >= 5:  # Limit to 5 requests per hour
        return True
    redis_client.incr(key)
    return False