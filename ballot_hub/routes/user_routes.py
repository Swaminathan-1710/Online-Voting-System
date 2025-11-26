from flask import Blueprint, request, jsonify
from controllers.user_controller import register, login, list_elections, list_candidates, vote, check_vote_status
from database.connection import get_collection
from utils.phone_validator import normalize_phone, hash_phone

user_bp = Blueprint("user_bp", __name__)

# User routes
user_bp.add_url_rule("/api/register", view_func=register, methods=["POST"])
user_bp.add_url_rule("/api/login", view_func=login, methods=["POST"])
user_bp.add_url_rule("/api/elections", view_func=list_elections, methods=["GET"])
user_bp.add_url_rule("/api/candidates/<string:election_id>", view_func=list_candidates, methods=["GET"])
user_bp.add_url_rule("/api/vote", view_func=vote, methods=["POST"])
user_bp.add_url_rule("/api/vote_status/<string:election_id>", view_func=check_vote_status, methods=["GET"])

@user_bp.route("/api/check_availability", methods=["POST"])
def check_availability():
    """Check if email or phone is available (for debugging)"""
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    
    users = get_collection("users")
    result = {"email_available": True, "phone_available": True, "details": {}}
    
    if email:
        existing = users.find_one({"email": email})
        result["email_available"] = existing is None
        if existing:
            result["details"]["email_exists"] = True
            result["details"]["email_user_name"] = existing.get("name", "Unknown")
    
    if phone:
        normalized = normalize_phone(phone)
        hashed = hash_phone(normalized)
        existing = users.find_one({"phone_hash": hashed})
        result["phone_available"] = existing is None
        if existing:
            result["details"]["phone_exists"] = True
            result["details"]["phone_user_email"] = existing.get("email", "Unknown")
            result["details"]["phone_last4"] = existing.get("phone_last4", "XXXX")
    
    return jsonify(result), 200

