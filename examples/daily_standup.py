"""
Daily Standup Report Example
Generate a daily standup report with team's tasks and overdue items
"""

import sys
import os
from datetime import datetime
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clients import (
    UserTasksFinder, OverdueTasksFinder,
    ClosedTasksFinder, BoardInfoFinder
)

def generate_standup_report(api_token: str, board_id: int):
    """Generate and print daily standup report"""
    
    print("\n" + "="*70)
    print(f"📊 DAILY STANDUP REPORT - {datetime.now().strftime('%A, %B %d, %Y')}")
    print("="*70)
    
    # Get overdue tasks
    print("\n⚠️  OVERDUE ITEMS:")
    print("-" * 70)
    overdue_finder = OverdueTasksFinder(api_token)
    overdue = overdue_finder.list_overdue_tasks(board_id)
    if overdue:
        for task in overdue[:5]:
            print(f"  • {task.get('name')} (ID: {task.get('id')})")
        if len(overdue) > 5:
            print(f"  ... and {len(overdue) - 5} more overdue tasks")
    else:
        print("  ✓ No overdue tasks!")
    
    # Get team workload
    print("\n👥 TEAM WORKLOAD:")
    print("-" * 70)
    tasks_finder = UserTasksFinder(api_token)
    workload = tasks_finder.count_tasks_per_user(board_id)
    
    for user, count in sorted(workload.items(), key=lambda x: x[1], reverse=True):
        if count > 15:
            status = "🔴 OVERLOADED"
        elif count > 10:
            status = "🟡 MODERATE"
        else:
            status = "🟢 AVAILABLE"
        print(f"  {user:<30} {count:>3} tasks {status}")
    
    # Get upcoming deadlines
    print("\n📅 UPCOMING DEADLINES (Next 7 Days):")
    print("-" * 70)
    upcoming = overdue_finder.list_upcoming_tasks(board_id, days=7)
    if upcoming:
        for task in upcoming[:5]:
            print(f"  • {task.get('name')}")
        if len(upcoming) > 5:
            print(f"  ... and {len(upcoming) - 5} more tasks")
    else:
        print("  ✓ No upcoming deadlines this week!")
    
    # Board summary
    print("\n📈 BOARD SUMMARY:")
    print("-" * 70)
    board_finder = BoardInfoFinder(api_token)
    stats = board_finder.get_board_statistics(board_id)
    print(f"  Total Items:     {stats.get('total_items', 0)}")
    print(f"  Active:          {stats.get('active_items', 0)}")
    print(f"  Completed:       {stats.get('archived_items', 0)}")
    print(f"  Completion Rate: {stats.get('completion_rate', 0):.1f}%")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API token and board ID from environment variables
    api_token = os.getenv("MONDAY_API_TOKEN")
    board_id_str = os.getenv("MONDAY_BOARD_ID")
    
    # Validate credentials
    if not api_token or api_token == "your_api_token_here":
        print("❌ Error: Please set MONDAY_API_TOKEN in your .env file")
        exit(1)
    
    if not board_id_str:
        print("❌ Error: Please set MONDAY_BOARD_ID in your .env file")
        exit(1)
    
    try:
        board_id = int(board_id_str)
    except ValueError:
        print("❌ Error: MONDAY_BOARD_ID must be a valid number")
        exit(1)
    
    generate_standup_report(api_token, board_id)
