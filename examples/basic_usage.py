"""
Monday.com Board Automator - Example Usage Scripts
"""

import sys
import os
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients import (
    TaskLister, UserLister, UserTasksFinder,
    CurrentMonthTasksFinder, ClosedTasksFinder,
    StatusTasksFinder, OverdueTasksFinder, BoardInfoFinder
)

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
    
    print("\n" + "="*70)
    print("MONDAY BOARD AUTOMATOR - EXAMPLE USAGE")
    print("="*70)
    
    # 1. Get board information
    print("\n[1] Getting Board Information...")
    board_finder = BoardInfoFinder(api_token)
    board_info = board_finder.get_board_info(board_id)
    if board_info:
        print(f"Board Name: {board_info.get('name')}")
        print(f"Board State: {board_info.get('state')}")
    
    # 2. List all tasks
    print("\n[2] Listing All Tasks...")
    task_lister = TaskLister(api_token)
    all_tasks = task_lister.list_all_tasks(board_id)
    print(f"Total tasks: {len(all_tasks)}")
    
    # 3. List all users
    print("\n[3] Listing All Users...")
    user_lister = UserLister(api_token)
    users = user_lister.list_users(board_id)
    print(f"Total users: {len(users)}")
    
    # 4. List active vs closed tasks
    print("\n[4] Task Status Summary...")
    closed_finder = ClosedTasksFinder(api_token)
    active = closed_finder.list_active_tasks(board_id)
    closed = closed_finder.list_closed_tasks(board_id)
    print(f"Active tasks: {len(active)}, Closed tasks: {len(closed)}")
    
    # 5. List tasks from current month
    print("\n[5] Current Month Tasks...")
    month_finder = CurrentMonthTasksFinder(api_token)
    current_month = month_finder.list_tasks_for_current_month(board_id)
    print(f"Tasks this month: {len(current_month)}")
    
    # 6. Tasks by status summary
    print("\n[6] Task Summary by Status...")
    status_finder = StatusTasksFinder(api_token)
    status_finder.print_status_summary(board_id)
    
    # 7. Overdue tasks
    print("\n[7] Overdue Tasks...")
    overdue_finder = OverdueTasksFinder(api_token)
    overdue = overdue_finder.list_overdue_tasks(board_id)
    print(f"Overdue tasks: {len(overdue)}")
    
    # 8. Board statistics
    print("\n[8] Board Statistics...")
    board_finder.print_board_statistics(board_id)


if __name__ == "__main__":
    main()
