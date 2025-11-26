from pymongo import MongoClient

def list_all_users():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("Listing all users in the database:")
        print("-" * 50)
        
        all_users = list(users.find({}))
        
        if not all_users:
            print("No users found in the database.")
            return True
            
        for i, user in enumerate(all_users, 1):
            print(f"\nUser #{i}:")
            print("-" * 30)
            for key, value in user.items():
                if key == '_id':
                    print(f"{key}: {str(value)}")
                else:
                    print(f"{key}: {value}")
            
        return True
        
    except Exception as e:
        print(f"Error listing users: {str(e)}")
        return False

if __name__ == "__main__":
    if list_all_users():
        print("\nUser listing completed.")
    else:
        print("\nFailed to list users. Please see the error message above.")
