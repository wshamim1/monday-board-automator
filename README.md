# Monday Board Automator

A Python client for automating Monday.com board operations with easy-to-use **modular clients** for common tasks.

## 🎯 Features

✅ **List all tasks** - Get complete task inventory from any board  
✅ **List all users** - See team members with board access  
✅ **Tasks per user** - Find what each team member is working on  
✅ **Current month tasks** - Focus on recent work  
✅ **Closed/archived tasks** - Track completions  
✅ **Active tasks** - Monitor open work  
✅ **Filter by status** - Organize by workflow stage (Done, In Progress, etc.)  
✅ **Overdue & upcoming** - Never miss deadlines  
✅ **Board analytics** - Track metrics and statistics  

## 📁 Project Structure

```
clients/                    # Individual client modules
├── task_lister.py         # List all tasks
├── user_lister.py         # List all users
├── user_tasks.py          # Tasks per user
├── current_month_tasks.py # Current month filtering
├── closed_tasks.py        # Archived tasks & active tasks
├── status_tasks.py        # Filter by status
├── overdue_tasks.py       # Deadline tracking
└── board_info.py          # Board statistics

examples/                   # Working example scripts
├── user_list_example.py   # Simple user list (recommended start)
├── active_tasks_example.py # Simple active tasks list
├── basic_usage.py         # All clients in action
├── daily_standup.py       # Daily report generator
└── resource_planning.py   # Team workload analysis

docs/                       # Documentation
README.md                   # This file
BLOG_ARTICLE.md            # Comprehensive guide
PROJECT_STRUCTURE.md       # Project layout details
```


## ⚡ Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/monday-board-automator.git
cd monday-board-automator
```

2. Create and activate virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
# The .env file is already created - just edit it with your credentials
# Add your Monday.com API token and Board ID
```

## 🔧 Setup

### 1. Get Your API Token

#### **Step-by-Step Guide:**

1. **Go to Monday.com Apps Management**
   - Visit https://monday.com/apps/manage
   - Or navigate: Account Settings → Apps → My Apps

2. **Create a New App (if needed)**
   - Click "Create App" button
   - Enter app name (e.g., "Board Automator")
   - Click "Create"
   - Select your workspace and board (optional)

3. **Generate API Token**
   - In your app settings, find the "API Token" section
   - You'll see a token starting with `eyJ0eXAi...`
   - If no token exists, click "Generate" or "Create Token"
   - The token is usually 200+ characters long

4. **Copy Your Token**
   - Click the copy icon next to your token
   - Store it securely (never commit to git!)
   - This is what you'll use as `MONDAY_API_TOKEN`

#### **Security Best Practices:**
- ⚠️ Never hardcode your token in source files
- ✅ Use `.env` file (already in `.gitignore`)
- ✅ Use environment variables in production
- 🔄 Rotate tokens periodically
- 🔒 Use tokens with minimal required permissions

#### **Example:**
```
MONDAY_API_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJkYXRhIjp7InVzZXJfaWQiOjEyMzQ1Njc4OX0sImlhdCI6MTY0NTAw...
```

### 2. Find Your Board ID

#### **Step-by-Step Guide:**

1. **Open Your Board**
   - Go to Monday.com and open any board you want to automate
   - Navigate to your workspace

2. **Check the URL**
   - Look at the browser address bar
   - The URL format is: `https://monday.com/boards/XXXXXXXXX/...`
   - The number is your **Board ID**

3. **Copy the Board ID**
   - For example: `https://monday.com/boards/1234567890/`
   - Your Board ID is: `1234567890`

4. **Get Multiple Board IDs (optional)**
   - You can automate multiple boards
   - Simply repeat this process for each board
   - Store them in your `.env` file

#### **Example URLs:**
```
https://monday.com/boards/1234567890/              → ID: 1234567890
https://monday.com/boards/9876543210/pulse         → ID: 9876543210
https://monday.com/boards/5555555555/views/table   → ID: 5555555555
```

### 3. Configure Environment

The `.env` file is already created in the project root. Edit it with your credentials:

```bash
# Open .env file and update these values:
MONDAY_API_TOKEN=your_actual_api_token_here
MONDAY_BOARD_ID=your_actual_board_id_here
```

**Example `.env` file:**
```
MONDAY_API_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
MONDAY_BOARD_ID=1234567890
```

### 4. Verify Your Credentials

Test the connection to ensure everything works:

```python
from clients import BoardInfoFinder
import os
from dotenv import load_dotenv

load_dotenv()

api_token = os.getenv("MONDAY_API_TOKEN")
board_id = int(os.getenv("MONDAY_BOARD_ID"))

try:
    finder = BoardInfoFinder(api_token)
    info = finder.get_board_info(board_id)
    
    if info:
        print(f"✅ Success! Board: {info.get('name')}")
        print(f"   State: {info.get('state')}")
        print(f"   Owner: {info.get('owner', {}).get('name')}")
    else:
        print("❌ No board found. Check your Board ID.")
except Exception as e:
    print(f"❌ Error: {str(e)}")
    print("   Check your API token and permissions.")
```

Run this script to verify:
```bash
python test_connection.py
```

✅ If you see board information, you're all set!  
❌ If you get an error, double-check your API token and Board ID.

## 🚀 Quick Start

### Run Simple Examples (Recommended)

Start with these simple, focused examples:

```bash
# List all users (owners and subscribers)
python examples/user_list_example.py

# List all active tasks
python examples/active_tasks_example.py
```

### Run Complete Examples

```bash
# Comprehensive example with all features
python examples/basic_usage.py

# Daily standup report
python examples/daily_standup.py
```

### Using Individual Clients in Your Code

All examples automatically load credentials from `.env` file:

```python
import os
from dotenv import load_dotenv
from clients import TaskLister, UserLister, BoardInfoFinder

# Load environment variables
load_dotenv()
api_token = os.getenv("MONDAY_API_TOKEN")
board_id = int(os.getenv("MONDAY_BOARD_ID"))

# List all tasks
task_lister = TaskLister(api_token)
tasks = task_lister.list_all_tasks(board_id)
task_lister.print_tasks(board_id)

# List all users
user_lister = UserLister(api_token)
users = user_lister.list_users(board_id)
user_lister.print_users(board_id)

# Get board statistics
board_finder = BoardInfoFinder(api_token)
board_finder.print_board_statistics(board_id)
```

## 📚 Client Reference

### TaskLister
List and analyze all tasks on a board.
```python
from clients import TaskLister

lister = TaskLister(api_token)
tasks = lister.list_all_tasks(board_id, limit=100)
lister.print_tasks(board_id)
```

### UserLister
Get users with board access.
```python
from clients import UserLister

lister = UserLister(api_token)
users = lister.list_users(board_id)
user = lister.get_user_by_email(board_id, "user@example.com")
lister.print_users(board_id)
```

### UserTasksFinder
Find tasks assigned to specific users.
```python
from clients import UserTasksFinder

finder = UserTasksFinder(api_token)
user_tasks = finder.list_tasks_per_user(board_id, user_id)
finder.print_tasks_per_user_summary(board_id)
```

### CurrentMonthTasksFinder
Get tasks from any month.
```python
from clients import CurrentMonthTasksFinder

finder = CurrentMonthTasksFinder(api_token)
current_month = finder.list_tasks_for_current_month(board_id)
march_tasks = finder.get_tasks_by_month(board_id, 2026, 3)
finder.print_current_month_tasks(board_id)
```

### ClosedTasksFinder
Track archived and active tasks.
```python
from clients import ClosedTasksFinder

finder = ClosedTasksFinder(api_token)
closed = finder.list_closed_tasks(board_id)
active = finder.list_active_tasks(board_id)
finder.print_task_summary(board_id)
```

### StatusTasksFinder
Filter tasks by workflow status.
```python
from clients import StatusTasksFinder

finder = StatusTasksFinder(api_token)
done_tasks = finder.list_tasks_by_status(board_id, "Done")
statuses = finder.get_all_statuses(board_id)
finder.print_status_summary(board_id)
```

### OverdueTasksFinder
Monitor deadlines and upcoming tasks.
```python
from clients import OverdueTasksFinder

finder = OverdueTasksFinder(api_token)
overdue = finder.list_overdue_tasks(board_id)
upcoming_7_days = finder.list_upcoming_tasks(board_id, days=7)
finder.print_overdue_tasks(board_id)
finder.print_upcoming_tasks(board_id, days=14)
```

### BoardInfoFinder
Get board information and statistics.
```python
from clients import BoardInfoFinder

finder = BoardInfoFinder(api_token)
info = finder.get_board_info(board_id)
stats = finder.get_board_statistics(board_id)
finder.print_board_info(board_id)
finder.print_board_statistics(board_id)
finder.compare_boards([board_id_1, board_id_2])
```

## 🔌 API Reference

This client uses Monday.com GraphQL API v2.

- **API Endpoint**: `https://api.monday.com/v2`
- **Documentation**: https://developer.monday.com/api-reference/docs

## ⚠️ Error Handling

All clients include error handling. Check for empty results:

```python
from clients import TaskLister

lister = TaskLister(api_token)
tasks = lister.list_all_tasks(board_id)

if tasks:
    print(f"Found {len(tasks)} tasks")
else:
    print("No tasks found or API error occurred")
```

## 📋 Requirements

- Python 3.7+
- requests (>=2.28.0)
- python-dateutil (>=2.8.2)
- python-dotenv (>=1.0.0)

## 🛠️ Advanced Usage

### Environment Variables (Already Configured)

All example scripts automatically load from `.env` file. No code changes needed!

```python
# This is already done in all examples:
from dotenv import load_dotenv
import os

load_dotenv()
api_token = os.getenv("MONDAY_API_TOKEN")
board_id = int(os.getenv("MONDAY_BOARD_ID"))
```

### Scheduling Reports

Use cron or task scheduler to run reports automatically:

```bash
# Daily standup at 9 AM
0 9 * * * /usr/bin/python3 /path/to/examples/daily_standup.py

# Weekly report Friday at 5 PM
0 17 * * 5 /usr/bin/python3 /path/to/examples/resource_planning.py
```

### Rate Limiting

Monday.com has API rate limits. Add delays between operations:

```python
import time
from clients import TaskLister

lister = TaskLister(api_token)
board_ids = [123456789, 987654321, 555666777]

for board_id in board_ids:
    tasks = lister.list_all_tasks(board_id)
    print(f"Board {board_id}: {len(tasks)} tasks")
    time.sleep(1)  # Wait 1 second between requests
```

## 🔍 Troubleshooting

### "GraphQL Error" messages
- Verify your API token is correct and active
- Check that your board ID is valid
- Ensure your token has proper Monday.com permissions
- Try testing on the [Monday.com API Playground](https://developer.monday.com/apps)

### No tasks/users returned
- Confirm the board exists and has content
- Verify board ID in the URL
- Check API token has permission to access the board
- Try using `list_all_tasks()` to see if any data is accessible

### Import errors
- Ensure you're in the project root directory
- Check that the virtual environment is activated
- Verify all dependencies are installed: `pip install -r requirements.txt`

### Rate Limiting
If you get rate limit errors:
- Add delays between API calls (at least 1 second)
- Cache results when possible
- Consider batching operations

## 📖 Documentation

- **README.md** - This file (setup and quick reference)
- **BLOG_ARTICLE.md** - Comprehensive guide with tutorials and real-world examples
- **PROJECT_STRUCTURE.md** - Detailed project layout and organization
- **Client docstrings** - Each client module has detailed docstrings

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your improvements
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details
