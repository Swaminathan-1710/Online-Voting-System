"""
Fix email uniqueness constraint to be case-insensitive and work with pending users.
"""
from ballot_hub.database.connection import get_db

def fix_email_uniqueness():
    try:
        db = get_db()
        users = db.users
        
        # Drop existing email index if it exists
        existing_indexes = users.index_information()
        if 'email_1' in existing_indexes:
            users.drop_index('email_1')
            print("✓ Dropped existing email index")
        
        # Create a case-insensitive index on email field
        users.create_index(
            [("email", "text")],
            unique=True,
            collation={
                'locale': 'en',
                'strength': 2  # Case-insensitive comparison
            }
        )
        
        print("✓ Created new case-insensitive email index")
        return True
        
    except Exception as e:
        print(f"✗ Error fixing email uniqueness: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Fixing email uniqueness constraint...")
    if fix_email_uniqueness():
        print("✓ Email uniqueness constraint fixed successfully!")
    else:
        print("✗ Failed to fix email uniqueness constraint")
