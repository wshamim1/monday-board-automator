"""
List closed/archived tasks from a Monday.com board
"""

import requests
from typing import List, Dict, Any


class ClosedTasksFinder:
    """Client for finding closed/archived tasks"""
    
    def __init__(self, api_token: str):
        """
        Initialize ClosedTasksFinder
        
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
    
    def list_closed_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List all closed/archived tasks
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of closed task dictionaries
        """
        query = """
        query {
            boards(ids: [%s]) {
                items {
                    id
                    name
                    created_at
                    updated_at
                    state
                    column_values {
                        id
                        text
                        title
                        type
                    }
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            all_tasks = result.get("boards", [{}])[0].get("items", [])
            closed_tasks = [task for task in all_tasks if task.get("state") == "archived"]
            return closed_tasks
        except Exception as e:
            print(f"Error listing closed tasks: {str(e)}")
            return []
    
    def list_active_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List all active/open tasks
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of active task dictionaries
        """
        query = """
        query {
            boards(ids: [%s]) {
                items {
                    id
                    name
                    created_at
                    updated_at
                    state
                    column_values {
                        id
                        text
                        title
                        type
                    }
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            all_tasks = result.get("boards", [{}])[0].get("items", [])
            active_tasks = [task for task in all_tasks if task.get("state") != "archived"]
            return active_tasks
        except Exception as e:
            print(f"Error listing active tasks: {str(e)}")
            return []
    
    def print_closed_tasks(self, board_id: int) -> None:
        """Print all closed tasks in formatted table"""
        closed = self.list_closed_tasks(board_id)
        
        print(f"\n{'='*80}")
        print(f"Closed/Archived Tasks: {len(closed)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Updated':<15}")
        print(f"{'-'*80}")
        
        for task in closed:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:37]
            state = task.get('state', 'N/A')
            updated = task.get('updated_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<40} {state:<10} {updated:<15}")
    
    def print_active_tasks(self, board_id: int) -> None:
        """Print all active tasks in formatted table"""
        active = self.list_active_tasks(board_id)
        
        print(f"\n{'='*80}")
        print(f"Active Tasks: {len(active)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        
        for task in active:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:37]
            state = task.get('state', 'N/A')
            created = task.get('created_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<40} {state:<10} {created:<15}")
    
    def print_task_summary(self, board_id: int) -> None:
        """Print summary of active vs closed tasks"""
        active = self.list_active_tasks(board_id)
        closed = self.list_closed_tasks(board_id)
        total = len(active) + len(closed)
        
        print(f"\n{'='*50}")
        print(f"Task Status Summary")
        print(f"{'='*50}")
        print(f"Total Tasks:      {total}")
        print(f"Active Tasks:     {len(active)}")
        print(f"Closed Tasks:     {len(closed)}")
        if total > 0:
            completion_rate = (len(closed) / total) * 100
            print(f"Completion Rate:  {completion_rate:.1f}%")
        print(f"{'='*50}")


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    finder = ClosedTasksFinder(api_token)
    
    # Print task summary
    finder.print_task_summary(board_id)
    
    # Print active tasks
    finder.print_active_tasks(board_id)
    
    # Print closed tasks
    finder.print_closed_tasks(board_id)
