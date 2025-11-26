import os
import sys
from pymongo import MongoClient
from datetime import datetime
import bcrypt
from bson.objectid import ObjectId

def reset_auth_system():
    print("Starting authentication system reset...")
    
    # Configuration
    DB_NAME = "ballot_hub"
    BACKUP_DIR = "db_backups"
    
    # Create backup directory if it doesn't exist
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    
    # Connect to MongoDB
    try:
        client = MongoClient('mongodb://localhost:27017/')
        db = client[DB_NAME]
        print("[SUCCESS] Connected to MongoDB")
    except Exception as e:
        print(f"[ERROR] Failed to connect to MongoDB: {e}")
        return False
    
    # Backup existing data
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_db = f"{DB_NAME}_backup_{timestamp}"
        client.admin.command('copydb', fromdb=DB_NAME, todb=backup_db)
        print(f"[SUCCESS] Created backup: {backup_db}")
    except Exception as e:
        print(f"[WARNING] Could not create backup: {e}")
        if input("Continue without backup? (y/n): ").lower() != 'y':
            return False
    
    # Reset users collection
    try:
        print("\nResetting users collection...")
        users = db['users']
        users.drop()
        print("[SUCCESS] Dropped users collection")
        
        # Recreate collection with proper indexes
        users = db['users']
        users.create_index("email", unique=True, name="email_1")
        print("[SUCCESS] Recreated users collection with indexes")
        
        # Create test admin user
        admin_email = "admin@ballothub.test"
        admin_password = "Admin@123"
        hashed_password = bcrypt.hashpw(admin_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_user = {
            "name": "Admin User",
            "email": admin_email,
            "password": hashed_password,
            "status": "approved",
            "is_admin": True,
            "created_at": datetime.utcnow()
        }
        
        users.insert_one(admin_user)
        print(f"[SUCCESS] Created test admin user")
        print(f"   Email: {admin_email}")
        print(f"   Password: {admin_password}")
        
        # Create test regular user
        user_email = "user@ballothub.test"
        user_password = "User@123"
        hashed_user_pw = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        regular_user = {
            "name": "Test User",
            "email": user_email,
            "password": hashed_user_pw,
            "status": "approved",
            "is_admin": False,
            "created_at": datetime.utcnow()
        }
        
        users.insert_one(regular_user)
        print(f"\n[SUCCESS] Created test regular user")
        print(f"   Email: {user_email}")
        print(f"   Password: {user_password}")
        
        # Verify the setup
        print("\nVerifying setup...")
        print(f"Total users: {users.count_documents({})}")
        print("Current indexes:")
        for idx in users.list_indexes():
            print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        print("\n[SUCCESS] Authentication system reset completed!")
        print("\nYou can now log in with:")
        print(f"Admin: {admin_email} / {admin_password}")
        print(f"User: {user_email} / {user_password}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error during reset: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("="*60)
    print("WARNING: This will reset the authentication system!")
    print("A backup of the current database will be created.")
    print("="*60)
    
    confirm = input("\nAre you sure you want to continue? (y/n): ")
    if confirm.lower() == 'y':
        if reset_auth_system():
            print("\n[SUCCESS] Reset completed successfully!")
            print("Please restart your application server for changes to take effect.")
        else:
            print("\n[ERROR] Reset failed. Check the error messages above.")
    else:
        print("\nOperation cancelled.")
    
    input("\nPress Enter to exit...")
