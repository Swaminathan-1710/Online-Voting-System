from pymongo import MongoClient

def fix_missing_status():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("Checking for users with missing status...")
        
        # Find users without a status field or with null status
        users_to_update = users.find({
            "$or": [
                {"status": {"$exists": False}},
                {"status": None}
            ]
        })
        
        count = 0
        for user in users_to_update:
            # Set default status to 'approved' for existing users
            users.update_one(
                {"_id": user["_id"]},
                {"$set": {"status": "approved"}}
            )
            count += 1
        
        if count > 0:
            print(f"Updated {count} users with missing or null status field to 'approved'")
        else:
            print("No users with missing or null status field found")
            
        return True
        
    except Exception as e:
        print(f"Error fixing user status: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting user status fix...")
    if fix_missing_status():
        print("\nSUCCESS: User status fields have been fixed.")
    else:
        print("\nERROR: Failed to fix user status fields. Please check the error message above.")
