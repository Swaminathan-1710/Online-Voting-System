"""
Quick script to check what elections exist in the database
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.connection import get_collection
from bson import ObjectId


def check_elections():
    """List all elections in the database"""
    try:
        elections = get_collection("elections")
        
        print("=" * 60)
        print("Current Elections in Database")
        print("=" * 60)
        
        all_elections = list(elections.find({}))
        
        if not all_elections:
            print("✓ No elections found. Database is clean.")
            return
        
        print(f"\nFound {len(all_elections)} election(s):\n")
        
        for election in all_elections:
            print(f"Election Name: {election.get('election_name', 'N/A')}")
            print(f"Status: {election.get('status', 'N/A')}")
            print(f"Start Date: {election.get('start_date', 'N/A')}")
            print(f"End Date: {election.get('end_date', 'N/A')}")
            print(f"Election ID: {election.get('_id')}")
            print("-" * 60)
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    check_elections()

