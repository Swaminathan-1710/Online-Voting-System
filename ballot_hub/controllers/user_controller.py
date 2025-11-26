from flask import request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from bson.errors import InvalidId
from bson import ObjectId
from datetime import datetime
from passlib.hash import bcrypt
from models.user_model import register_user, authenticate_user, check_if_voted_in_election
from models.election_model import get_all_active_elections
from models.candidate_model import get_candidates
from models.votes_model import record_vote
from database.connection import get_collection


def _hash_password(password: str) -> str:
    """Hash a password for storing."""
    return bcrypt.hash(password)



def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Basic validation
    if not all([name, email, password]):
        return jsonify({
            "error": "Name, email, and password are required"
        }), 400

    # Check if email already exists (case-insensitive)
    users = get_collection("users")
    existing_user = users.find_one({
        "email": {"$regex": f"^{email}$", "$options": "i"}
    })

    if existing_user:
        if existing_user.get("status") == "pending":
            return jsonify({
                "error": "This email is already registered and pending approval. Please wait for admin approval."
            }), 409
        else:
            return jsonify({
                "error": "This email is already registered. Please use a different email or log in."
            }), 409

    # If we get here, the email is available for registration
    try:
        # Hash the password
        hashed_password = _hash_password(password)
        
        # Create new user
        result = users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_password,
            "status": "pending",
            "voted": False,
            "created_at": datetime.utcnow()
        })

        return jsonify({
            "message": "Registration successful. Please wait for admin approval.",
            "requires_approval": True
        }), 201

    except Exception as e:
        return jsonify({
            "error": f"Registration failed: {str(e)}"
        }), 500
def login():
    """
    Step 1: Verify email and password
    Returns user info and triggers OTP generation
    """
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    step = data.get("step", "1")  # Step 1: verify credentials, Step 2: verify OTP
    
    # Step 1: Verify credentials and send OTP
    if step == "1":
        user = authenticate_user(email, password)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
        if user["status"] != "approved":
            return jsonify({"error": "User not approved yet"}), 403
        
        # Generate and send OTP to user's email
        from models.otp_model import generate_and_send_otp
        user_email = user.get("email", email)
        user_name = user.get("name", "User")
        
        otp_result = generate_and_send_otp(user["user_id"], user_email, user_name)
        
        if not otp_result.get("success"):
            return jsonify({"error": otp_result.get("message", "Failed to send OTP")}), 500
        
        # Mask email for display (e.g., u***@example.com)
        email_parts = user_email.split("@")
        if len(email_parts) == 2:
            masked_email = f"{email_parts[0][0]}***@{email_parts[1]}"
        else:
            masked_email = user_email
        
        return jsonify({
            "step": 1,
            "message": "OTP sent to your registered email address",
            "user_id": user["user_id"],
            "email_masked": masked_email,
            "expires_in": otp_result.get("expires_in", 5)
        }), 200
    
    # Step 2: Verify OTP and issue token
    elif step == "2":
        user_id = data.get("user_id", "")
        otp = data.get("otp", "").strip()
        
        if not user_id or not otp:
            return jsonify({"error": "user_id and otp required"}), 400
        
        # Verify OTP
        from models.otp_model import verify_user_otp
        if not verify_user_otp(user_id, otp):
            return jsonify({"error": "Invalid or expired OTP"}), 401
        
        # Get user details
        from database.connection import get_collection
        from bson import ObjectId
        users = get_collection("users")
        
        try:
            user_id_obj = ObjectId(user_id)
        except:
            return jsonify({"error": "Invalid user ID"}), 400
        
        user = users.find_one({"_id": user_id_obj}, {"name": 1, "email": 1, "status": 1})
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        if user.get("status") != "approved":
            return jsonify({"error": "User not approved yet"}), 403
        
        # Generate JWT token
        token = create_access_token(
            identity=user_id,
            additional_claims={
                "role": "user",
                "user_id": user_id,
                "email": user.get("email", "")
            }
        )
        
        return jsonify({
            "access_token": token,
            "user": {
                "user_id": user_id,
                "name": user.get("name", ""),
                "email": user.get("email", "")
            }
        }), 200
    
    else:
        return jsonify({"error": "Invalid step"}), 400


@jwt_required()
def list_elections():
    """List all active elections"""
    active_elections = get_all_active_elections()
    return jsonify({"elections": active_elections}), 200


@jwt_required()
def list_candidates(election_id: str):
    try:
        candidates = get_candidates(election_id)
    except (InvalidId, ValueError) as e:
        return jsonify({"error": f"Invalid election id: {str(e)}"}), 400
    return jsonify({"candidates": candidates}), 200


@jwt_required()
def check_vote_status(election_id: str):
    """Check if the current user has voted in a specific election"""
    claims = get_jwt()
    if claims.get("role") != "user":
        return jsonify({"error": "Unauthorized"}), 403
    user_id = get_jwt_identity()
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 403
    
    from models.user_model import check_if_voted_in_election
    has_voted = check_if_voted_in_election(user_id, election_id)
    return jsonify({"has_voted": has_voted, "election_id": election_id}), 200


@jwt_required()
def vote():
    try:
        # Authentication and input validation
        claims = get_jwt()
        if claims.get("role") != "user":
            return jsonify({"error": "Unauthorized: Only users can vote"}), 403
            
        user_id = get_jwt_identity()
        if not user_id:
            return jsonify({"error": "Unauthorized: Invalid user session"}), 403

        data = request.get_json() or {}
        candidate_id = data.get("candidate_id")
        election_id = data.get("election_id")
        
        if not candidate_id or not election_id:
            return jsonify({"error": "Both candidate_id and election_id are required"}), 400

        # Check if user has already voted in this election
        if check_if_voted_in_election(user_id, election_id):
            return jsonify({"error": "You have already voted in this election"}), 400

        # Get user details
        try:
            users = get_collection("users")
            user = users.find_one({"_id": ObjectId(user_id)})
            if not user:
                return jsonify({"error": "User account not found"}), 404
        except Exception as e:
            print(f"❌ Error fetching user details: {e}")
            return jsonify({"error": "Error processing your request"}), 500

        # Get candidate and election details
        try:
            candidates = get_collection("candidates")
            candidate = candidates.find_one({"_id": ObjectId(candidate_id)})
            if not candidate:
                return jsonify({"error": "Candidate not found"}), 404

            elections = get_collection("elections")
            election = elections.find_one({"_id": ObjectId(election_id)})
            if not election:
                return jsonify({"error": "Election not found"}), 404
        except Exception as e:
            print(f"❌ Error fetching election/candidate details: {e}")
            return jsonify({"error": "Error processing election data"}), 500

        # Record the vote
        try:
            ok = record_vote(user_id, candidate_id, election_id)
            if not ok:
                return jsonify({"error": "Failed to record your vote. Please try again."}), 400
        except Exception as e:
            print(f"❌ Error recording vote: {e}")
            return jsonify({"error": "Failed to process your vote"}), 500

        # Send confirmation email (non-blocking)
        try:
            from utils.email_service import send_vote_confirmation_email
            from threading import Thread
            
            # Start a new thread to send email
            email_thread = Thread(
                target=send_vote_confirmation_email,
                kwargs={
                    'to_email': user.get('email'),
                    'user_name': user.get('name', 'Voter'),
                    'candidate_name': candidate.get('candidate_name', 'the candidate'),
                    'election_name': election.get('election_name', 'the election')
                }
            )
            email_thread.daemon = True
            email_thread.start()
            print(f"ℹ️  Email notification queued for {user.get('email')}")
            
        except Exception as e:
            print(f"⚠️  Failed to queue email notification: {e}")
            # Continue even if email fails

        return jsonify({
            "message": "Vote recorded successfully!",
            "candidate": candidate.get('candidate_name'),
            "election": election.get('election_name')
        }), 201

    except Exception as e:
        print(f"❌ Unexpected error in vote endpoint: {str(e)}")
        return jsonify({"error": "An unexpected error occurred. Please try again."}), 500

