from typing import Optional, Dict, Any, List
from datetime import datetime
from bson import ObjectId
from database.connection import get_collection

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def create_election(election_name: str, start_date: str, end_date: str, status: str = "active") -> bool:
    elections = get_collection("elections")
    start_dt = datetime.strptime(start_date, DATETIME_FORMAT)
    end_dt = datetime.strptime(end_date, DATETIME_FORMAT)
    elections.insert_one(
        {
            "election_name": election_name,
            "start_date": start_dt,
            "end_date": end_dt,
            "status": status,
        }
    )
    return True


def get_active_election() -> Optional[Dict[str, Any]]:
    """Get the first active election (for backward compatibility)"""
    active_elections = get_all_active_elections()
    return active_elections[0] if active_elections else None


def get_all_active_elections() -> List[Dict[str, Any]]:
    """Get all active elections that are currently within their date range"""
    elections = get_collection("elections")
    now = datetime.utcnow()
    docs = list(elections.find(
        {
            "status": "active",
            "start_date": {"$lte": now},
            "end_date": {"$gte": now},
        }
    ).sort("start_date", -1))
    
    result = []
    for doc in docs:
        result.append({
            "election_id": str(doc["_id"]),
            "election_name": doc["election_name"],
            "start_date": doc["start_date"].isoformat(),
            "end_date": doc["end_date"].isoformat(),
            "status": doc["status"],
        })
    return result


def get_all_elections() -> List[Dict[str, Any]]:
    """Get all elections (for admin to select when adding candidates)"""
    elections = get_collection("elections")
    docs = list(elections.find({}).sort("start_date", -1))
    result = []
    for doc in docs:
        result.append({
            "election_id": str(doc["_id"]),
            "election_name": doc["election_name"],
            "start_date": doc["start_date"].isoformat() if isinstance(doc["start_date"], datetime) else str(doc["start_date"]),
            "end_date": doc["end_date"].isoformat() if isinstance(doc["end_date"], datetime) else str(doc["end_date"]),
            "status": doc["status"],
        })
    return result


def get_election_by_id(election_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific election by ID"""
    from bson.errors import InvalidId
    elections = get_collection("elections")
    try:
        doc = elections.find_one({"_id": ObjectId(election_id)})
        if not doc:
            return None
        return {
            "election_id": str(doc["_id"]),
            "election_name": doc["election_name"],
            "start_date": doc["start_date"].isoformat() if isinstance(doc["start_date"], datetime) else str(doc["start_date"]),
            "end_date": doc["end_date"].isoformat() if isinstance(doc["end_date"], datetime) else str(doc["end_date"]),
            "status": doc["status"],
        }
    except (InvalidId, ValueError):
        return None


def update_election_status(election_id: str, status: str) -> bool:
    """Update election status (active/inactive)"""
    from bson.errors import InvalidId
    elections = get_collection("elections")
    if status not in ("active", "inactive"):
        raise ValueError(f"Invalid status: {status}. Must be 'active' or 'inactive'")
    try:
        result = elections.update_one(
            {"_id": ObjectId(election_id)},
            {"$set": {"status": status}}
        )
        return result.modified_count > 0
    except (InvalidId, ValueError):
        raise ValueError(f"Invalid election_id: {election_id}")


def delete_election(election_id: str) -> Dict[str, Any]:
    """
    Delete an election and its associated candidates and votes.
    Returns dict with success status and message.
    """
    from bson.errors import InvalidId
    
    elections = get_collection("elections")
    candidates = get_collection("candidates")
    votes = get_collection("votes")
    
    try:
        election_oid = ObjectId(election_id)
    except (InvalidId, ValueError):
        return {"success": False, "message": "Invalid election ID"}
    
    # Check if election exists
    election = elections.find_one({"_id": election_oid})
    if not election:
        return {"success": False, "message": "Election not found"}
    
    # Check if election has votes (optional: warn but allow deletion)
    vote_count = votes.count_documents({"election_id": election_oid})
    candidate_count = candidates.count_documents({"election_id": election_oid})
    
    # Delete associated votes
    votes.delete_many({"election_id": election_oid})
    
    # Delete associated candidates
    candidates.delete_many({"election_id": election_oid})
    
    # Delete the election
    elections.delete_one({"_id": election_oid})
    
    return {
        "success": True,
        "message": f"Election deleted successfully. Removed {vote_count} votes and {candidate_count} candidates."
    }

