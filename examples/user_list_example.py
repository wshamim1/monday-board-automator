"""
Simple User List Example
List all users (owners and subscribers) from a Monday.com board
"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients import UserLister

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API token and board ID from environment variables
    api_token = os.getenv("MONDAY_API_TOKEN")
    board_id_str = os.getenv("MONDAY_BOARD_ID")
    
    # Validate credentials
    if not api_token or api_token == "your_api_token_here":
        print("❌ Error: Please set MONDAY_API_TOKEN in your .env file")
        return
    
    if not board_id_str:
        print("❌ Error: Please set MONDAY_BOARD_ID in your .env file")
        return
    
    try:
        board_id = int(board_id_str)
    except ValueError:
        print("❌ Error: MONDAY_BOARD_ID must be a valid number")
        return
    
    print("\n" + "="*70)
    print("MONDAY.COM BOARD USERS")
    print("="*70)
    
    # Create user lister instance
    user_lister = UserLister(api_token)
    
    # Get and print all users
    users = user_lister.list_users(board_id)
    
    if users:
        print(f"\nTotal Users: {len(users)}")
        print("-" * 70)
        print(f"{'ID':<15} {'Name':<30} {'Email':<40}")
        print("-" * 70)
        
        for user in users:
            user_id = user.get('id', 'N/A')
            name = user.get('name', 'N/A')[:27]
            email = user.get('email', 'N/A')[:37]
            print(f"{user_id:<15} {name:<30} {email:<40}")
        
        print("="*70)
        
        # Example: Find a specific user by email
        print("\n📧 Find User by Email:")
        print("-" * 70)
        example_email = input("Enter email to search (or press Enter to skip): ").strip()
        
        if example_email:
            user = user_lister.get_user_by_email(board_id, example_email)
            if user:
                print(f"✅ Found: {user.get('name')} (ID: {user.get('id')})")
            else:
                print(f"❌ No user found with email: {example_email}")
    else:
        print("\n❌ No users found or error occurred")
    
    print()

if __name__ == "__main__":
    main()


