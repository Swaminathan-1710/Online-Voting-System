import os
import sys
from pymongo import MongoClient, ASCENDING, DESCENDING
from datetime import datetime
import bcrypt

def update_database_schema():
    print("Updating database schema to support multiple registrations...")
    
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        # Drop the existing unique email index if it exists
        try:
            users.drop_index("email_1")
            print("Dropped existing email index")
        except Exception as e:
            print(f"No existing email index to drop: {e}")
        
        # Create a new non-unique index on email
        users.create_index([("email", ASCENDING)], name="email_1", unique=False)
        
        # Add a new field to track registration status if it doesn't exist
        users.update_many(
            {"status": {"$exists": False}},
            {"$set": {"status": "approved"}}
        )
        
        # Add a new field to track registration time
        users.update_many(
            {"created_at": {"$exists": False}},
            {"$set": {"created_at": datetime.utcnow()}}
        )
        
        # Add a new field to track if the user is active
        users.update_many(
            {"is_active": {"$exists": False}},
            {"$set": {"is_active": True}}
        )
        
        print("Database schema updated successfully!")
        
        # Print current indexes
        print("\nCurrent indexes in 'users' collection:")
        for idx in users.list_indexes():
            print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        return True
        
    except Exception as e:
        print(f"Error updating database schema: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_registration_controller():
    print("\nUpdating registration controller...")
    
    try:
        controller_path = os.path.join('ballot_hub', 'controllers', 'user_controller.py')
        
        with open(controller_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the register function to handle multiple registrations
        new_register_function = """
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    # Validate inputs before processing
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not email:
        return jsonify({"error": "Email is required"}), 400
    if not password:
        return jsonify({"error": "Password is required"}), 400

    # Check if this is a duplicate registration attempt
    existing_user = get_collection("users").find_one({
        "email": email,
        "name": name,
        "status": "pending"
    })
    
    if existing_user:
        return jsonify({
            "message": "Your registration is already pending. Please wait for admin approval."
        }), 200

    # Register the new user with pending status
    result = register_user(name, email, password, status="pending")
    
    if result.get("success"):
        return jsonify({
            "message": "Registration submitted. Please wait for admin approval.",
            "requires_approval": True
        }), 201
    
    return jsonify({"error": result.get("message", "Registration failed")}), 400
"""
        # Replace the existing register function
        import re
        updated_content = re.sub(
            r'def register\(\).*?(?=def |\Z)',
            new_register_function,
            content,
            flags=re.DOTALL
        )
        
        # Write the updated content back to the file
        with open(controller_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("Registration controller updated successfully!")
        return True
        
    except Exception as e:
        print(f"Error updating registration controller: {e}")
        import traceback
        traceback.print_exc()
        return False

def update_admin_interface():
    print("\nUpdating admin interface to show pending registrations...")
    
    try:
        admin_routes_path = os.path.join('ballot_hub', 'routes', 'admin_routes.py')
        
        # Check if admin_routes.py exists, if not create it
        if not os.path.exists(admin_routes_path):
            print("admin_routes.py not found. Creating a basic admin interface...")
            admin_routes_content = """from flask import Blueprint, jsonify, request
from bson import ObjectId
from ..database.connection import get_collection
from flask_login import login_required, current_user

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/api/admin/pending-registrations', methods=['GET'])
@login_required
def get_pending_registrations():
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
        
    users = get_collection('users')
    pending_users = list(users.find({"status": "pending"}, {"password": 0}))
    
    # Convert ObjectId to string for JSON serialization
    for user in pending_users:
        user['_id'] = str(user['_id'])
        user['created_at'] = user.get('created_at', '').isoformat() if user.get('created_at') else ''
    
    return jsonify({"users": pending_users})

@admin_bp.route('/api/admin/approve-user/<user_id>', methods=['POST'])
@login_required
def approve_user(user_id):
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
    
    users = get_collection('users')
    result = users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"status": "approved", "is_active": True}}
    )
    
    if result.modified_count > 0:
        return jsonify({"message": "User approved successfully"})
    return jsonify({"error": "User not found or already approved"}), 404

@admin_bp.route('/api/admin/reject-user/<user_id>', methods=['POST'])
@login_required
def reject_user(user_id):
    if not current_user.is_authenticated or not current_user.is_admin:
        return jsonify({"error": "Unauthorized"}), 403
    
    users = get_collection('users')
    result = users.delete_one({"_id": ObjectId(user_id), "status": "pending"})
    
    if result.deleted_count > 0:
        return jsonify({"message": "User registration rejected and removed"})
    return jsonify({"error": "User not found or already processed"}), 404
"""
            with open(admin_routes_path, 'w', encoding='utf-8') as f:
                f.write(admin_routes_content)
            
            # Also update __init__.py to register the admin blueprint
            init_path = os.path.join('ballot_hub', '__init__.py')
            with open(init_path, 'r', encoding='utf-8') as f:
                init_content = f.read()
            
            # Add import for admin blueprint
            if 'from .routes import admin_routes' not in init_content:
                init_content = init_content.replace(
                    'from .routes import user_routes',
                    'from .routes import user_routes, admin_routes'
                )
                
                # Register the admin blueprint
                if 'app.register_blueprint(admin_routes.admin_bp, url_prefix="/admin")' not in init_content:
                    init_content = init_content.replace(
                        'app.register_blueprint(user_routes.user_bp, url_prefix="/api")',
                        'app.register_blueprint(user_routes.user_bp, url_prefix="/api")\n    app.register_blueprint(admin_routes.admin_bp, url_prefix="/api")'
                    )
                
                with open(init_path, 'w', encoding='utf-8') as f:
                    f.write(init_content)
        
        print("Admin interface updated successfully!")
        return True
        
    except Exception as e:
        print(f"Error updating admin interface: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("UPDATING REGISTRATION SYSTEM")
    print("This will modify your database and application code")
    print("="*60)
    
    # Update database schema
    if not update_database_schema():
        print("\n[ERROR] Failed to update database schema. Please check the error messages above.")
        sys.exit(1)
    
    # Update registration controller
    if not update_registration_controller():
        print("\n[WARNING] Failed to update registration controller. You may need to update it manually.")
    
    # Update admin interface
    if not update_admin_interface():
        print("\n[WARNING] Failed to update admin interface. You may need to update it manually.")
    
    print("\n" + "="*60)
    print("UPDATE COMPLETE!")
    print("Please restart your application server for the changes to take effect.")
    print("="*60)
    
    input("\nPress Enter to exit...")
