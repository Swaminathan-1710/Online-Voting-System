"""
Quick fix script to resolve phone_hash index creation error.
This script removes users without phone_hash so the unique index can be created.
"""
from database.connection import get_collection


def fix_phone_hash_index():
    """Remove users without phone_hash and create the index"""
    try:
        users = get_collection("users")
        
        print("=" * 60)
        print("Fixing phone_hash Index Issue")
        print("=" * 60)
        
        # Check for users without phone_hash
        users_without_phone = list(users.find({
            "$or": [
                {"phone_hash": {"$exists": False}},
                {"phone_hash": None}
            ]
        }))
        
        count = len(users_without_phone)
        
        if count == 0:
            print("✓ No users without phone_hash found. Index should work now.")
            # Try to create index
            try:
                existing_indexes = [idx['name'] for idx in users.list_indexes()]
                if 'phone_hash_1' not in existing_indexes:
                    users.create_index("phone_hash", unique=True)
                    print("✓ Created phone_hash index successfully!")
                else:
                    print("✓ phone_hash index already exists")
            except Exception as e:
                print(f"⚠️  Could not create index: {e}")
            return True
        
        print(f"\nFound {count} users without phone_hash:")
        for user in users_without_phone[:5]:  # Show first 5
            print(f"  - {user.get('name', 'Unknown')} ({user.get('email', 'No email')})")
        if count > 5:
            print(f"  ... and {count - 5} more")
        
        print("\n⚠️  These users need to be removed to create the unique index.")
        print("   They can re-register with phone numbers later.")
        
        response = input("\nDelete these users? (yes/no): ")
        
        if response.lower() == 'yes':
            result = users.delete_many({
                "$or": [
                    {"phone_hash": {"$exists": False}},
                    {"phone_hash": None}
                ]
            })
            print(f"\n✓ Deleted {result.deleted_count} users without phone_hash")
            
            # Now try to create the index
            try:
                existing_indexes = [idx['name'] for idx in users.list_indexes()]
                if 'phone_hash_1' not in existing_indexes:
                    users.create_index("phone_hash", unique=True)
                    print("✓ Created phone_hash index successfully!")
                else:
                    print("✓ phone_hash index already exists")
                print("\n✓ Fix completed successfully!")
                return True
            except Exception as e:
                print(f"\n✗ Could not create index: {e}")
                print("   There may be other issues. Check MongoDB logs.")
                return False
        else:
            print("\n⚠️  Skipped deletion. Index cannot be created with null values.")
            print("   You can run this script again later to fix it.")
            return False
        
    except Exception as e:
        print(f"\n✗ Fix failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    fix_phone_hash_index()

