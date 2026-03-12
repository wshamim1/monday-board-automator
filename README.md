# Monday Board Automator

A Python client for automating Monday.com board operations with easy-to-use methods for common tasks.

## Features

- **List all tasks** from a board
- **List all users** with board access
- **List tasks per user** (assigned to specific user)
- **List tasks for current month**
- **List closed/archived tasks**
- **List active tasks**
- **Get task details** by ID
- **List tasks by status** (Done, In Progress, Todo, etc.)
- **Find overdue tasks** (tasks with due dates in the past)
- **Get board information**

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/monday-board-automator.git
cd monday-board-automator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup

### 1. Get Your API Token

1. Visit [Monday.com Apps](https://monday.com/apps/manage)
2. Create a new app or use an existing one
3. Copy your API token

### 2. Find Your Board ID

1. Open your board in Monday.com
2. The board ID is in the URL: `https://monday.com/boards/123456789/...`
3. In this example, `123456789` is your board ID

## Usage

### Basic Example

```python
from monday_client import MondayClient

# Initialize client
client = MondayClient(api_token="your_api_token_here")

# Your board ID
board_id = 123456789

# List all tasks
tasks = client.list_all_tasks(board_id)
for task in tasks:
    print(f"Task: {task['name']}")

# List all users
users = client.list_users(board_id)
for user in users:
    print(f"User: {user['name']} ({user['email']})")

# List active tasks
active = client.list_active_tasks(board_id)
print(f"Active tasks: {len(active)}")

# List closed tasks
closed = client.list_closed_tasks(board_id)
print(f"Closed tasks: {len(closed)}")

# List tasks from current month
current_month = client.list_tasks_for_current_month(board_id)
print(f"Tasks this month: {len(current_month)}")

# Get board summary
client.print_tasks_summary(board_id)
```

## Available Methods

### `list_all_tasks(board_id, limit=100)`
Returns all tasks from the specified board.

### `list_users(board_id)`
Returns all users with access to the board.

### `list_tasks_per_user(board_id, user_id)`
Returns tasks assigned to a specific user.

### `list_tasks_for_current_month(board_id)`
Returns tasks created in the current month.

### `list_closed_tasks(board_id)`
Returns archived/closed tasks.

### `list_active_tasks(board_id)`
Returns open/active tasks.

### `get_task_by_id(task_id)`
Returns detailed information about a specific task.

### `list_tasks_by_status(board_id, status)`
Returns tasks with a specific status (e.g., "Done", "In Progress").

### `list_overdue_tasks(board_id)`
Returns tasks with due dates that have passed.

### `get_board_info(board_id)`
Returns board information and metadata.

### `print_tasks_summary(board_id)`
Prints a summary of board statistics.

## Example Script

See `example_usage.py` for a complete working example with all methods demonstrated.

```bash
# Run the example (after updating your API token and board ID)
python example_usage.py
```

## API Reference

This client uses Monday.com GraphQL API v2.

- API Endpoint: `https://api.monday.com/v2`
- Documentation: https://developer.monday.com/api-reference/docs

## Error Handling

The client includes basic error handling. Check for empty results:

```python
tasks = client.list_all_tasks(board_id)
if tasks:
    # Process tasks
else:
    print("No tasks found or API error occurred")
```

## Requirements

- Python 3.7+
- requests library
- python-dateutil library

## Troubleshooting

### "GraphQL Error" messages

- Verify your API token is correct
- Check that your board ID is valid
- Ensure your token has proper permissions

### No tasks/users returned

- Confirm the board exists and has content
- Check API token permissions
- Verify board ID is correct

### Rate Limiting

Monday.com has rate limits on their API. For large-scale operations, add delays between requests:

```python
import time

for board_id in board_ids:
    client.list_all_tasks(board_id)
    time.sleep(1)  # Wait 1 second between requests
```

## Contributing

Feel free to open issues and pull requests for improvements!

## License

MIT License - see LICENSE file for details
