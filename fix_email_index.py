"""
Script to fix email index issues
Run this if you're getting false positive duplicate errors
"""
import sys
import os
from pymongo import MongoClient, ASCENDING
from pymongo.errors import OperationFailure

def fix_email_index():
    """Fix email index by making it non-unique and adding a partial unique index"""
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("=" * 60)
        print("Fixing Email Indexes")
        print("=" * 60)
        
        # Get current indexes
        print("\nCurrent indexes:")
        for idx in users.list_indexes():
            print(f" - {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        # Drop all indexes except _id_
        for idx in users.list_indexes():
            if idx['name'] != '_id_':
                users.drop_index(idx['name'])
                print(f"Dropped index: {idx['name']}")
        
        # Create a non-unique index on email
        users.create_index([("email", ASCENDING)], name="email_1")
        print("Created non-unique email index")
        
        # Create a compound unique index on email+name for approved users
        users.create_index(
            [("email", ASCENDING), ("name", ASCENDING)],
            name="email_name",
            partialFilterExpression={"status": "approved"},
            unique=True
        )
        print("Created partial unique index for approved users")
        
        # Verify
        print("\nUpdated indexes:")
        for idx in users.list_indexes():
            print(f" - {idx['name']}: {idx['key']} (unique: {idx.get('unique', False)})")
        
        print("\nSUCCESS: Email indexes have been fixed.")
        print("You can now register multiple users with the same email but different names.")
        print("Only one approved user per email+name combination will be allowed.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    fix_email_index()
