"""
Script to ensure email uniqueness across all users
"""
from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure

def ensure_email_uniqueness():
    """Ensure email is unique across all users"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("=" * 60)
        print("Ensuring Email Uniqueness")
        print("=" * 60)
        
        # Get current indexes
        print("\nCurrent indexes:")
        for idx in users.list_indexes():
            print(f" - {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        # Drop existing email-related indexes
        for idx in users.list_indexes():
            if idx['name'] != '_id_':
                users.drop_index(idx['name'])
                print(f"Dropped index: {idx['name']}")
        
        # Create a unique index on email
        users.create_index([("email", ASCENDING)], name="email", unique=True)
        print("\nCreated unique email index")
        
        # Verify
        print("\nUpdated indexes:")
        for idx in users.list_indexes():
            print(f" - {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        print("\nSUCCESS: Email uniqueness has been enforced.")
        print("Each email can only be used by one user.")
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    ensure_email_uniqueness()
