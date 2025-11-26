"""
Script to fix email index issues
Run this if you're getting false positive duplicate errors
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_collection


def fix_email_index():
    """Fix email index by dropping and recreating it"""
    users = get_collection("users")
    
    print("=" * 60)
    print("Fixing Email Index")
    print("=" * 60)
    
    # Get existing indexes
    existing_indexes = [idx['name'] for idx in users.list_indexes()]
    
    # Drop email index if it exists
    if 'email_1' in existing_indexes:
        try:
            users.drop_index('email_1')
            print("✓ Dropped existing email index")
        except Exception as e:
            print(f"⚠️  Could not drop email index: {e}")
    
    # Check for duplicate emails
    all_users = list(users.find({}, {"email": 1, "name": 1}))
    email_counts = {}
    for user in all_users:
        email = user.get("email", "").lower().strip()
        if email:
            if email not in email_counts:
                email_counts[email] = []
            email_counts[email].append(user)
    
    duplicates = {email: user_list for email, user_list in email_counts.items() if len(user_list) > 1}
    
    if duplicates:
        print(f"\n⚠️  Found {len(duplicates)} duplicate emails:")
        for email, user_list in duplicates.items():
            print(f"\n  Email: {email}")
            for i, user in enumerate(user_list, 1):
                print(f"    {i}. {user.get('name', 'N/A')} - ID: {user.get('_id')}")
        
        response = input("\nDelete duplicate users? (yes/no): ")
        if response.lower() == 'yes':
            for email, user_list in duplicates.items():
                # Keep the first one, delete the rest
                for user in user_list[1:]:
                    users.delete_one({"_id": user["_id"]})
                    print(f"  ✓ Deleted duplicate: {user.get('name', 'N/A')}")
        else:
            print("Skipped deletion. Cannot create unique index with duplicates.")
            return False
    
    # Recreate email index
    try:
        users.create_index("email", unique=True)
        print("\n✓ Created email index successfully")
        return True
    except Exception as e:
        print(f"\n✗ Failed to create email index: {e}")
        return False


if __name__ == "__main__":
    fix_email_index()

