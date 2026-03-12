"""
List tasks created or updated in the current month
"""

import requests
from datetime import datetime
from typing import List, Dict, Any


class CurrentMonthTasksFinder:
    """Client for finding tasks from the current month"""
    
    def __init__(self, api_token: str):
        """
        Initialize CurrentMonthTasksFinder
        
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
    
    def list_tasks_for_current_month(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List tasks created or updated in the current month
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of task dictionaries from current month
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
            
            now = datetime.now()
            current_month_tasks = []
            
            for task in all_tasks:
                try:
                    created_at = datetime.fromisoformat(task.get("created_at", "").replace("Z", "+00:00"))
                    if created_at.year == now.year and created_at.month == now.month:
                        current_month_tasks.append(task)
                except (ValueError, TypeError):
                    continue
            
            return current_month_tasks
        except Exception as e:
            print(f"Error listing current month tasks: {str(e)}")
            return []
    
    def print_current_month_tasks(self, board_id: int) -> None:
        """Print all tasks from current month in formatted table"""
        tasks = self.list_tasks_for_current_month(board_id)
        
        now = datetime.now()
        month_name = now.strftime("%B %Y")
        
        print(f"\n{'='*80}")
        print(f"Tasks Created in {month_name}: {len(tasks)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        
        for task in tasks:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:37]
            state = task.get('state', 'N/A')
            created = task.get('created_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<40} {state:<10} {created:<15}")
    
    def get_tasks_by_month(self, board_id: int, year: int, month: int) -> List[Dict[str, Any]]:
        """
        Get tasks for a specific month
        
        Args:
            board_id: Monday.com board ID
            year: Year (e.g., 2026)
            month: Month (1-12)
            
        Returns:
            List of tasks from specified month
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
            
            month_tasks = []
            for task in all_tasks:
                try:
                    created_at = datetime.fromisoformat(task.get("created_at", "").replace("Z", "+00:00"))
                    if created_at.year == year and created_at.month == month:
                        month_tasks.append(task)
                except (ValueError, TypeError):
                    continue
            
            return month_tasks
        except Exception as e:
            print(f"Error getting tasks by month: {str(e)}")
            return []


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    finder = CurrentMonthTasksFinder(api_token)
    
    # Print current month tasks
    finder.print_current_month_tasks(board_id)
    
    # Get tasks from specific month
    tasks_march_2026 = finder.get_tasks_by_month(board_id, 2026, 3)
    print(f"\nTasks in March 2026: {len(tasks_march_2026)}")
