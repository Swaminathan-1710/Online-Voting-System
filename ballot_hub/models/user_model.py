from typing import Optional, Dict, Any
import bcrypt
from pymongo.errors import DuplicateKeyError
from bson import ObjectId
from datetime import datetime
from database.connection import get_collection
from config import PASSWORD_HASH_ROUNDS


def _hash_password(plain_password: str) -> str:
    salt = bcrypt.gensalt(rounds=PASSWORD_HASH_ROUNDS)
    return bcrypt.hashpw(plain_password.encode("utf-8"), salt).decode("utf-8")


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def register_user(name: str, email: str, password: str, status: str = "pending") -> Dict[str, Any]:
    # Validate and normalize inputs
    email = email.lower().strip() if email else ""
    name = name.strip()
    
    if not email or '@' not in email:
        return {
            "success": False, 
            "message": "A valid email address is required"
        }
    if not name:
        return {
            "success": False, 
            "message": "Name is required"
        }
    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must be at least 6 characters"
        }
    
    # Hash password for security
    hashed_password = _hash_password(password)
    users = get_collection("users")
    
    # Check for existing approved user with this email (case-insensitive)
    existing_approved = users.find_one({
        "email": {"$regex": f"^{email}$", "$options": "i"},
        "status": "approved"
    })
    
    if existing_approved:
        return {
            "success": False, 
            "message": "This email is already registered. Please use a different email or log in.",
            "email_exists": True
        }
    
    # If we get here, we can register the new user
    try:
        user_data = {
            "name": name,
            "email": email,  # Store in lowercase
            "password": hashed_password,
            "status": status,
            "voted": False,
            "created_at": datetime.utcnow()
        }
        
        result = users.insert_one(user_data)
        
        return {
            "success": True, 
            "user_id": str(result.inserted_id),
            "message": "Registration successful. Please wait for admin approval.",
            "requires_approval": True
        }
        
    except Exception as e:
        error_msg = str(e).lower()
        if "duplicate key error" in error_msg:
            # Check if it's a pending user
            pending_user = users.find_one({
                "email": {"$regex": f"^{email}$", "$options": "i"},
                "status": "pending"
            })
            
            if pending_user:
                return {
                    "success": False,
                    "message": "This email is already registered and pending approval. Please wait for admin approval.",
                    "pending_approval": True
                }
            
            return {
                "success": False,
                "message": "This email is already registered. Please use a different email or log in.",
                "email_exists": True
            }
            
        return {
            "success": False, 
            "message": f"Registration failed: {str(e)}"
        }


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    users = get_collection("users")
    
    # Find user with case-insensitive email match
    user = users.find_one({
        "email": {"$regex": f"^{email}$", "$options": "i"}
    })
    
    if not user:
        return None
        
    if not _verify_password(password, user["password"]):
        return None
        
    # Add user_id and ensure consistent email case
    user["user_id"] = str(user["_id"])
    user["email"] = user["email"].lower()  # Ensure consistent case
    
    user.pop("_id", None)
    user.pop("password", None)
    return user


def mark_user_voted(user_id: str) -> bool:
    from bson.errors import InvalidId
    users = get_collection("users")
    try:
        users.update_one({"_id": ObjectId(user_id)}, {"$set": {"voted": True}})
    except (InvalidId, ValueError):
        raise ValueError(f"Invalid user_id: {user_id}")
    return True


def check_if_voted(user_id: str) -> bool:
    """Check if user has voted in any election (for backward compatibility)"""
    from bson.errors import InvalidId
    from database.connection import get_collection as get_coll
    votes = get_coll("votes")
    try:
        vote_count = votes.count_documents({"user_id": ObjectId(user_id)})
        return vote_count > 0
    except (InvalidId, ValueError):
        return False


def check_if_voted_in_election(user_id: str, election_id: str) -> bool:
    """Check if user has already voted in a specific election"""
    from bson.errors import InvalidId
    from database.connection import get_collection as get_coll
    votes = get_coll("votes")
    try:
        vote = votes.find_one({
            "user_id": ObjectId(user_id),
            "election_id": ObjectId(election_id)
        })
        return vote is not None
    except (InvalidId, ValueError):
        return False

