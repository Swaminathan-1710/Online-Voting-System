"""
Auto-initialize MongoDB database with collections, indexes, and seed data.
Run this once or let app.py call it on startup.
"""
import bcrypt
from datetime import datetime, timedelta
from database.connection import get_db, get_collection
from config import PASSWORD_HASH_ROUNDS


def init_database():
    """Initialize MongoDB database with all required collections, indexes, and seed data."""
    try:
        # Test connection first
        from database.connection import get_client
        client = get_client()
        client.server_info()  # This will raise if connection fails
        db = get_db()
        
        # Create collections (MongoDB creates them automatically on first insert, but we'll ensure they exist)
        collections = ["users", "admins", "elections", "candidates", "votes", "otps"]
        for coll_name in collections:
            if coll_name not in db.list_collection_names():
                db.create_collection(coll_name)
        
        # Create indexes
        users = get_collection("users")
        
        # Get existing indexes
        existing_indexes = [idx['name'] for idx in users.list_indexes()]
        
        # Create email index (if not exists)
        if 'email_1' not in existing_indexes:
            users.create_index("email", unique=True)
            print("✓ Created email index")
        else:
            print("✓ Email index already exists")
        
        # Remove phone_hash index if it exists (no longer needed)
        if 'phone_hash_1' in existing_indexes:
            try:
                users.drop_index('phone_hash_1')
                print("✓ Removed phone_hash index (no longer needed)")
            except Exception as e:
                print(f"⚠️  Could not remove phone_hash index: {e}")
        
        admins = get_collection("admins")
        admins.create_index("username", unique=True)
        
        elections = get_collection("elections")
        elections.create_index([("status", 1), ("start_date", 1), ("end_date", 1)])
        
        candidates = get_collection("candidates")
        candidates.create_index("election_id")
        
        votes = get_collection("votes")
        votes.create_index([("user_id", 1), ("election_id", 1)], unique=True)
        votes.create_index([("candidate_id", 1), ("election_id", 1)])
        
        # Seed admin user if not exists
        admin_exists = admins.find_one({"username": "admin"})
        if not admin_exists:
            admin_password = bcrypt.hashpw(
                b"AdminPass123",
                bcrypt.gensalt(rounds=PASSWORD_HASH_ROUNDS)
            ).decode("utf-8")
            admins.insert_one({
                "username": "admin",
                "password": admin_password
            })
            print("✓ Admin user created: username='admin', password='AdminPass123'")
        else:
            print("✓ Admin user already exists")
        
        # Note: No sample elections are created - admin must create elections manually
        
        print("✓ Database initialization completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Initializing MongoDB database...")
    init_database()

