from pymongo import MongoClient

def check_all_emails():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['ballot_hub']
    users = db['users']
    
    # Get all users and their emails
    all_users = list(users.find({}, {"email": 1, "name": 1, "_id": 1, "status": 1}))
    
    # Group by lowercase email
    email_map = {}
    duplicates = {}
    
    for user in all_users:
        if 'email' not in user:
            print(f"User {user.get('_id')} has no email field!")
            continue
            
        email = user['email']
        email_lower = email.lower()
        
        if email_lower in email_map:
            if email_lower not in duplicates:
                duplicates[email_lower] = [email_map[email_lower]]
            duplicates[email_lower].append(user)
        else:
            email_map[email_lower] = user
    
    # Print results
    if duplicates:
        print("\nFound potential duplicate emails (case-insensitive):")
        for email, user_list in duplicates.items():
            print(f"\nEmail (case-insensitive): {email}")
            for user in user_list:
                print(f"  - ID: {user['_id']}, Email: {user.get('email')}, Name: {user.get('name')}, Status: {user.get('status', 'active')}")
    else:
        print("\nNo duplicate emails found (case-insensitive check).")
    
    # Check for any malformed emails or users without emails
    users_without_email = [u for u in all_users if 'email' not in u]
    if users_without_email:
        print(f"\nFound {len(users_without_email)} users without email field:")
        for user in users_without_email[:5]:  # Show first 5
            print(f"  - ID: {user['_id']}, Name: {user.get('name')}")
        if len(users_without_email) > 5:
            print(f"  ... and {len(users_without_email) - 5} more")
    
    # Check indexes
    print("\nCurrent indexes:")
    for idx_name, idx in db.users.index_information().items():
        print(f"- {idx_name}: {idx.get('key')} (unique: {idx.get('unique', False)})")

if __name__ == "__main__":
    check_all_emails()
