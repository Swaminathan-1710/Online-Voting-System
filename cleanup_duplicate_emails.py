"""
Script to find and clean up duplicate emails in the users collection
"""
from pymongo import MongoClient
from bson.objectid import ObjectId
from collections import defaultdict

def find_and_clean_duplicates():
    try:
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['ballot_hub']
        users = db['users']
        
        print("=" * 60)
        print("Finding and Cleaning Duplicate Emails")
        print("=" * 60)
        
        # Find all users and group by email (case-insensitive)
        email_groups = defaultdict(list)
        all_users = list(users.find({}, {"email": 1, "name": 1, "created_at": 1, "status": 1}))
        
        for user in all_users:
            if 'email' in user:
                email_groups[user['email'].lower().strip()].append(user)
        
        # Find duplicates
        duplicates = {email: user_list for email, user_list in email_groups.items() if len(user_list) > 1}
        
        if not duplicates:
            print("\nNo duplicate emails found!")
            return True
            
        print(f"\nFound {len(duplicates)} email(s) with duplicates:")
        
        # Process each duplicate email
        for email, user_list in duplicates.items():
            print(f"\nEmail: {email}")
            print("-" * 40)
            
            # Sort by created_at (oldest first) and status (approved first)
            user_list.sort(key=lambda x: (
                x.get('status') != 'approved',
                x.get('created_at', '')
            ))
            
            # Keep the first user (approved and oldest)
            keep_user = user_list[0]
            print(f"KEEPING: {keep_user.get('name')} (ID: {keep_user['_id']}, Status: {keep_user.get('status', 'unknown')})")
            
            # Mark others for deletion
            for dup_user in user_list[1:]:
                print(f"  - Will delete: {dup_user.get('name')} (ID: {dup_user['_id']}, Status: {dup_user.get('status', 'unknown')})")
            
            # Ask for confirmation
            response = input("\nDelete these duplicates? (y/n): ").strip().lower()
            if response == 'y':
                for dup_user in user_list[1:]:
                    users.delete_one({"_id": dup_user["_id"]})
                    print(f"  - Deleted user: {dup_user.get('name')}")
            else:
                print("Skipped deletion.")
            
            print()
        
        print("\nDuplicate email cleanup completed!")
        return True
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        return False

if __name__ == "__main__":
    find_and_clean_duplicates()
