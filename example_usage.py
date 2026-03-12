"""
Example usage of the Monday.com Board Automator Client

Replace YOUR_API_TOKEN and BOARD_ID with your actual Monday.com API token and board ID
"""

from monday_client import MondayClient
import json


def main():
    # Initialize the client with your API token
    # Get your token from: https://monday.com/apps/manage
    api_token = "YOUR_API_TOKEN"
    client = MondayClient(api_token)
    
    # Your board ID
    board_id = 123456789  # Replace with your actual board ID
    
    print("\n" + "="*70)
    print("MONDAY BOARD AUTOMATOR - EXAMPLE USAGE")
    print("="*70)
    
    # 1. Get board information
    print("\n[1] Getting Board Information...")
    board_info = client.get_board_info(board_id)
    if board_info:
        print(f"Board Name: {board_info.get('name')}")
        print(f"Board State: {board_info.get('state')}")
        print(f"Users Count: {board_info.get('users_count')}")
    
    # 2. List all tasks
    print("\n[2] Listing All Tasks...")
    all_tasks = client.list_all_tasks(board_id)
    print(f"Total tasks: {len(all_tasks)}")
    if all_tasks:
        for task in all_tasks[:5]:  # Show first 5
            print(f"  - {task.get('name')} (ID: {task.get('id')})")
        if len(all_tasks) > 5:
            print(f"  ... and {len(all_tasks) - 5} more")
    
    # 3. List all users
    print("\n[3] Listing All Users...")
    users = client.list_users(board_id)
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"  - {user.get('name')} ({user.get('email')})")
    
    # 4. List active tasks
    print("\n[4] Listing Active Tasks...")
    active_tasks = client.list_active_tasks(board_id)
    print(f"Active tasks: {len(active_tasks)}")
    
    # 5. List closed/archived tasks
    print("\n[5] Listing Closed Tasks...")
    closed_tasks = client.list_closed_tasks(board_id)
    print(f"Closed tasks: {len(closed_tasks)}")
    
    # 6. List tasks for current month
    print("\n[6] Listing Tasks from Current Month...")
    current_month_tasks = client.list_tasks_for_current_month(board_id)
    print(f"Tasks this month: {len(current_month_tasks)}")
    if current_month_tasks:
        for task in current_month_tasks[:3]:
            print(f"  - {task.get('name')}")
    
    # 7. List tasks per user (example with first user)
    if users:
        user_id = users[0].get('id')
        print(f"\n[7] Listing Tasks for User: {users[0].get('name')}...")
        user_tasks = client.list_tasks_per_user(board_id, int(user_id))
        print(f"Tasks assigned to {users[0].get('name')}: {len(user_tasks)}")
    
    # 8. Get a specific task (if tasks exist)
    if all_tasks:
        print(f"\n[8] Getting Specific Task Details...")
        task_id = all_tasks[0].get('id')
        task_detail = client.get_task_by_id(int(task_id))
        print(f"Task: {task_detail.get('name')}")
        print(f"State: {task_detail.get('state')}")
        print(f"Created: {task_detail.get('created_at')}")
    
    # 9. List tasks by status (example)
    print(f"\n[9] Listing Tasks by Status...")
    done_tasks = client.list_tasks_by_status(board_id, "Done")
    in_progress = client.list_tasks_by_status(board_id, "In Progress")
    todo_tasks = client.list_tasks_by_status(board_id, "Todo")
    print(f"Done: {len(done_tasks)}, In Progress: {len(in_progress)}, Todo: {len(todo_tasks)}")
    
    # 10. List overdue tasks
    print(f"\n[10] Listing Overdue Tasks...")
    overdue = client.list_overdue_tasks(board_id)
    print(f"Overdue tasks: {len(overdue)}")
    if overdue:
        for task in overdue[:3]:
            print(f"  - {task.get('name')}")
    
    # 11. Print summary
    print("\n[11] Board Summary:")
    client.print_tasks_summary(board_id)


if __name__ == "__main__":
    main()
