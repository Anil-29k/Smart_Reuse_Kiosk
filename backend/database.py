from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import hashlib

# ---------------- MONGO CONNECTION ----------------
client = MongoClient("mongodb://localhost:27017/")
db = client["waste_management"]
users_col = db["users"]
transactions_col = db["transactions"]  # store QR scans / points history

# ---------------- HELPER FUNCTIONS ----------------
def hash_password(password: str) -> str:
    """Simple hash for storing passwords."""
    return hashlib.sha256(password.encode()).hexdigest()

# ---------------- USER FUNCTIONS ----------------
def register_user(name: str, email: str, password: str):
    """Register a new user."""
    if users_col.find_one({"email": email}):
        return {"error": "User already exists"}
    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "points": 0.0,
        "created_at": datetime.utcnow()
    }
    result = users_col.insert_one(user)
    return {"msg": "User registered successfully", "user_id": str(result.inserted_id)}

def login_user(email: str, password: str):
    """Login user."""
    user = users_col.find_one({"email": email})
    if not user:
        return {"error": "User not found"}
    if user["password"] != hash_password(password):
        return {"error": "Incorrect password"}
    return {"success": True, "user_id": str(user["_id"])}

def add_points(user_id: str, points_to_add: float, source: str = "QR Scan"):
    """Add points to a user account."""
    user = users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        return {"error": "User not found"}

    # Update points
    users_col.update_one({"_id": ObjectId(user_id)}, {"$inc": {"points": points_to_add}})
    new_user = users_col.find_one({"_id": ObjectId(user_id)})

    # Record transaction
    transactions_col.insert_one({
        "user_id": ObjectId(user_id),
        "points": points_to_add,
        "source": source,
        "timestamp": datetime.utcnow()
    })

    return {"total_points": new_user["points"]}

def get_user(user_id: str):
    """Get user details (without password)."""
    user = users_col.find_one({"_id": ObjectId(user_id)}, {"password": 0})
    if not user:
        return {"error": "User not found"}
    user["user_id"] = str(user["_id"])
    del user["_id"]
    return user

def get_leaderboard(top_n: int = 10):
    """Return top users by points."""
    users = users_col.find({}, {"password": 0}).sort("points", -1).limit(top_n)
    leaderboard = []
    for user in users:
        leaderboard.append({
            "user_id": str(user["_id"]),
            "name": user["name"],
            "points": user["points"]
        })
    return leaderboard