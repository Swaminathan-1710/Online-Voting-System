from pymongo import MongoClient

def fix_user_status():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("Fixing user status fields...")
        
        # First, find all users without a status field
        users_without_status = list(users.find({"status": {"$exists": False}}))
        
        if not users_without_status:
            print("No users with missing status field found.")
            return True
            
        print(f"Found {len(users_without_status)} users with missing status field")
        
        # Update all users without a status field to have status='approved'
        result = users.update_many(
            {"status": {"$exists": False}},
            {"$set": {"status": "approved"}}
        )
        
        print(f"Updated {result.modified_count} users with missing status field")
        print("User status fix completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error fixing user status: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting user status fix...")
    if fix_user_status():
        print("\nSUCCESS: User status fields have been fixed.")
    else:
        print("\nERROR: Failed to fix user status fields. Please check the error message above.")
