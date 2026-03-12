"""
Simple Active Tasks List Example
List all active (non-archived) tasks from a Monday.com board
"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients import ClosedTasksFinder

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API token and board ID from environment variables
    api_token = os.getenv("MONDAY_API_TOKEN")
    board_id_str = os.getenv("MONDAY_BOARD_ID")
    
    # Validate credentials
    if not api_token or api_token == "your_api_token_here":
        print("❌ Error: Please set MONDAY_API_TOKEN in your .env file")
        return
    
    if not board_id_str:
        print("❌ Error: Please set MONDAY_BOARD_ID in your .env file")
        return
    
    try:
        board_id = int(board_id_str)
    except ValueError:
        print("❌ Error: MONDAY_BOARD_ID must be a valid number")
        return
    
    print("\n" + "="*80)
    print("ACTIVE TASKS LIST")
    print("="*80)
    
    # Create task finder instance
    task_finder = ClosedTasksFinder(api_token)
    
    # Get all active tasks
    active_tasks = task_finder.list_active_tasks(board_id)
    
    if active_tasks:
        print(f"\nTotal Active Tasks: {len(active_tasks)}")
        print("-" * 80)
        print(f"{'ID':<15} {'Task Name':<45} {'State':<10} {'Created':<15}")
        print("-" * 80)
        
        for task in active_tasks:
            task_id = task.get('id', 'N/A')
            name = task.get('name', 'N/A')[:42]
            state = task.get('state', 'N/A')
            created = task.get('created_at', 'N/A')[:10]
            
            print(f"{task_id:<15} {name:<45} {state:<10} {created:<15}")
        
        print("="*80)
        
        # Show summary
        print(f"\n📊 Summary:")
        print(f"   Active Tasks: {len(active_tasks)}")
        
        # Get closed tasks for comparison
        closed_tasks = task_finder.list_closed_tasks(board_id)
        total_tasks = len(active_tasks) + len(closed_tasks)
        
        if total_tasks > 0:
            completion_rate = (len(closed_tasks) / total_tasks) * 100
            print(f"   Closed Tasks: {len(closed_tasks)}")
            print(f"   Total Tasks: {total_tasks}")
            print(f"   Completion Rate: {completion_rate:.1f}%")
    else:
        print("\n✅ No active tasks found (all tasks are completed!)")
    
    print()

if __name__ == "__main__":
    main()

# Made with Bob
