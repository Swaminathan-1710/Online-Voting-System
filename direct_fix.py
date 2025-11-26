from pymongo import MongoClient
from bson.objectid import ObjectId
import pymongo

def check_database():
    print("Connecting to MongoDB...")
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    
    # Get all collections
    collections = db.list_collection_names()
    print("\nCollections in database:", collections)
    
    # Check users collection
    if 'users' in collections:
        users = db['users']
        
        # Drop and recreate users collection
        print("\nDropping and recreating 'users' collection...")
        db.drop_collection('users')
        users = db.create_collection('users')
        
        # Create indexes
        print("Creating indexes...")
        users.create_index("email", unique=True, name="email_1")
        
        # Verify
        print("\nCurrent indexes in 'users' collection:")
        for idx in users.list_indexes():
            print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        print(f"\nTotal users after reset: {users.count_documents({})}")
    
    print("\n[COMPLETE] Database has been reset. Please try registering again.")

if __name__ == "__main__":
    print("Starting database cleanup...")
    check_database()
    print("\nPlease try registering again. The database has been reset.")
    print("If you still have issues, please restart your application server.")
