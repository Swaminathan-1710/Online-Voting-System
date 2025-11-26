from pymongo import MongoClient

def fix_aadhaar_issue():
    try:
        print("Connecting to MongoDB...")
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub_db']  # Using ballot_hub_db as per error message
        users = db['users']
        
        print("\n=== Current Indexes ===")
        for idx in users.list_indexes():
            print(f"Index: {idx['name']}, Keys: {idx['key']}")
        
        # Drop aadhaar_no_1 index if it exists
        try:
            users.drop_index('aadhaar_no_1')
            print("\n✅ Dropped aadhaar_no_1 index")
        except Exception as e:
            print(f"\nℹ️ Could not drop aadhaar_no_1 index (may not exist): {str(e)}")
        
        # Remove aadhaar fields from all documents
        result = users.update_many(
            {},
            {'$unset': {
                'aadhaar_no': "",
                'aadhaar_hash': "",
                'aadhaar_last4': ""
            }}
        )
        print(f"\n✅ Removed Aadhaar fields from {result.modified_count} documents")
        
        print("\n=== Final Indexes ===")
        for idx in users.list_indexes():
            print(f"Index: {idx['name']}, Keys: {idx['key']}")
            
        print("\n✅ Aadhaar cleanup completed successfully!")
        print("Please restart your Flask application.")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease make sure MongoDB is running and try again.")

if __name__ == "__main__":
    fix_aadhaar_issue()
