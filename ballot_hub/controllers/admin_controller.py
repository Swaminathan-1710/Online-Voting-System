from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt
from bson import ObjectId
from bson.errors import InvalidId
from models.admin_model import admin_login as admin_auth
from database.connection import get_collection
from models.candidate_model import add_candidate as model_add_candidate
from models.election_model import (
    create_election as model_create_election,
    get_all_elections,
    update_election_status as model_update_election_status,
    delete_election as model_delete_election
)
from models.votes_model import count_votes
from datetime import datetime


def admin_login():
    data = request.get_json() or {}
    username = data.get("username", "").strip()
    password = data.get("password", "")
    admin = admin_auth(username, password)
    if not admin:
        return jsonify({"error": "Invalid admin credentials"}), 401
    token = create_access_token(identity=admin["admin_id"], additional_claims={"role": "admin", "admin_id": admin["admin_id"]})
    return jsonify({"access_token": token, "admin": {"admin_id": admin["admin_id"], "username": admin["username"]}}), 200


@jwt_required()
def approve_user(user_id: str):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    users = get_collection("users")
    try:
        users.update_one({"_id": ObjectId(user_id)}, {"$set": {"status": "approved"}})
    except InvalidId:
        return jsonify({"error": "Invalid user id"}), 400
    return jsonify({"message": "User approved"}), 200


@jwt_required()
def add_candidate():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    election_id = (data.get("election_id") or "").strip()
    photo = data.get("photo", "").strip()
    if not name or not election_id:
        return jsonify({"error": "name and election_id required"}), 400
    try:
        model_add_candidate(name, election_id, photo)
    except (InvalidId, ValueError) as e:
        return jsonify({"error": f"Invalid election id: {str(e)}"}), 400
    return jsonify({"message": "Candidate added"}), 201


@jwt_required()
def create_election():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json() or {}
    name = data.get("election_name", "").strip()
    start_date = data.get("start_date", "").strip()  # format: 'YYYY-MM-DD HH:MM:SS'
    end_date = data.get("end_date", "").strip()
    status = data.get("status", "active").strip()
    if not name or not start_date or not end_date:
        return jsonify({"error": "election_name, start_date, end_date required"}), 400
    if status not in ("active", "inactive"):
        status = "active"
    try:
        model_create_election(name, start_date, end_date, status)
    except ValueError as e:
        return jsonify({"error": f"Invalid date format: {str(e)}. Expected format: YYYY-MM-DD HH:MM:SS"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to create election: {str(e)}"}), 500
    return jsonify({"message": "Election created"}), 201


@jwt_required()
def list_users():
    """List all users (for admin to see pending approvals)"""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    users = get_collection("users")
    user_list = []
    for user in users.find({}, {"password": 0}):  # Exclude sensitive data
        user_list.append({
            "user_id": str(user["_id"]),
            "name": user.get("name", ""),
            "email": user.get("email", ""),
            "status": user.get("status", "pending"),
            "voted": user.get("voted", False)
        })
    return jsonify({"users": user_list}), 200


@jwt_required()
def list_all_elections():
    """List all elections (for admin to select when adding candidates)"""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    elections = get_all_elections()
    return jsonify({"elections": elections}), 200


@jwt_required()
def election_results(election_id: str):
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    try:
        results = count_votes(election_id)
    except (InvalidId, ValueError) as e:
        return jsonify({"error": f"Invalid election id: {str(e)}"}), 400
    return jsonify({"results": results}), 200


@jwt_required()
def update_election():
    """Update election status (active/inactive)"""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    data = request.get_json() or {}
    election_id = data.get("election_id", "").strip()
    status = data.get("status", "").strip().lower()
    
    if not election_id or not status:
        return jsonify({"error": "election_id and status required"}), 400
    
    if status not in ("active", "inactive"):
        return jsonify({"error": "status must be 'active' or 'inactive'"}), 400
    
    try:
        success = model_update_election_status(election_id, status)
        if success:
            return jsonify({"message": f"Election status updated to {status}"}), 200
        else:
            return jsonify({"error": "Election not found or status unchanged"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to update election: {str(e)}"}), 500


@jwt_required()
def delete_election(election_id: str):
    """Delete an election and its associated data"""
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
    
    try:
        result = model_delete_election(election_id)
        if result.get("success"):
            return jsonify({"message": result.get("message", "Election deleted successfully")}), 200
        else:
            return jsonify({"error": result.get("message", "Failed to delete election")}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to delete election: {str(e)}"}), 500


@jwt_required()
def reject_user(user_id: str):
    """
    Reject a pending user registration (admin only)
    This will delete the user account and any associated data
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    users = get_collection("users")
    
    try:
        # Only allow rejecting pending users
        user = users.find_one({"_id": ObjectId(user_id), "status": "pending"})
        if not user:
            return jsonify({"error": "Pending user not found or already processed"}), 404
        
        # Delete the user
        result = users.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "User not found or already deleted"}), 404
            
        return jsonify({"message": "User registration rejected and account deleted"}), 200
        
    except InvalidId:
        return jsonify({"error": "Invalid user ID"}), 400
    except Exception as e:
        return jsonify({"error": f"Error rejecting user: {str(e)}"}), 500


@jwt_required()
def delete_user(user_id: str):
    """
    Delete a user and their associated votes
    """
    claims = get_jwt()
    if claims.get("role") != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    users = get_collection("users")
    votes = get_collection("votes")
    
    try:
        # First, check if user exists
        user = users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        # If user has already voted, we need to update the vote counts
        user_votes = list(votes.find({"user_id": str(user["_id"])}))
        
        # Delete the user's votes
        votes.delete_many({"user_id": str(user["_id"]), "is_counted": True})
        
        # Mark votes as not counted in the vote counts
        for vote in user_votes:
            if vote.get("is_counted", False):
                # This part would need to be adjusted based on your voting system
                # You might need to decrement vote counts for the candidates
                pass
        
        # Now delete the user
        result = users.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "User not found or already deleted"}), 404
            
        return jsonify({"message": "User and their votes have been deleted"}), 200
        
    except InvalidId:
        return jsonify({"error": "Invalid user ID"}), 400
    except Exception as e:
        return jsonify({"error": f"Error deleting user: {str(e)}"}), 500
