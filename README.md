# BallotHub - Secure Online Voting System

A complete online voting system built with Flask, MongoDB, and JWT authentication.

## Features

- ✅ Secure user registration with phone number validation
- ✅ Admin approval system
- ✅ Candidate management
- ✅ Election creation and control (start/stop)
- ✅ One-time voting per user
- ✅ Results dashboard for admin
- ✅ JWT authentication for users & admin
- ✅ Responsive Bootstrap frontend

## Tech Stack

- **Backend**: Python Flask
- **Database**: MongoDB
- **Authentication**: JWT + bcrypt password hashing
- **Frontend**: HTML, CSS, Bootstrap, JavaScript

## Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **MongoDB** installed and running (or use Docker)

### Installation & Run

1. **Navigate to project folder:**
   ```powershell
   cd "F:\Ballot Hub\ballot_hub"
   ```

2. **Create virtual environment (if not exists):**
   ```powershell
   py -3 -m venv venv
   ```

3. **Activate virtual environment:**
   ```powershell
   .\venv\Scripts\activate
   ```

4. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Start MongoDB** (if not running as a service):
   ```powershell
   mongod
   ```
   Or use Docker:
   ```powershell
   docker run -d --name ballot-mongo -p 27017:27017 mongo:6
   ```

6. **Run the application:**
   ```powershell
   python run.py
   ```
   
   Or directly:
   ```powershell
   python app.py
   ```

The app will automatically:
- Connect to MongoDB
- Create database and collections
- Set up indexes
- Create default admin user
- Create a sample election with candidates

## Default Credentials

**Admin:**
- Username: `admin`
- Password: `AdminPass123`

## Access Pages

Once the server is running on `http://127.0.0.1:5000`:

### User Pages:
- **Register**: http://127.0.0.1:5000/register
- **Login**: http://127.0.0.1:5000/login
- **Vote**: http://127.0.0.1:5000/vote
- **Profile**: http://127.0.0.1:5000/profile

### Admin Pages:
- **Login**: http://127.0.0.1:5000/admin
- **Dashboard**: http://127.0.0.1:5000/admin/dashboard
- **Add Candidate**: http://127.0.0.1:5000/admin/add_candidate
- **Create Election**: http://127.0.0.1:5000/admin/create_election

## API Endpoints

### User APIs:
- `POST /api/register` - Register new user
- `POST /api/login` - User login
- `GET /api/elections` - Get active election (requires JWT)
- `GET /api/candidates/<election_id>` - Get candidates (requires JWT)
- `POST /api/vote` - Cast vote (requires JWT)

### Admin APIs:
- `POST /api/admin/login` - Admin login
- `GET /api/admin/users` - List all users (requires admin JWT)
- `PUT /api/admin/approve_user/<user_id>` - Approve user (requires admin JWT)
- `POST /api/admin/add_candidate` - Add candidate (requires admin JWT)
- `POST /api/admin/create_election` - Create election (requires admin JWT)
- `GET /api/admin/results/<election_id>` - Get results (requires admin JWT)

## Project Structure

```
ballot_hub/
├── app.py                 # Main Flask application
├── run.py                 # Simple run script
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── database/
│   ├── connection.py     # MongoDB connection
│   ├── init_db.py        # Database initialization
│   └── schema.sql        # MongoDB setup instructions
├── models/               # Data models
│   ├── user_model.py
│   ├── admin_model.py
│   ├── candidate_model.py
│   ├── election_model.py
│   └── votes_model.py
├── controllers/          # Business logic
│   ├── user_controller.py
│   └── admin_controller.py
├── routes/               # API routes
│   ├── user_routes.py
│   └── admin_routes.py
├── templates/            # HTML templates
│   ├── user/
│   ├── admin/
│   └── shared/
└── static/              # Static files
    ├── css/
    ├── js/
    └── img/
```

## Environment Variables (Optional)

You can set these environment variables before running:

```powershell
$env:MONGO_URI="mongodb://localhost:27017"
$env:MONGO_DB_NAME="ballot_hub_db"
$env:JWT_SECRET_KEY="your-secret-key-here"
```

If not set, defaults will be used.

## Troubleshooting

1. **MongoDB connection error**: Make sure MongoDB is running
2. **Port 5000 already in use**: Change port in `app.py` or `run.py`
3. **Import errors**: Make sure virtual environment is activated and dependencies are installed

## License

This project is for educational purposes.
