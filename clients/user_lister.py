"""
List all users from a Monday.com board
"""

import requests
from typing import List, Dict, Any


class UserLister:
    """Client for listing users with board access"""
    
    def __init__(self, api_token: str):
        """
        Initialize UserLister
        
        Args:
            api_token: Monday.com API token
        """
        self.api_token = api_token
        self.api_url = "https://api.monday.com/v2"
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, query: str) -> Dict[str, Any]:
        """Make GraphQL request to Monday.com API"""
        payload = {"query": query}
        response = requests.post(self.api_url, json=payload, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise Exception(f"GraphQL Error: {data['errors']}")
        
        return data.get("data", {})
    
    def list_users(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List all users with access to a board
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of user dictionaries with id, name, and email
        """
        query = """
        query {
            boards(ids: [%s]) {
                users {
                    id
                    email
                    name
                    photo_thumb
                    is_pending
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            users = result.get("boards", [{}])[0].get("users", [])
            return users
        except Exception as e:
            print(f"Error listing users: {str(e)}")
            return []
    
    def print_users(self, board_id: int) -> None:
        """Print all users in a formatted table"""
        users = self.list_users(board_id)
        
        print(f"\n{'='*80}")
        print(f"Total Users: {len(users)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Name':<25} {'Email':<40} {'Status':<10}")
        print(f"{'-'*80}")
        
        for user in users:
            user_id = user.get('id', 'N/A')
            name = user.get('name', 'N/A')[:22]
            email = user.get('email', 'N/A')[:37]
            status = "Pending" if user.get('is_pending') else "Active"
            
            print(f"{user_id:<15} {name:<25} {email:<40} {status:<10}")
    
    def get_user_by_email(self, board_id: int, email: str) -> Dict[str, Any]:
        """
        Find a user by email address
        
        Args:
            board_id: Monday.com board ID
            email: Email address to search for
            
        Returns:
            User dictionary or empty dict if not found
        """
        users = self.list_users(board_id)
        for user in users:
            if user.get('email') == email:
                return user
        return {}


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    lister = UserLister(api_token)
    lister.print_users(board_id)
    
    # Find specific user
    user = lister.get_user_by_email(board_id, "user@example.com")
    if user:
        print(f"\nFound user: {user['name']} ({user['email']})")
