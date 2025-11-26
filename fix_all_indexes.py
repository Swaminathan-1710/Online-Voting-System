from pymongo import MongoClient, ASCENDING

def fix_indexes():
    try:
        print("Connecting to MongoDB...")
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("Removing old indexes...")
        # Drop all indexes except _id_
        for idx in users.list_indexes():
            if idx['name'] != '_id_':
                users.drop_index(idx['name'])
                print(f"Dropped index: {idx['name']}")
        
        print("\nCreating new indexes...")
        # Create case-insensitive unique email index
        users.create_index(
            [("email", ASCENDING)],
            name="email_unique",
            unique=True,
            collation={'locale': 'en', 'strength': 2}
        )
        print("- Created unique email index (case-insensitive)")
        
        # Create compound index for faster lookups
        users.create_index(
            [("email", ASCENDING), ("name", ASCENDING)],
            name="email_name"
        )
        print("- Created email+name index")
        
        # Create status index for faster filtering
        users.create_index(
            [("status", ASCENDING)],
            name="status"
        )
        print("- Created status index")
        
        # Verify
        print("\nCurrent indexes:")
        for idx in users.list_indexes():
            print(f"- {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        print("\n✅ Indexes fixed successfully!")
        print("You can now register multiple unique users.")
        print("Each email can only be used once (case-insensitive).")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        if hasattr(e, 'details'):
            print(f"Details: {e.details}")

if __name__ == "__main__":
    print("Fixing database indexes...")
    fix_indexes()
    print("\nPlease restart your Flask application for the changes to take effect.")
