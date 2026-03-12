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
        """
        List all tasks assigned to a specific user
        
        Args:
            board_id: Monday.com board ID
            user_id: Monday.com user ID
            
        Returns:
            List of task dictionaries assigned to the user
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
            
            # Filter tasks by user assignment
            user_tasks = []
            for task in all_tasks:
                subscribers = task.get("subscribers", [])
                if any(sub.get("id") == str(user_id) for sub in subscribers):
                    user_tasks.append(task)
            
            return user_tasks
        except Exception as e:
            print(f"Error listing tasks per user: {str(e)}")
            return []
    
    def print_user_tasks(self, board_id: int, user_id: int, user_name: str = "") -> None:
        """Print all tasks assigned to a user"""
        tasks = self.list_tasks_per_user(board_id, user_id)
        
        print(f"\n{'='*80}")
        print(f"Tasks for {user_name or f'User {user_id}'}: {len(tasks)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        
        for task in tasks:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:37]
            state = task.get('state', 'N/A')
            created = task.get('created_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<40} {state:<10} {created:<15}")
    
    def count_tasks_per_user(self, board_id: int) -> Dict[str, int]:
        """
        Count tasks assigned to each user
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            Dictionary mapping user names to task counts
        """
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
                subscribers = task.get("subscribers", [])
                for subscriber in subscribers:
                    user_name = subscriber.get("name", "Unknown")
                    user_counts[user_name] = user_counts.get(user_name, 0) + 1
            
            return user_counts
        except Exception as e:
            print(f"Error counting tasks: {str(e)}")
            return {}
    
    def print_tasks_per_user_summary(self, board_id: int) -> None:
        """Print a summary of task counts for all users"""
        user_counts = self.count_tasks_per_user(board_id)
        
        print(f"\n{'='*50}")
        print(f"Task Summary by User")
        print(f"{'='*50}")
        
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
        
        for user_name, count in sorted_users:
            print(f"{user_name:<35} {count:>5} tasks")


# Example usage
if __name__ == "__main__":
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    user_id = 987654  # Replace with actual user ID
    
    finder = UserTasksFinder(api_token)
    
    # List tasks for specific user
    finder.print_user_tasks(board_id, user_id, "John Doe")
    
    # Print summary for all users
    finder.print_tasks_per_user_summary(board_id)
