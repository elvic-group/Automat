#!/usr/bin/env python3
"""
Advanced demo of the Automat agent with real-world workflows.
"""

from automat import Agent
from examples import (
    health_check,
    check_disk_space,
    generate_report,
    send_notification,
    cleanup_temp_files
)


def main():
    """Demonstrate a complete automation workflow."""
    print("=" * 60)
    print("Automat Agent - Advanced Demo")
    print("=" * 60)
    print()
    
    # Create agent with configuration
    agent = Agent("AutomatDemo", config_file="config.json")
    
    # Add monitoring tasks
    agent.add_task(
        "health_check",
        health_check,
        interval=0,
        enabled=True
    )
    
    agent.add_task(
        "disk_check",
        check_disk_space,
        interval=0,
        enabled=True
    )
    
    # Add maintenance tasks
    agent.add_task(
        "cleanup",
        cleanup_temp_files,
        interval=0,
        enabled=True
    )
    
    # Add reporting task
    agent.add_task(
        "report",
        generate_report,
        interval=0,
        enabled=True
    )
    
    # Add notification task
    def notify_completion():
        send_notification("Automation workflow completed successfully!")
    
    agent.add_task(
        "notification",
        notify_completion,
        interval=0,
        enabled=True
    )
    
    # Display configuration
    print("Agent Configuration:")
    print(f"  Name: {agent.name}")
    print(f"  Tasks: {len(agent.tasks)}")
    print()
    
    # Display tasks
    print("Registered Tasks:")
    for i, task in enumerate(agent.tasks, 1):
        interval_str = f"{task.interval}s" if task.interval > 0 else "once"
        status_str = "enabled" if task.enabled else "disabled"
        print(f"  {i}. {task.name} - runs {interval_str} ({status_str})")
    print()
    
    # Execute workflow
    print("=" * 60)
    print("Executing Automation Workflow")
    print("=" * 60)
    print()
    
    results = agent.run_once()
    
    # Display results
    print()
    print("=" * 60)
    print("Execution Summary")
    print("=" * 60)
    print()
    
    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = sum(1 for r in results if r["status"] == "failed")
    
    print(f"Total tasks: {len(results)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failed_count}")
    print()
    
    # Show detailed results
    for result in results:
        status_symbol = "✓" if result["status"] == "success" else "✗"
        print(f"{status_symbol} {result['task']}: {result['message'] or result['error']}")
    
    print()
    
    # Display final task status
    print("=" * 60)
    print("Task Status")
    print("=" * 60)
    print()
    
    status = agent.get_task_status()
    for task_status in status:
        print(f"Task: {task_status['name']}")
        print(f"  Status: {task_status['status']}")
        print(f"  Run count: {task_status['run_count']}")
        print(f"  Last run: {task_status['last_run']}")
        print()
    
    print("=" * 60)
    print("Demo Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
