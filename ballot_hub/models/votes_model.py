from typing import Dict, Any, List
from datetime import datetime
from bson import ObjectId
from pymongo.errors import DuplicateKeyError
from database.connection import get_collection


def record_vote(user_id: str, candidate_id: str, election_id: str) -> bool:
    from bson.errors import InvalidId
    try:
        user_oid = ObjectId(user_id)
        candidate_oid = ObjectId(candidate_id)
        election_oid = ObjectId(election_id)
    except (InvalidId, ValueError):
        raise ValueError(f"Invalid ID format: user_id={user_id}, candidate_id={candidate_id}, election_id={election_id}")
    votes = get_collection("votes")
    try:
        votes.insert_one(
            {
                "user_id": user_oid,
                "candidate_id": candidate_oid,
                "election_id": election_oid,
                "timestamp": datetime.utcnow(),
            }
        )
        return True
    except DuplicateKeyError:
        return False


def count_votes(election_id: str) -> List[Dict[str, Any]]:
    try:
        election_oid = ObjectId(election_id)
    except Exception:
        return []
    candidates = get_collection("candidates")
    votes = get_collection("votes")
    
    # Get all candidates for this election
    candidate_list = list(candidates.find({"election_id": election_oid}))
    results = []
    
    for candidate in candidate_list:
        candidate_oid = candidate["_id"]
        vote_count = votes.count_documents({
            "candidate_id": candidate_oid,
            "election_id": election_oid
        })
        results.append({
            "candidate_id": str(candidate_oid),
            "candidate_name": candidate.get("candidate_name", ""),
            "total_votes": vote_count
        })
    
    # Sort by votes descending, then by name ascending
    results.sort(key=lambda x: (-x["total_votes"], x["candidate_name"]))
    return results

