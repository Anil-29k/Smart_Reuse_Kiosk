import requests

BASE_URL = "http://127.0.0.1:8000"  # backend

def register_user(name, email, password):
    data = {"name": name, "email": email, "password": password}
    response = requests.post(f"{BASE_URL}/register", json=data)
    return response.json()

def login_user(email, password):
    data = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=data)
    return response.json()

def scan_qr(user_id, qr_data):
    data = {"user_id": user_id, "qr_code": qr_data}
    response = requests.post(f"{BASE_URL}/scan_qr", json=data)
    return response.json()

def get_dashboard(user_id):
    response = requests.get(f"{BASE_URL}/dashboard/{user_id}")
    return response.json()

def get_leaderboard():
    response = requests.get(f"{BASE_URL}/leaderboard")
    return response.json()

def redeem_coupon(user_id, coupon_id):
    data = {"user_id": user_id, "coupon_id": coupon_id}
    response = requests.post(f"{BASE_URL}/redeem_coupon", json=data)
    return response.json()