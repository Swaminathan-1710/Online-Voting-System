from pymongo import MongoClient
from datetime import datetime

def update_users_collection():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("Updating users collection...")
        
        # Add default status to users without one
        result = users.update_many(
            {"status": {"$exists": False}},
            {"$set": {"status": "approved"}}  # Set existing users as approved
        )
        print(f"Updated {result.modified_count} users with default 'approved' status")
        
        # Add created_at to users without it
        result = users.update_many(
            {"created_at": {"$exists": False}},
            {"$set": {"created_at": datetime.utcnow()}}
        )
        print(f"Updated {result.modified_count} users with creation timestamp")
        
        print("Users collection update completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error updating users collection: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting users collection update...")
    if update_users_collection():
        print("\nSUCCESS: Users collection has been updated successfully.")
    else:
        print("\nERROR: Failed to update users collection. Please check the error message above.")
