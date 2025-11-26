from pymongo import MongoClient
from bson.objectid import ObjectId

def deep_inspect_database():
    print("🔍 Performing deep inspection of the database...")
    
    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    
    # 1. Check all collections
    print("\n📂 Collections in database:")
    collections = db.list_collection_names()
    for col in collections:
        count = db[col].count_documents({})
        print(f"- {col}: {count} documents")
    
    # 2. Check users collection in detail
    if 'users' in collections:
        users = db['users']
        
        # 2.1 Check indexes
        print("\n🔑 Indexes in 'users' collection:")
        for idx in users.list_indexes():
            print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        # 2.2 Check for any documents
        all_users = list(users.find({}))
        print(f"\n👥 Total users: {len(all_users)}")
        
        if all_users:
            print("\n📝 User details:")
            for user in all_users:
                print(f"\nID: {user.get('_id')}")
                print(f"Name: {user.get('name')}")
                print(f"Email: {user.get('email')}")
                print(f"Status: {user.get('status', 'N/A')}")
                print("-" * 50)
        
        # 2.3 Check for the specific email (case-insensitive)
        email_to_check = "iswami167@gmail.com"
        print(f"\n🔍 Searching for email (case-insensitive): {email_to_check}")
        
        # Try different search methods
        search_methods = [
            ("Direct match", {"email": email_to_check}),
            ("Case-insensitive regex", {"email": {"$regex": f"^{email_to_check}$", "$options": "i"}}),
            ("Partial match", {"email": {"$regex": email_to_check, "$options": "i"}})
        ]
        
        for method_name, query in search_methods:
            print(f"\n🔎 {method_name}:")
            try:
                matches = list(users.find(query, {"_id": 1, "email": 1, "name": 1, "status": 1}))
                if matches:
                    for match in matches:
                        print(f"- Found: {match}")
                else:
                    print("  No matches found")
            except Exception as e:
                print(f"  Error: {str(e)}")
    
    # 3. Check system collections that might contain user data
    system_collections = ["system.users", "system.profile"]
    print("\n🔍 Checking system collections:")
    for sys_col in system_collections:
        try:
            if sys_col in db.list_collection_names():
                count = db[sys_col].count_documents({})
                print(f"- {sys_col}: {count} documents")
                if count > 0 and sys_col == "system.users":
                    print("  Warning: System users collection has entries")
        except Exception as e:
            print(f"  Could not check {sys_col}: {str(e)}")
    
    print("\n[COMPLETE] Deep inspection complete!")

if __name__ == "__main__":
    print("Starting deep database inspection...")
    deep_inspect_database()
    print("\n[NOTE] If no issues were found but you're still having problems:")
    print("1. Try restarting your MongoDB service")
    print("2. Check for any application logs")
    print("3. Try registering with a different email address")
