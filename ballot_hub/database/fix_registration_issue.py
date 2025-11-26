"""
Script to fix registration issues by cleaning up problematic data
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_collection


def fix_registration_issues():
    """Fix common registration issues"""
    users = get_collection("users")
    
    print("=" * 60)
    print("Fixing Registration Issues")
    print("=" * 60)
    
    # Check for users with null phone_hash
    null_phone_users = list(users.find({
        "$or": [
            {"phone_hash": None},
            {"phone_hash": {"$exists": False}}
        ]
    }))
    
    print(f"\nFound {len(null_phone_users)} users with null/missing phone_hash")
    
    if null_phone_users:
        print("\nThese users may cause registration issues:")
        for user in null_phone_users:
            print(f"  - {user.get('name', 'N/A')} ({user.get('email', 'N/A')}) - ID: {user.get('_id')}")
        
        response = input("\nDelete these users? (yes/no): ")
        if response.lower() == 'yes':
            for user in null_phone_users:
                users.delete_one({"_id": user["_id"]})
            print(f"✓ Deleted {len(null_phone_users)} users with null phone_hash")
        else:
            print("Skipped deletion")
    
    # Check for duplicate emails
    all_users = list(users.find({}, {"email": 1, "name": 1}))
    email_counts = {}
    for user in all_users:
        email = user.get("email", "").lower().strip()
        if email:
            if email not in email_counts:
                email_counts[email] = []
            email_counts[email].append(user)
    
    duplicates = {email: users for email, users in email_counts.items() if len(users) > 1}
    
    if duplicates:
        print(f"\nFound {len(duplicates)} duplicate emails:")
        for email, user_list in duplicates.items():
            print(f"\n  Email: {email}")
            for i, user in enumerate(user_list, 1):
                print(f"    {i}. {user.get('name', 'N/A')} - ID: {user.get('_id')}")
    else:
        print("\n✓ No duplicate emails found")
    
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)


if __name__ == "__main__":
    fix_registration_issues()

