-- MongoDB setup instructions for BallotHub
-- Run these commands inside mongosh (MongoDB shell)

use ballot_hub_db

db.createCollection("users")
db.users.createIndex({email: 1}, {unique: true})

db.createCollection("admins")
db.admins.createIndex({username: 1}, {unique: true})

db.createCollection("elections")
db.elections.createIndex({status: 1, start_date: 1, end_date: 1})

db.createCollection("candidates")
db.candidates.createIndex({election_id: 1})

db.createCollection("votes")
db.votes.createIndex({user_id: 1, election_id: 1}, {unique: true})
db.votes.createIndex({candidate_id: 1, election_id: 1})

-- Seed an admin (replace <hashed_password> with bcrypt hash)
-- db.admins.insertOne({ username: "admin", password: "<hashed_password>" })

