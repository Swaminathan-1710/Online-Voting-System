"""Quick script to check if a user exists"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_collection

email = "11229a039@kanchiuniv.ac.in"
users = get_collection("users")

# Check with exact match
user = users.find_one({"email": email})
print(f"Exact match: {user is not None}")

# Check with case-insensitive
user2 = users.find_one({"email": {"$regex": f"^{email}$", "$options": "i"}})
print(f"Case-insensitive match: {user2 is not None}")

# List all users
all_users = list(users.find({}, {"email": 1, "name": 1}))
print(f"\nTotal users: {len(all_users)}")
for u in all_users:
    print(f"  - {u.get('email')} ({u.get('name')})")

