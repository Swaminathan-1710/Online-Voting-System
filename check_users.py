from pymongo import MongoClient

def check_users():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("Checking users collection for issues...")
        
        # Find users with missing required fields
        users_with_issues = list(users.find({
            "$or": [
                {"status": {"$exists": False}},
                {"name": {"$exists": False}},
                {"email": {"$exists": False}}
            ]
        }))
        
        if not users_with_issues:
            print("No users with missing required fields found.")
            return True
            
        print("\nUsers with issues:")
        for user in users_with_issues:
            print(f"\nUser ID: {user.get('_id')}")
            print(f"Name: {user.get('name', 'MISSING')}")
            print(f"Email: {user.get('email', 'MISSING')}")
            print(f"Status: {user.get('status', 'MISSING')}")
            print("---")
            
        return True
        
    except Exception as e:
        print(f"Error checking users: {str(e)}")
        return False

if __name__ == "__main__":
    if check_users():
        print("\nUser check completed.")
    else:
        print("\nFailed to check users. Please see the error message above.")
