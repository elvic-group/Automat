# Automat Quick Start Guide

Get started with Automat in 5 minutes!

## Installation

```bash
git clone https://github.com/elvic-group/Automat.git
cd Automat
```

## Run Your First Agent

```bash
python automat.py
```

## Try the Demo

```bash
python demo.py
```

## Run Examples

```bash
python examples.py
```

## Create Your Own Agent

Create a file `my_agent.py`:

```python
from automat import Agent

# Define your tasks
def morning_task():
    print("Good morning! Starting daily tasks...")

def hourly_check():
    print("Performing hourly system check...")

# Create and configure agent
agent = Agent("MyAgent")
agent.add_task("morning", morning_task)
agent.add_task("hourly", hourly_check, interval=3600)

# Run once or continuously
agent.run_once()  # Run all tasks once
# agent.run()     # Run continuously (Ctrl+C to stop)
```

Run it:

```bash
python my_agent.py
```

## Test the Agent

```bash
python -m unittest test_automat.py -v
```

## Common Use Cases

### 1. System Monitoring

```python
from automat import Agent
from examples import health_check, check_disk_space

agent = Agent("Monitor")
agent.add_task("health", health_check, interval=300)  # Every 5 min
agent.add_task("disk", check_disk_space, interval=600)  # Every 10 min
agent.run()
```

### 2. Scheduled Maintenance

```python
from automat import Agent
from examples import cleanup_temp_files, backup_files

agent = Agent("Maintenance")
agent.add_task("cleanup", cleanup_temp_files, interval=3600)  # Hourly
agent.add_task("backup", backup_files, interval=86400)  # Daily
agent.run()
```

### 3. One-Time Workflow

```python
from automat import Agent

def task1():
    print("Step 1: Initialize")

def task2():
    print("Step 2: Process")

def task3():
    print("Step 3: Finalize")

agent = Agent("Workflow")
agent.add_task("init", task1)
agent.add_task("process", task2)
agent.add_task("finalize", task3)

results = agent.run_once()
```

## Configuration

Edit `config.json`:

```json
{
  "agent_name": "MyAgent",
  "log_level": "INFO",
  "default_interval": 60
}
```

Load it:

```python
agent = Agent("MyAgent", config_file="config.json")
```

## Next Steps

- Read the full [README.md](README.md) for detailed API reference
- Check [examples.py](examples.py) for more task examples
- Review [test_automat.py](test_automat.py) to understand testing
- Run [demo.py](demo.py) for an advanced workflow demonstration

## Getting Help

- Check task status: `agent.get_task_status()`
- View logs: Set `log_level` to "DEBUG" in config
- Run tests: `python -m unittest test_automat.py -v`

Happy automating! 🤖
