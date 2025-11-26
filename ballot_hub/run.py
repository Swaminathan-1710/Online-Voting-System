"""
Simple run script for BallotHub
Just run: python run.py
"""
import os
import sys

# Set default environment variables if not already set
if not os.getenv("MONGO_URI"):
    os.environ["MONGO_URI"] = "mongodb://localhost:27017"
if not os.getenv("MONGO_DB_NAME"):
    os.environ["MONGO_DB_NAME"] = "ballot_hub_db"
if not os.getenv("JWT_SECRET_KEY"):
    # Generate a simple default secret (not for production!)
    import secrets
    os.environ["JWT_SECRET_KEY"] = secrets.token_urlsafe(48)

if __name__ == "__main__":
    from app import create_app
    
    print("=" * 60)
    print("BallotHub - Secure Online Voting System")
    print("=" * 60)
    print(f"MongoDB URI: {os.getenv('MONGO_URI')}")
    print(f"Database: {os.getenv('MONGO_DB_NAME')}")
    print("=" * 60)
    
    # Initialize database
    try:
        from database.init_db import init_database
        print("\n[1/2] Initializing database...")
        init_database()
        print("[2/2] Database ready!\n")
    except Exception as e:
        print(f"\n⚠ Warning: Database initialization failed: {e}")
        print("Make sure MongoDB is running on mongodb://localhost:27017")
        print("You can start MongoDB with: mongod")
        print("=" * 60 + "\n")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Create and run app
    app = create_app()
    print("=" * 60)
    print("Server starting on http://127.0.0.1:5000")
    print("=" * 60)
    print("\nAvailable pages:")
    print("  • User Register: http://127.0.0.1:5000/register")
    print("  • User Login:    http://127.0.0.1:5000/login")
    print("  • Vote:          http://127.0.0.1:5000/vote")
    print("  • Admin Login:   http://127.0.0.1:5000/admin")
    print("  • Admin Dashboard: http://127.0.0.1:5000/admin/dashboard")
    print("\nDefault Admin Credentials:")
    print("  Username: admin")
    print("  Password: AdminPass123")
    print("\nPress Ctrl+C to stop the server\n")
    print("=" * 60 + "\n")
    
    app.run(host="0.0.0.0", port=5000, debug=True)

