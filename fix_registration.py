from pymongo import MongoClient
import pymongo

def fix_registration_issue():
    print("Fixing registration issues...")
    
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    
    # 1. Get the users collection
    users = db['users']
    
    # 2. Check for the specific email (case-insensitive)
    email_to_fix = "iswami167@gmail.com"
    print(f"Checking for email: {email_to_fix}")
    
    # 3. Delete any user with this email (case-insensitive)
    result = users.delete_many({
        "email": {"$regex": f"^{email_to_fix}$", "$options": "i"}
    })
    
    print(f"Deleted {result.deleted_count} users with email {email_to_fix}")
    
    # 4. Drop and recreate the email index
    print("\nResetting email index...")
    try:
        users.drop_index("email_1")
        print("Dropped existing email index")
    except Exception as e:
        print(f"Could not drop email index (may not exist): {e}")
    
    # Create new index
    users.create_index("email", unique=True, name="email_1")
    print("Created new unique email index")
    
    # 5. Verify
    print("\nVerifying database state:")
    print(f"Total users: {users.count_documents({})}")
    print("Current indexes:")
    for idx in users.list_indexes():
        print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
    
    # 6. Check if we can insert a test user
    test_email = "test_user@example.com"
    try:
        test_user = {
            "name": "Test User",
            "email": test_email,
            "password": "hashed_password_here",
            "status": "test"
        }
        users.insert_one(test_user)
        print(f"\nSuccessfully inserted test user with email: {test_email}")
        
        # Clean up test user
        users.delete_one({"email": test_email})
        print("Cleaned up test user")
    except Exception as e:
        print(f"\nError inserting test user: {e}")
        print("This suggests there are still issues with the database.")
    
    print("\n[COMPLETE] Database fix completed. Please try registering again.")
    print("If you still have issues, please try restarting your application server.")

if __name__ == "__main__":
    fix_registration_issue()
