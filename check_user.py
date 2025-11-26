from pymongo import MongoClient

def check_user(email):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    users = db['users']
    
    # Check if user exists (case-insensitive)
    user = users.find_one({"email": {"$regex": f'^{email}$', "$options": 'i'}})
    
    if user:
        print(f"User found with email '{email}':")
        print(f"Name: {user.get('name')}")
        print(f"ID: {user['_id']}")
        print(f"Status: {user.get('status', 'active')}")
        return True
    else:
        print(f"No user found with email '{email}'")
        return False

if __name__ == "__main__":
    check_user("surya@gmail.com")
