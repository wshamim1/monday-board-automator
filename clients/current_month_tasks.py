"""
List tasks created or updated in the current month
"""

import requests
from datetime import datetime
from typing import List, Dict, Any


class CurrentMonthTasksFinder:
    """Client for finding tasks from the current month"""
    
    def __init__(self, api_token: str):
        """Initialize CurrentMonthTasksFinder"""
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
        """List tasks created in the current month"""
        query = """query { boards(ids: [%s]) { items_page(limit: 500) { items { id name created_at updated_at state column_values { id text type } } } } }""" % board_id
        try:
            result = self._make_request(query)
            items_page = result.get("boards", [{}])[0].get("items_page", {})
            all_tasks = items_page.get("items", [])
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
    
    def get_tasks_by_month(self, board_id: int, year: int, month: int) -> List[Dict[str, Any]]:
        """Get tasks for a specific month"""
        query = """query { boards(ids: [%s]) { items_page(limit: 500) { items { id name created_at updated_at state column_values { id text type } } } } }""" % board_id
        try:
            result = self._make_request(query)
            items_page = result.get("boards", [{}])[0].get("items_page", {})
            all_tasks = items_page.get("items", [])
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
    
    def print_current_month_tasks(self, board_id: int) -> None:
        """Print all tasks from current month"""
        tasks = self.list_tasks_for_current_month(board_id)
        now = datetime.now()
        month_name = now.strftime("%B %Y")
        print(f"\n{'='*80}")
        print(f"Tasks Created in {month_name}: {len(tasks)}")
        print(f"{'='*80}")
        print(f"{'ID':<15} {'Task Name':<40} {'State':<10} {'Created':<15}")
        print(f"{'-'*80}")
        for task in tasks:
            print(f"{task.get('id', 'N/A'):<15} {task.get('name', 'N/A')[:37]:<40} {task.get('state', 'N/A'):<10} {task.get('created_at', 'N/A')[:10]:<15}")
