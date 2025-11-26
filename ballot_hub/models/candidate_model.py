from typing import List, Dict, Any
from bson import ObjectId
from database.connection import get_collection


def add_candidate(name: str, election_id: str, photo: str = "") -> bool:
    from bson.errors import InvalidId
    candidates = get_collection("candidates")
    try:
        election_oid = ObjectId(election_id)
    except (InvalidId, ValueError):
        raise ValueError(f"Invalid election_id: {election_id}")
    candidates.insert_one(
        {
            "candidate_name": name,
            "election_id": election_oid,
            "photo": photo,
        }
    )
    return True


def get_candidates(election_id: str) -> List[Dict[str, Any]]:
    from bson.errors import InvalidId
    candidates = get_collection("candidates")
    try:
        election_oid = ObjectId(election_id)
    except (InvalidId, ValueError):
        raise ValueError(f"Invalid election_id: {election_id}")
    docs = list(candidates.find({"election_id": election_oid}))
    result: List[Dict[str, Any]] = []
    for doc in docs:
        result.append(
            {
                "candidate_id": str(doc["_id"]),
                "candidate_name": doc["candidate_name"],
                "election_id": str(doc["election_id"]),
                "photo": doc.get("photo", ""),
            }
        )
    return result

