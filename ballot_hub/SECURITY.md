# Security Features - BallotHub

## Phone Number Security

### 🔒 Confidentiality Measures

1. **Hashing**: Phone numbers are hashed using HMAC-SHA256 before storage
   - Never stored in plain text
   - Uses JWT secret key for additional security
   - One-way hashing (cannot be reversed)

2. **Display Masking**: Phone numbers are masked when displayed
   - Format: `XXXXXX-1234` (only last 4 digits visible)
   - Admin dashboard shows masked versions only
   - User profile shows masked version only

3. **Database Storage**:
   - `phone_hash`: HMAC-SHA256 hash of full phone number
   - `phone_last4`: Last 4 digits for display purposes only
   - No plain text phone number stored

### ✅ Validation

1. **Format Validation**:
   - Must be exactly 10 digits (Indian format)
   - Must start with 6, 7, 8, or 9 (valid mobile number prefix)
   - Only numeric characters allowed
   - Supports international format (10-15 digits)

2. **Normalization**:
   - Automatically removes spaces, dashes, and country codes
   - Standardizes to 10-digit format for Indian numbers
   - Ensures consistent storage format

3. **Real-time Validation**:
   - Client-side validation on registration form
   - Server-side validation before storage
   - Clear error messages for invalid formats

### 🔐 Security Best Practices

- ✅ Phone numbers are never logged
- ✅ Phone numbers are never returned in API responses
- ✅ Only masked versions displayed in UI
- ✅ Unique constraint on hashed phone prevents duplicates
- ✅ Cannot be retrieved even with database access

## Password Security

- ✅ Bcrypt hashing with 12 rounds
- ✅ Never stored in plain text
- ✅ Secure password verification

## JWT Security

- ✅ Secure token generation
- ✅ Token expiration (8 hours)
- ✅ Role-based access control
- ✅ Secure secret key management
