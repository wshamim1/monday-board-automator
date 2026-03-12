"""
Get comprehensive board information and statistics
"""

import requests
from typing import Dict, Any, List


class BoardInfoFinder:
    """Client for getting board information and statistics"""
    
    def __init__(self, api_token: str):
        """
        Initialize BoardInfoFinder
        
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
    
    def get_board_info(self, board_id: int) -> Dict[str, Any]:
        """
        Get basic information about a board
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            Board information dictionary
        """
        query = """
        query {
            boards(ids: [%s]) {
                id
                name
                description
                state
                type
                owner {
                    id
                    name
                    email
                }
                users_count
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            boards = result.get("boards", [])
            return boards[0] if boards else {}
        except Exception as e:
            print(f"Error getting board info: {str(e)}")
            return {}
    
    def get_board_statistics(self, board_id: int) -> Dict[str, Any]:
        """
        Get comprehensive statistics about the board
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            Dictionary with board statistics
        """
        query = """
        query {
            boards(ids: [%s]) {
                id
                name
                items {
                    id
                    state
                    created_at
                }
                users {
                    id
                    name
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            board = result.get("boards", [{}])[0]
            
            items = board.get("items", [])
            users = board.get("users", [])
            
            active_items = [item for item in items if item.get("state") != "archived"]
            archived_items = [item for item in items if item.get("state") == "archived"]
            
            stats = {
                "board_name": board.get("name"),
                "total_items": len(items),
                "active_items": len(active_items),
                "archived_items": len(archived_items),
                "total_users": len(users),
                "completion_rate": (len(archived_items) / len(items) * 100) if items else 0
            }
            
            return stats
        except Exception as e:
            print(f"Error getting board statistics: {str(e)}")
            return {}
    
    def print_board_info(self, board_id: int) -> None:
        """Print board information in formatted output"""
        board = self.get_board_info(board_id)
        
        if not board:
            print("No board information found")
            return
        
        print(f"\n{'='*70}")
        print(f"BOARD INFORMATION")
        print(f"{'='*70}")
        print(f"Name:        {board.get('name', 'N/A')}")
        print(f"ID:          {board.get('id', 'N/A')}")
        print(f"Description: {board.get('description', 'N/A')}")
        print(f"State:       {board.get('state', 'N/A')}")
        print(f"Type:        {board.get('type', 'N/A')}")
        print(f"Users Count: {board.get('users_count', 'N/A')}")
        
        owner = board.get('owner', {})
        if owner:
            print(f"Owner:       {owner.get('name', 'N/A')} ({owner.get('email', 'N/A')})")
        
        print(f"{'='*70}")
    
    def print_board_statistics(self, board_id: int) -> None:
        """Print board statistics in formatted output"""
        stats = self.get_board_statistics(board_id)
        
        if not stats:
            print("No statistics available")
            return
        
        print(f"\n{'='*70}")
        print(f"BOARD STATISTICS - {stats.get('board_name', 'Unknown')}")
        print(f"{'='*70}")
        print(f"Total Items:        {stats.get('total_items', 0)}")
        print(f"Active Items:       {stats.get('active_items', 0)}")
        print(f"Archived Items:     {stats.get('archived_items', 0)}")
        print(f"Total Users:        {stats.get('total_users', 0)}")
        
        completion = stats.get('completion_rate', 0)
        print(f"Completion Rate:    {completion:.1f}%")
        
        # Print progress bar
        bar_length = 40
        filled = int(bar_length * completion / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"Progress:           [{bar}] {completion:.1f}%")
        
        print(f"{'='*70}")
    
    def compare_boards(self, board_ids: List[int]) -> None:
        """Compare statistics across multiple boards"""
        print(f"\n{'='*80}")
        print(f"BOARD COMPARISON")
        print(f"{'='*80}")
        print(f"{'Board Name':<30} {'Total':<8} {'Active':<8} {'Complete':<10}")
        print(f"{'-'*80}")
        
        for board_id in board_ids:
            stats = self.get_board_statistics(board_id)
            if stats:
                name = stats.get('board_name', 'Unknown')[:27]
                total = stats.get('total_items', 0)
                active = stats.get('active_items', 0)
                complete = f"{stats.get('completion_rate', 0):.1f}%"
                
                print(f"{name:<30} {total:<8} {active:<8} {complete:<10}")


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    finder = BoardInfoFinder(api_token)
    
    # Print board information
    finder.print_board_info(board_id)
    
    # Print board statistics
    finder.print_board_statistics(board_id)
    
    # Compare multiple boards
    # finder.compare_boards([123456789, 987654321])
