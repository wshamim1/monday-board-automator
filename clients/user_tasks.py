"""
List tasks assigned to specific users
"""

import requests
from typing import List, Dict, Any


class UserTasksFinder:
    """Client for finding tasks assigned to specific users"""
    
    def __init__(self, api_token: str):
        """
        Initialize UserTasksFinder
        
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
    
    def list_tasks_per_user(self, board_id: int, user_id: int) -> List[Dict[str, Any]]:
        """List all tasks assigned to a specific user"""
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
                    subscribers {
                        id
                        name
                        email
                    }
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            all_tasks = result.get("boards", [{}])[0].get("items", [])
            user_tasks = [task for task in all_tasks if any(sub.get("id") == str(user_id) for sub in task.get("subscribers", []))]
            return user_tasks
        except Exception as e:
            print(f"Error listing tasks per user: {str(e)}")
            return []
    
    def count_tasks_per_user(self, board_id: int) -> Dict[str, int]:
        """Count tasks assigned to each user"""
        query = """
        query {
            boards(ids: [%s]) {
                items {
                    subscribers {
                        id
                        name
                    }
                }
            }
        }
        """ % board_id
        
        try:
            result = self._make_request(query)
            all_tasks = result.get("boards", [{}])[0].get("items", [])
            user_counts = {}
            for task in all_tasks:
                for subscriber in task.get("subscribers", []):
                    user_name = subscriber.get("name", "Unknown")
                    user_counts[user_name] = user_counts.get(user_name, 0) + 1
            return user_counts
        except Exception as e:
            print(f"Error counting tasks: {str(e)}")
            return {}
    
    def print_user_tasks(self, board_id: int, user_id: int, user_name: str = "") -> None:
        """Print all tasks assigned to a user"""
        tasks = self.list_tasks_per_user(board_id, user_id)
        print(f"\n{'='*80}")
        print(f"Tasks for {user_name or f'User {user_id}'}: {len(tasks)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        for task in tasks:
            print(f"{task.get('id', 'N/A'):<15} {task.get('name', 'N/A')[:37]:<40} {task.get('state', 'N/A'):<10} {task.get('created_at', 'N/A')[:10]:<15}")
    
    def print_tasks_per_user_summary(self, board_id: int) -> None:
        """Print a summary of task counts for all users"""
        user_counts = self.count_tasks_per_user(board_id)
        print(f"\n{'='*50}")
        print(f"Task Summary by User")
        print(f"{'='*50}")
        for user_name, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"{user_name:<35} {count:>5} tasks")
