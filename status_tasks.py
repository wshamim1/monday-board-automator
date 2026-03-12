"""
List tasks by status (Done, In Progress, Todo, etc.)
"""

import requests
from typing import List, Dict, Any


class StatusTasksFinder:
    """Client for filtering tasks by status"""
    
    def __init__(self, api_token: str):
        """
        Initialize StatusTasksFinder
        
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
    
    def list_tasks_by_status(self, board_id: int, status: str) -> List[Dict[str, Any]]:
        """
        List tasks with a specific status
        
        Args:
            board_id: Monday.com board ID
            status: Status value to filter by (e.g., "Done", "In Progress", "Todo")
            
        Returns:
            List of tasks matching the status
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
            filtered_tasks = []
            
            for task in all_tasks:
                for column in task.get("column_values", []):
                    if column.get("type") == "status" and column.get("text") == status:
                        filtered_tasks.append(task)
                        break
            
            return filtered_tasks
        except Exception as e:
            print(f"Error listing tasks by status: {str(e)}")
            return []
    
    def get_all_statuses(self, board_id: int) -> List[str]:
        """
        Get all available statuses in the board
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of unique status values
        """
        query = """
        query {
            boards(ids: [%s]) {
                items {
                    column_values {
                        type
                        text
                    }
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            all_tasks = result.get("boards", [{}])[0].get("items", [])
            
            statuses = set()
            for task in all_tasks:
                for column in task.get("column_values", []):
                    if column.get("type") == "status" and column.get("text"):
                        statuses.add(column.get("text"))
            
            return sorted(list(statuses))
        except Exception as e:
            print(f"Error getting statuses: {str(e)}")
            return []
    
    def print_tasks_by_status(self, board_id: int, status: str) -> None:
        """Print tasks with a specific status"""
        tasks = self.list_tasks_by_status(board_id, status)
        
        print(f"\n{'='*80}")
        print(f"Tasks with Status '{status}': {len(tasks)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        
        for task in tasks:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:37]
            state = task.get('state', 'N/A')
            created = task.get('created_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<40} {state:<10} {created:<15}")
    
    def print_status_summary(self, board_id: int) -> None:
        """Print summary of tasks by all statuses"""
        statuses = self.get_all_statuses(board_id)
        
        print(f"\n{'='*50}")
        print(f"Task Summary by Status")
        print(f"{'='*50}")
        
        for status in statuses:
            count = len(self.list_tasks_by_status(board_id, status))
            print(f"{status:<35} {count:>5} tasks")
        
        print(f"{'='*50}")


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    finder = StatusTasksFinder(api_token)
    
    # Print status summary
    finder.print_status_summary(board_id)
    
    # Print tasks for specific statuses
    finder.print_tasks_by_status(board_id, "Done")
    finder.print_tasks_by_status(board_id, "In Progress")
    finder.print_tasks_by_status(board_id, "Todo")
