# Project Structure

```
monday-board-automator/
├── clients/                           # All individual client modules
│   ├── __init__.py                   # Package initialization
│   ├── task_lister.py               # List all tasks from a board
│   ├── user_lister.py               # List all users on a board
│   ├── user_tasks.py                # Find tasks assigned to specific users
│   ├── current_month_tasks.py       # Get tasks from current month
│   ├── closed_tasks.py              # Find closed/archived tasks
│   ├── status_tasks.py              # Filter tasks by status
│   ├── overdue_tasks.py             # Find overdue and upcoming tasks
│   └── board_info.py                # Get board information & statistics
│
├── examples/                         # Example scripts showing how to use clients
│   ├── basic_usage.py               # Basic example covering all clients
│   ├── daily_standup.py             # Daily standup report generator
│   └── resource_planning.py         # Resource allocation analysis
│
├── docs/                            # Documentation and articles
│   ├── README.md                    # Main documentation
│   └── BLOG_ARTICLE.md             # Comprehensive blog post
│
├── monday_client.py                 # (Root) Main client with all functionality
├── requirements.txt                 # Python dependencies
├── .env                            # Environment variables (configured locally)
├── .gitignore                      # Git ignore rules
└── .git/                           # Git repository
```

## Quick Navigation

### 📚 Using Individual Clients
Each client in `clients/` is independent and can be used separately:

```python
from clients import TaskLister, UserLister, BoardInfoFinder

# Use individual clients
lister = TaskLister(api_token)
users = UserLister(api_token)
board = BoardInfoFinder(api_token)
```

### 🚀 Running Examples
Examples in `examples/` demonstrate real-world usage:

```bash
python examples/basic_usage.py
python examples/daily_standup.py
python examples/resource_planning.py
```

### 📖 Reading Documentation
- `docs/README.md` - Setup and API reference
- `docs/BLOG_ARTICLE.md` - Comprehensive guide with tutorials
- Each client file has docstrings explaining its methods

## File Organization Benefits

✅ **Better Visibility** - Organized by category
✅ **Modular Design** - Import only what you need
✅ **Scalability** - Easy to add new clients
✅ **Maintainability** - Separate concerns clearly
✅ **Examples** - Learn from working code
✅ **Documentation** - Centralized in docs/

## Clean Import Syntax

### Before (Root-level files)
```python
from task_lister import TaskLister
from user_lister import UserLister
```

### After (Organized)
```python
from clients import TaskLister, UserLister
```

Much cleaner! 🎉
