"""
Monday.com Board Automation Client
Provides methods to interact with Monday.com API for task and user management
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


class MondayClient:
    """Client for interacting with Monday.com API"""
    
    def __init__(self, api_token: str, api_url: str = "https://api.monday.com/v2"):
        """
        Initialize Monday.com client
        
        Args:
            api_token: Your Monday.com API token
            api_url: Monday.com API endpoint (default is v2)
        """
        self.api_token = api_token
        self.api_url = api_url
        self.headers = {
            "Authorization": api_token,
            "Content-Type": "application/json"
        }
    
    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Make a GraphQL request to Monday.com API
        
        Args:
            query: GraphQL query string
            variables: GraphQL variables dictionary
            
        Returns:
            Response data as dictionary
            
        Raises:
            Exception: If API request fails
        """
        payload = {
            "query": query
        }
        if variables:
            payload["variables"] = variables
        
        try:
            response = requests.post(
                self.api_url,
                json=payload,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            if "errors" in data:
                raise Exception(f"GraphQL Error: {data['errors']}")
            
            return data.get("data", {})
        except requests.exceptions.RequestException as e:
            raise Exception(f"API Request Failed: {str(e)}")
    
    def list_all_tasks(self, board_id: int, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List all tasks from a board
        
        Args:
            board_id: Monday.com board ID
            limit: Maximum number of tasks to retrieve
            
        Returns:
            List of task dictionaries
        """
        query = """
        query {
            boards(ids: [%s]) {
                items(limit: %s) {
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
        """ % (board_id, limit)
        
        try:
            result = self._make_request(query)
            tasks = result.get("boards", [{}])[0].get("items", [])
            return tasks
        except Exception as e:
            print(f"Error listing tasks: {str(e)}")
            return []
    
    def list_users(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List all users with access to a board
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of user dictionaries
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
    
    def list_tasks_per_user(self, board_id: int, user_id: int) -> List[Dict[str, Any]]:
        """
        List all tasks assigned to a specific user
        
        Args:
            board_id: Monday.com board ID
            user_id: Monday.com user ID
            
        Returns:
            List of task dictionaries assigned to user
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
    
    def list_tasks_for_current_month(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List tasks created or updated in the current month
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of tasks from current month
        """
        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        
        all_tasks = self.list_all_tasks(board_id)
        current_month_tasks = []
        
        for task in all_tasks:
            try:
                created_at = datetime.fromisoformat(task.get("created_at", "").replace("Z", "+00:00"))
                if created_at.year == now.year and created_at.month == now.month:
                    current_month_tasks.append(task)
            except (ValueError, TypeError):
                continue
        
        return current_month_tasks
    
    def list_closed_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List all closed or completed tasks
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of closed task dictionaries
        """
        all_tasks = self.list_all_tasks(board_id)
        closed_tasks = [task for task in all_tasks if task.get("state") == "archived"]
        return closed_tasks
    
    def list_active_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List all active/open tasks
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of active task dictionaries
        """
        all_tasks = self.list_all_tasks(board_id)
        active_tasks = [task for task in all_tasks if task.get("state") != "archived"]
        return active_tasks
    
    def get_task_by_id(self, task_id: int) -> Dict[str, Any]:
        """
        Get a specific task by ID
        
        Args:
            task_id: Monday.com task ID
            
        Returns:
            Task dictionary
        """
        query = """
        query {
            items(ids: [%s]) {
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
                creator {
                    id
                    name
                    email
                }
            }
        }
        """ % task_id
        
        try:
            result = self._make_request(query)
            tasks = result.get("items", [])
            return tasks[0] if tasks else {}
        except Exception as e:
            print(f"Error getting task: {str(e)}")
            return {}
    
    def list_tasks_by_status(self, board_id: int, status: str) -> List[Dict[str, Any]]:
        """
        List tasks with a specific status
        
        Args:
            board_id: Monday.com board ID
            status: Status value to filter by (e.g., "Done", "In Progress", "Todo")
            
        Returns:
            List of tasks matching status
        """
        all_tasks = self.list_all_tasks(board_id)
        filtered_tasks = []
        
        for task in all_tasks:
            for column in task.get("column_values", []):
                if column.get("type") == "status" and column.get("text") == status:
                    filtered_tasks.append(task)
                    break
        
        return filtered_tasks
    
    def list_overdue_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """
        List tasks with due dates that have passed
        
        Args:
            board_id: Monday.com board ID
            
        Returns:
            List of overdue tasks
        """
        all_tasks = self.list_all_tasks(board_id)
        now = datetime.now()
        overdue_tasks = []
        
        for task in all_tasks:
            for column in task.get("column_values", []):
                if column.get("type") == "date":
                    try:
                        due_date = datetime.fromisoformat(column.get("text", ""))
                        if due_date < now and task.get("state") != "archived":
                            overdue_tasks.append(task)
                            break
                    except (ValueError, TypeError):
                        continue
        
        return overdue_tasks
    
    def get_board_info(self, board_id: int) -> Dict[str, Any]:
        """
        Get information about a board
        
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
    
    def print_tasks_summary(self, board_id: int) -> None:
        """
        Print a summary of all tasks on the board
        
        Args:
            board_id: Monday.com board ID
        """
        board_info = self.get_board_info(board_id)
        all_tasks = self.list_all_tasks(board_id)
        active_tasks = self.list_active_tasks(board_id)
        closed_tasks = self.list_closed_tasks(board_id)
        users = self.list_users(board_id)
        
        print(f"\n{'='*60}")
        print(f"Board: {board_info.get('name', 'Unknown')}")
        print(f"Description: {board_info.get('description', 'No description')}")
        print(f"{'='*60}")
        print(f"Total Users: {len(users)}")
        print(f"Total Tasks: {len(all_tasks)}")
        print(f"Active Tasks: {len(active_tasks)}")
        print(f"Closed Tasks: {len(closed_tasks)}")
        print(f"{'='*60}\n")
