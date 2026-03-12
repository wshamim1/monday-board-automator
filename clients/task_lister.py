"""
List all tasks from a Monday.com board
"""

import requests
from typing import List, Dict, Any


class TaskLister:
    """Client for listing all tasks from a board"""
    
    def __init__(self, api_token: str):
        """
        Initialize TaskLister
        
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
    
    def list_all_tasks(self, board_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all tasks from a board
        
        Args:
            board_id: Monday.com board ID
            limit: Maximum number of tasks to retrieve (default: 100)
            
        Returns:
            List of task dictionaries containing id, name, dates, and columns
        """
        query = """
        query {
            boards(ids: [%s]) {
                items_page(limit: %s) {
                    items {
                        id
                        name
                        created_at
                        updated_at
                        state
                        column_values {
                            id
                            text
                            type
                        }
                    }
                }
            }
        }
        """ % (board_id, limit)
        
        try:
            result = self._make_request(query)
            items_page = result.get("boards", [{}])[0].get("items_page", {})
            tasks = items_page.get("items", [])
            return tasks
        except Exception as e:
            print(f"Error listing tasks: {str(e)}")
            return []
    
    def print_tasks(self, board_id: int, limit: int = 100) -> None:
        """Print all tasks in a formatted table"""
        tasks = self.list_all_tasks(board_id, limit)
        
        print(f"\n{'='*80}")
        print(f"Total Tasks: {len(tasks)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        
        for task in tasks:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:37]
            state = task.get('state', 'N/A')
            created = task.get('created_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<40} {state:<10} {created:<15}")


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    lister = TaskLister(api_token)
    lister.print_tasks(board_id)
