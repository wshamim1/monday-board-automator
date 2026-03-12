"""
List closed/archived tasks from a Monday.com board
"""

import requests
from typing import List, Dict, Any


class ClosedTasksFinder:
    """Client for finding closed/archived tasks"""
    
    def __init__(self, api_token: str):
        """Initialize ClosedTasksFinder"""
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
        """List all closed/archived tasks"""
        query = """query { boards(ids: [%s]) { items_page(limit: 500) { items { id name created_at updated_at state column_values { id text type } } } } }""" % board_id
        try:
            result = self._make_request(query)
            items_page = result.get("boards", [{}])[0].get("items_page", {})
            all_tasks = items_page.get("items", [])
            return [task for task in all_tasks if task.get("state") == "archived"]
        except Exception as e:
            print(f"Error listing closed tasks: {str(e)}")
            return []
    
    def list_active_tasks(self, board_id: int) -> List[Dict[str, Any]]:
        """List all active/open tasks"""
        query = """query { boards(ids: [%s]) { items_page(limit: 500) { items { id name created_at updated_at state column_values { id text type } } } } }""" % board_id
        try:
            result = self._make_request(query)
            items_page = result.get("boards", [{}])[0].get("items_page", {})
            all_tasks = items_page.get("items", [])
            return [task for task in all_tasks if task.get("state") != "archived"]
        except Exception as e:
            print(f"Error listing active tasks: {str(e)}")
            return []
    
    def print_closed_tasks(self, board_id: int) -> None:
        """Print all closed tasks"""
        closed = self.list_closed_tasks(board_id)
        print(f"\n{'='*80}")
        print(f"Closed/Archived Tasks: {len(closed)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Updated':<15}")
        print(f"{'-'*80}")
        for task in closed:
            print(f"{task.get('id', 'N/A'):<15} {task.get('name', 'N/A')[:37]:<40} {task.get('state', 'N/A'):<10} {task.get('updated_at', 'N/A')[:10]:<15}")
    
    def print_active_tasks(self, board_id: int) -> None:
        """Print all active tasks"""
        active = self.list_active_tasks(board_id)
        print(f"\n{'='*80}")
        print(f"Active Tasks: {len(active)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        for task in active:
            print(f"{task.get('id', 'N/A'):<15} {task.get('name', 'N/A')[:37]:<40} {task.get('state', 'N/A'):<10} {task.get('created_at', 'N/A')[:10]:<15}")
    
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
