from pymongo import MongoClient
import pymongo
from bson.objectid import ObjectId

def check_specific_user(email):
    """Check if a specific user exists by email."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    users = db['users']
    
    # Check with case-insensitive search
    user = users.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
    return user

def delete_user_by_email(email):
    """Delete a user by email (case-insensitive)."""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    users = db['users']
    
    result = users.delete_many({"email": {"$regex": f"^{email}$", "$options": "i"}})
    return result.deleted_count

def check_and_fix_indexes():
    # Connect to MongoDB (update the connection string if needed)
    client = MongoClient('mongodb://localhost:27017/')
    
    # Get the database (update 'ballot_hub' if your database name is different)
    db = client['ballot_hub']
    users = db['users']
    
    # First, drop and recreate the email index
    print("Dropping existing email index...")
    users.drop_index("email_1")
    print("Creating new email index...")
    users.create_index("email", unique=True, name="email_1")
    
    print("Current indexes in 'users' collection:")
    for idx in users.list_indexes():
        print(f"- {idx['name']}: {idx['key']}")
    
    # Check if email index exists and is unique
    email_index = None
    for idx in users.list_indexes():
        if 'email' in idx['key']:
            email_index = idx
            break
    
    if email_index:
        print("\nCurrent email index:")
        print(f"- Name: {email_index['name']}")
        print(f"- Key: {email_index['key']}")
        print(f"- Unique: {email_index.get('unique', False)}")
        
        # If email index is not unique, drop and recreate it
        if not email_index.get('unique', False):
            print("\nEmail index is not unique. Fixing...")
            users.drop_index(email_index['name'])
            users.create_index("email", unique=True)
            print("[SUCCESS] Recreated email index with unique constraint")
        else:
            print("\n[INFO] Email index is already unique")
    else:
        print("\nNo email index found. Creating one...")
        users.create_index("email", unique=True)
        print("[SUCCESS] Created email index with unique constraint")
    
    # Print final index status
    print("\nFinal indexes in 'users' collection:")
    for idx in users.list_indexes():
        print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
    
    # Count users
    total_users = users.count_documents({})
    print(f"\nTotal users in database: {total_users}")
    
    # List all users (email and name only)
    if total_users > 0:
        print("\nAll users in database:")
        for user in users.find({}, {'email': 1, 'name': 1, '_id': 1, 'status': 1}):
            print(f"- ID: {user.get('_id')}")
            print(f"  Name: {user.get('name')}")
            print(f"  Email: {user.get('email')}")
            print(f"  Status: {user.get('status', 'N/A')}")
            print("  " + "-"*30)

if __name__ == "__main__":
    print("Checking and fixing database issues...\n")
    
    # Email to check and clean up
    email_to_check = "iswami167@gmail.com"
    
    print(f"Checking for user with email: {email_to_check}")
    user = check_specific_user(email_to_check)
    
    if user:
        print(f"\nFound existing user with email {email_to_check}:")
        print(f"- ID: {user.get('_id')}")
        print(f"- Name: {user.get('name')}")
        print(f"- Status: {user.get('status', 'N/A')}")
        
        # Delete the user
        deleted_count = delete_user_by_email(email_to_check)
        print(f"\nDeleted {deleted_count} user(s) with email {email_to_check}")
    else:
        print(f"\nNo user found with email: {email_to_check}")
    
    # Fix indexes
    print("\nFixing database indexes...")
    check_and_fix_indexes()
    
    print("\n[COMPLETE] Database cleanup complete. Please try registering again.")
    print("If you still encounter issues, please try these steps:")
    print("1. Clear your browser cache and cookies")
    print("2. Try registering with a different email address")
    print("3. Restart the application server if possible")
