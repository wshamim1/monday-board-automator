"""
Daily Standup Report Example
Generate a daily standup report with team's tasks and overdue items
"""

import sys
import os
from datetime import datetime

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
    api_token = "YOUR_API_TOKEN"
    board_id = 123456789
    
    generate_standup_report(api_token, board_id)
