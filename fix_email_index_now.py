from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure

def fix_registration_indexes():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("=" * 60)
        print("Fixing Registration Indexes")
        print("=" * 60)
        
        # 1. First, drop all existing indexes except _id_
        print("\nDropping existing indexes...")
        for idx in users.list_indexes():
            if idx['name'] != '_id_':
                users.drop_index(idx['name'])
                print(f"  - Dropped index: {idx['name']}")
        
        # 2. Create a unique index on email (case-insensitive)
        print("\nCreating email index...")
        users.create_index(
            [("email", ASCENDING)],
            name="email_unique",
            unique=True,
            collation={'locale': 'en', 'strength': 2}  # Case-insensitive comparison
        )
        print("  - Created unique email index (case-insensitive)")
        
        # 3. Create a compound index for faster lookups
        users.create_index(
            [("email", ASCENDING), ("name", ASCENDING)],
            name="email_name"
        )
        print("  - Created email+name index")
        
        # 4. Create index on status for faster filtering
        users.create_index(
            [("status", ASCENDING)],
            name="status"
        )
        print("  - Created status index")
        
        # 5. Verify the indexes
        print("\nCurrent indexes:")
        for idx in users.list_indexes():
            print(f"  - {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        print("\nSUCCESS: Registration indexes have been fixed!")
        print("You can now register multiple unique users.")
        print("Each email can only be used once (case-insensitive).")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        if hasattr(e, 'details'):
            print(f"Details: {e.details}")
        return False

if __name__ == "__main__":
    print("Fixing database indexes for user registration...")
    print("Make sure your MongoDB server is running.\n")
    
    if fix_registration_indexes():
        print("\n✅ Indexes fixed successfully!")
        print("Please restart your Flask application for the changes to take effect.")
    else:
        print("\n❌ Failed to fix indexes. Please check the error message above.")
