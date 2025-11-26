"""
Script to remove the default sample election created by init_db.py
Run this to clean up the "General Election 2024" sample election
"""
from database.connection import get_collection
from bson import ObjectId
import sys


def remove_sample_election(auto_confirm=False):
    """Remove the sample 'General Election 2024' election and its candidates"""
    try:
        elections = get_collection("elections")
        candidates = get_collection("candidates")
        votes = get_collection("votes")
        
        print("=" * 60)
        print("Removing Sample Election")
        print("=" * 60)
        
        # Find sample elections (case-insensitive search for "General Election")
        import re
        sample_elections = list(elections.find({
            "election_name": {"$regex": re.compile("General Election", re.IGNORECASE)}
        }))
        
        if not sample_elections:
            print("✓ No sample elections found. Nothing to remove.")
            return True
        
        print(f"\nFound {len(sample_elections)} sample election(s) to remove:")
        total_candidates = 0
        total_votes = 0
        for e in sample_elections:
            election_id = e["_id"]
            candidate_count = candidates.count_documents({"election_id": election_id})
            vote_count = votes.count_documents({"election_id": election_id})
            total_candidates += candidate_count
            total_votes += vote_count
            print(f"  - {e.get('election_name')} (ID: {e.get('_id')})")
            print(f"    → {candidate_count} candidate(s), {vote_count} vote(s)")
        
        print(f"\nThis will delete:")
        print(f"  - {len(sample_elections)} election(s)")
        print(f"  - {total_candidates} candidate(s)")
        print(f"  - {total_votes} vote(s)")
        
        # Auto-confirm if requested, otherwise ask (before deletion)
        if not auto_confirm:
            response = input(f"\nDelete {len(sample_elections)} sample election(s)? (yes/no): ")
            if response.lower() != 'yes':
                print("Cancelled. Sample elections not deleted.")
                return False
        else:
            print("\nAuto-removing sample elections...")
        
        # Process all sample elections
        total_deleted = 0
        for sample_election in sample_elections:
            election_id = sample_election["_id"]
            election_name = sample_election.get('election_name', 'Unknown')
            
            # Count related data
            candidate_count = candidates.count_documents({"election_id": election_id})
            vote_count = votes.count_documents({"election_id": election_id})
            
            print(f"\nRemoving: {election_name}")
            
            # Delete votes
            if vote_count > 0:
                votes.delete_many({"election_id": election_id})
                print(f"  ✓ Deleted {vote_count} vote(s)")
            
            # Delete candidates
            if candidate_count > 0:
                candidates.delete_many({"election_id": election_id})
                print(f"  ✓ Deleted {candidate_count} candidate(s)")
            
            # Delete election
            elections.delete_one({"_id": election_id})
            print(f"  ✓ Deleted election: {election_name}")
            total_deleted += 1
        
        print(f"\n✓ Successfully removed {total_deleted} sample election(s)!")
        return True
        
    except Exception as e:
        print(f"\n✗ Failed to remove sample election: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Auto-confirm if --yes flag is passed
    auto_confirm = "--yes" in sys.argv or "-y" in sys.argv
    remove_sample_election(auto_confirm=auto_confirm)

