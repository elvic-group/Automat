# Automat

An intelligent automation agent system for executing scheduled tasks and workflows.

## Overview

Automat is a flexible Python-based automation framework that allows you to create, schedule, and manage automated tasks. It provides a simple yet powerful API for building custom automation workflows.

## Features

- **Task Scheduling**: Run tasks once or on recurring intervals
- **Status Tracking**: Monitor task execution and performance
- **Error Handling**: Robust error handling with detailed logging
- **Configuration**: JSON-based configuration for easy customization
- **Extensible**: Simple API for adding custom tasks
- **Lightweight**: Minimal dependencies, pure Python implementation

## Installation

Clone the repository:

```bash
git clone https://github.com/elvic-group/Automat.git
cd Automat
```

## Quick Start

### Basic Usage

```python
from automat import Agent

# Create an agent
agent = Agent("MyAgent")

# Define a task
def my_task():
    print("Task executed!")

# Add task to agent
agent.add_task("my_task", my_task)

# Run all tasks once
results = agent.run_once()
```

### Recurring Tasks

```python
from automat import Agent

agent = Agent("MyAgent")

# Task that runs every 60 seconds
def periodic_task():
    print("Running periodic check...")

agent.add_task("periodic", periodic_task, interval=60)

# Run agent continuously
agent.run()
```

### Using Configuration File

```python
from automat import Agent

agent = Agent("MyAgent", config_file="config.json")
agent.add_task("task1", my_function)
agent.run_once()
```

## Examples

See `examples.py` for common automation tasks:

```bash
python examples.py
```

Example tasks include:
- System health checks
- Disk space monitoring
- File backups
- Status reports
- Notifications

## Running the Agent

Execute the main agent:

```bash
python automat.py
```

Or use it as a module:

```python
from automat import Agent
from examples import health_check, check_disk_space

agent = Agent("Automat")
agent.add_task("health", health_check, interval=300)
agent.add_task("disk", check_disk_space, interval=600)
agent.run()
```

## Configuration

The `config.json` file allows you to customize the agent:

```json
{
  "agent_name": "Automat",
  "log_level": "INFO",
  "default_interval": 60,
  "max_concurrent_tasks": 5
}
```

## Testing

Run the test suite:

```bash
python -m unittest test_automat.py
```

Or run tests with verbose output:

```bash
python -m unittest test_automat.py -v
```

## API Reference

### Agent Class

**`Agent(name, config_file=None)`**
- Create a new automation agent
- `name`: Agent name
- `config_file`: Optional path to configuration file

**`add_task(name, action, interval=0, enabled=True)`**
- Add a task to the agent
- `name`: Unique task identifier
- `action`: Callable function to execute
- `interval`: Execution interval in seconds (0 = run once)
- `enabled`: Whether task is enabled
- Returns: Agent instance (for chaining)

**`remove_task(name)`**
- Remove a task by name
- Returns: Boolean indicating success

**`run_once()`**
- Execute all enabled tasks once
- Returns: List of execution results

**`run(max_iterations=None)`**
- Run agent continuously
- `max_iterations`: Optional limit on iterations

**`stop()`**
- Stop the running agent

**`get_task_status()`**
- Get status of all tasks
- Returns: List of task status dictionaries

### Task Class

**`Task(name, action, interval=0, enabled=True)`**
- Create a new task
- Automatically managed by Agent, typically not instantiated directly

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is open source and available under the MIT License.
