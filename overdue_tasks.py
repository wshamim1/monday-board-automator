"""
List overdue tasks (tasks with due dates in the past)
"""

import requests
from datetime import datetime
from typing import List, Dict, Any


class OverdueTasksFinder:
    """Client for finding overdue tasks"""
    
    def __init__(self, api_token: str):
        """
        Initialize OverdueTasksFinder
        
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
    
    def list_overdue_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List tasks with due dates that have passed
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of overdue task dictionaries
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
            overdue_tasks = []
            
            for task in all_tasks:
                for column in task.get("column_values", []):
                    if column.get("type") == "date":
                        try:
                            due_date = datetime.fromisoformat(column.get("text", ""))
                            if due_date < now and task.get("state") != "archived":
                                task['due_date'] = column.get("text")
                                overdue_tasks.append(task)
                                break
                        except (ValueError, TypeError):
                            continue
            
            return overdue_tasks
        except Exception as e:
            print(f"Error listing overdue tasks: {str(e)}")
            return []
    
    def list_upcoming_tasks(self, board_id: int, days: int = 7) -> List[Dict[str, Any]]:
        """
        List tasks with due dates coming up
        
        Args:
            board_id: Monday.com board ID
            days: Number of days to look ahead (default: 7)
            
        Returns:
            List of upcoming task dictionaries
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
            future_date = datetime.now().replace(hour=23, minute=59, second=59)
            future_date = future_date.replace(day=future_date.day + days)
            
            upcoming_tasks = []
            
            for task in all_tasks:
                for column in task.get("column_values", []):
                    if column.get("type") == "date":
                        try:
                            due_date = datetime.fromisoformat(column.get("text", ""))
                            if now <= due_date <= future_date and task.get("state") != "archived":
                                task['due_date'] = column.get("text")
                                upcoming_tasks.append(task)
                                break
                        except (ValueError, TypeError):
                            continue
            
            return upcoming_tasks
        except Exception as e:
            print(f"Error listing upcoming tasks: {str(e)}")
            return []
    
    def print_overdue_tasks(self, board_id: int) -> None:
        """Print all overdue tasks"""
        overdue = self.list_overdue_tasks(board_id)
        
        print(f"\n{'='*80}")
        print(f"OVERDUE TASKS: {len(overdue)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<35} {'Due Date':<15} {'Days Late':<10}")
        print(f"{'-'*80}")
        
        now = datetime.now()
        
        for task in overdue:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:32]
            due_date = task.get('due_date', 'N/A')[:10]
            
            try:
                due_dt = datetime.fromisoformat(task.get('due_date', '').replace("Z", "+00:00"))
                days_late = (now - due_dt).days
                days_str = f"{days_late} days"
            except (ValueError, TypeError):
                days_str = "N/A"
            
            print(f"{task_id:<15} {name:<35} {due_date:<15} {days_str:<10}")
    
    def print_upcoming_tasks(self, board_id: int, days: int = 7) -> None:
        """Print upcoming tasks due within specified days"""
        upcoming = self.list_upcoming_tasks(board_id, days)
        
        print(f"\n{'='*80}")
        print(f"UPCOMING TASKS (Next {days} Days): {len(upcoming)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<35} {'Due Date':<15} {'Days Left':<10}")
        print(f"{'-'*80}")
        
        now = datetime.now()
        
        for task in upcoming:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:32]
            due_date = task.get('due_date', 'N/A')[:10]
            
            try:
                due_dt = datetime.fromisoformat(task.get('due_date', '').replace("Z", "+00:00"))
                days_left = (due_dt - now).days
                days_str = f"{days_left} days"
            except (ValueError, TypeError):
                days_str = "N/A"
            
            print(f"{task_id:<15} {name:<35} {due_date:<15} {days_str:<10}")


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    finder = OverdueTasksFinder(api_token)
    
    # Print overdue tasks
    finder.print_overdue_tasks(board_id)
    
    # Print upcoming tasks for next 7 days
    finder.print_upcoming_tasks(board_id, days=7)
    
    # Print upcoming tasks for next 30 days
    finder.print_upcoming_tasks(board_id, days=30)
