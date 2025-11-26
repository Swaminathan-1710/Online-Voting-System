"""
Script to check for duplicate email or phone numbers in the database
Run this to debug registration issues
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_collection
from utils.phone_validator import normalize_phone, hash_phone


def check_duplicates():
    """Check for duplicate emails or phone numbers"""
    users = get_collection("users")
    
    print("=" * 60)
    print("Checking for Duplicate Users")
    print("=" * 60)
    
    # Get all users
    all_users = list(users.find({}, {"name": 1, "email": 1, "phone_hash": 1, "phone_last4": 1, "phone_normalized": 1, "status": 1}))
    
    print(f"\nTotal users in database: {len(all_users)}")
    
    # Check for duplicate emails
    email_map = {}
    duplicate_emails = []
    
    for user in all_users:
        email = user.get("email", "").lower().strip()
        if email:
            if email in email_map:
                duplicate_emails.append({
                    "email": email,
                    "user1": email_map[email],
                    "user2": user
                })
            else:
                email_map[email] = user
    
    # Check for duplicate phone hashes
    phone_map = {}
    duplicate_phones = []
    
    for user in all_users:
        phone_hash = user.get("phone_hash")
        if phone_hash:
            if phone_hash in phone_map:
                duplicate_phones.append({
                    "phone_hash": phone_hash,
                    "phone_last4": user.get("phone_last4", "N/A"),
                    "user1": phone_map[phone_hash],
                    "user2": user
                })
            else:
                phone_map[phone_hash] = user
    
    # Report results
    print("\n" + "=" * 60)
    print("DUPLICATE EMAILS")
    print("=" * 60)
    if duplicate_emails:
        for dup in duplicate_emails:
            print(f"\nEmail: {dup['email']}")
            print(f"  User 1: {dup['user1'].get('name', 'N/A')} (ID: {dup['user1'].get('_id')}, Status: {dup['user1'].get('status', 'N/A')})")
            print(f"  User 2: {dup['user2'].get('name', 'N/A')} (ID: {dup['user2'].get('_id')}, Status: {dup['user2'].get('status', 'N/A')})")
    else:
        print("✓ No duplicate emails found")
    
    print("\n" + "=" * 60)
    print("DUPLICATE PHONE NUMBERS")
    print("=" * 60)
    if duplicate_phones:
        for dup in duplicate_phones:
            print(f"\nPhone ending in: {dup['phone_last4']}")
            print(f"  User 1: {dup['user1'].get('name', 'N/A')} - Email: {dup['user1'].get('email', 'N/A')} (ID: {dup['user1'].get('_id')}, Status: {dup['user1'].get('status', 'N/A')})")
            print(f"  User 2: {dup['user2'].get('name', 'N/A')} - Email: {dup['user2'].get('email', 'N/A')} (ID: {dup['user2'].get('_id')}, Status: {dup['user2'].get('status', 'N/A')})")
    else:
        print("✓ No duplicate phone numbers found")
    
    # Check for users with missing phone_hash
    users_without_phone = [u for u in all_users if not u.get("phone_hash")]
    if users_without_phone:
        print("\n" + "=" * 60)
        print(f"USERS WITHOUT PHONE_HASH ({len(users_without_phone)})")
        print("=" * 60)
        for user in users_without_phone:
            print(f"  - {user.get('name', 'N/A')} - Email: {user.get('email', 'N/A')} (ID: {user.get('_id')})")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total users: {len(all_users)}")
    print(f"Duplicate emails: {len(duplicate_emails)}")
    print(f"Duplicate phones: {len(duplicate_phones)}")
    print(f"Users without phone_hash: {len(users_without_phone)}")
    
    if duplicate_emails or duplicate_phones:
        print("\n⚠️  WARNING: Duplicates found! This may cause registration issues.")
        print("   Consider cleaning up duplicate entries.")
    else:
        print("\n✓ No duplicates found. Database looks clean.")


def check_specific_user(email=None, phone=None):
    """Check if a specific email or phone exists"""
    users = get_collection("users")
    
    if email:
        email = email.lower().strip()
        user = users.find_one({"email": email})
        if user:
            print(f"\n✓ Email '{email}' EXISTS in database:")
            print(f"  Name: {user.get('name', 'N/A')}")
            print(f"  Status: {user.get('status', 'N/A')}")
            print(f"  Phone last 4: {user.get('phone_last4', 'N/A')}")
            print(f"  User ID: {user.get('_id')}")
        else:
            print(f"\n✗ Email '{email}' NOT FOUND in database")
    
    if phone:
        normalized = normalize_phone(phone)
        hashed = hash_phone(normalized)
        user = users.find_one({"phone_hash": hashed})
        if user:
            print(f"\n✓ Phone '{phone}' (normalized: {normalized}) EXISTS in database:")
            print(f"  Name: {user.get('name', 'N/A')}")
            print(f"  Email: {user.get('email', 'N/A')}")
            print(f"  Status: {user.get('status', 'N/A')}")
            print(f"  Phone last 4: {user.get('phone_last4', 'N/A')}")
            print(f"  User ID: {user.get('_id')}")
        else:
            print(f"\n✗ Phone '{phone}' (normalized: {normalized}) NOT FOUND in database")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Check for duplicate users in database")
    parser.add_argument("--email", help="Check specific email")
    parser.add_argument("--phone", help="Check specific phone number")
    
    args = parser.parse_args()
    
    if args.email or args.phone:
        check_specific_user(email=args.email, phone=args.phone)
    else:
        check_duplicates()

