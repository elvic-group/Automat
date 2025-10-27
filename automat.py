#!/usr/bin/env python3
"""
Automat - Automated Agent System
A flexible automation framework for executing scheduled tasks and workflows.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional


class Task:
    """Represents a single automation task."""
    
    def __init__(self, name: str, action: Callable, interval: int = 0, enabled: bool = True):
        """
        Initialize a task.
        
        Args:
            name: Unique task name
            action: Callable function to execute
            interval: Execution interval in seconds (0 = run once)
            enabled: Whether task is enabled
        """
        self.name = name
        self.action = action
        self.interval = interval
        self.enabled = enabled
        self.last_run: Optional[float] = None
        self.run_count = 0
        self.status = "pending"
        
    def should_run(self) -> bool:
        """Check if task should run based on interval."""
        if not self.enabled:
            return False
        if self.last_run is None:
            return True
        if self.interval == 0:
            return False
        return (time.time() - self.last_run) >= self.interval
    
    def execute(self) -> Dict[str, Any]:
        """Execute the task and return result."""
        result = {
            "task": self.name,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "message": None,
            "error": None
        }
        
        try:
            logging.info(f"Executing task: {self.name}")
            self.status = "running"
            self.action()
            self.last_run = time.time()
            self.run_count += 1
            self.status = "completed"
            result["message"] = f"Task completed successfully (run #{self.run_count})"
        except Exception as e:
            self.status = "failed"
            result["status"] = "failed"
            result["error"] = str(e)
            logging.error(f"Task {self.name} failed: {e}")
        
        return result


class Agent:
    """Main automation agent that manages and executes tasks."""
    
    def __init__(self, name: str = "Automat", config_file: Optional[str] = None):
        """
        Initialize the automation agent.
        
        Args:
            name: Agent name
            config_file: Path to configuration file
        """
        self.name = name
        self.tasks: List[Task] = []
        self.running = False
        self.config = self._load_config(config_file) if config_file else {}
        
        # Setup logging
        log_level = self.config.get("log_level", "INFO")
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(self.name)
        
    def _load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file {config_file} not found, using defaults")
            return {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            return {}
    
    def add_task(self, name: str, action: Callable, interval: int = 0, enabled: bool = True) -> 'Agent':
        """
        Add a task to the agent.
        
        Args:
            name: Unique task name
            action: Callable function to execute
            interval: Execution interval in seconds (0 = run once)
            enabled: Whether task is enabled
            
        Returns:
            Self for method chaining
        """
        task = Task(name, action, interval, enabled)
        self.tasks.append(task)
        self.logger.info(f"Added task: {name} (interval: {interval}s)")
        return self
    
    def remove_task(self, name: str) -> bool:
        """Remove a task by name."""
        for i, task in enumerate(self.tasks):
            if task.name == name:
                self.tasks.pop(i)
                self.logger.info(f"Removed task: {name}")
                return True
        return False
    
    def get_task_status(self) -> List[Dict[str, Any]]:
        """Get status of all tasks."""
        return [
            {
                "name": task.name,
                "status": task.status,
                "enabled": task.enabled,
                "interval": task.interval,
                "run_count": task.run_count,
                "last_run": datetime.fromtimestamp(task.last_run).isoformat() if task.last_run else None
            }
            for task in self.tasks
        ]
    
    def run_once(self) -> List[Dict[str, Any]]:
        """Execute all enabled tasks once and return results."""
        self.logger.info(f"Agent {self.name} running tasks once")
        results = []
        
        for task in self.tasks:
            if task.enabled and task.last_run is None:
                result = task.execute()
                results.append(result)
        
        return results
    
    def run(self, max_iterations: Optional[int] = None) -> None:
        """
        Run the agent continuously, executing tasks based on their intervals.
        
        Args:
            max_iterations: Maximum number of iterations (None = infinite)
        """
        self.running = True
        self.logger.info(f"Agent {self.name} started")
        iteration = 0
        
        try:
            while self.running:
                if max_iterations and iteration >= max_iterations:
                    break
                
                for task in self.tasks:
                    if task.should_run():
                        task.execute()
                
                time.sleep(1)
                iteration += 1
                
        except KeyboardInterrupt:
            self.logger.info("Agent interrupted by user")
        finally:
            self.running = False
            self.logger.info(f"Agent {self.name} stopped")
    
    def stop(self) -> None:
        """Stop the agent."""
        self.running = False


def main():
    """Main entry point for the agent."""
    # Example usage
    agent = Agent("Automat")
    
    # Add example tasks
    def hello_task():
        print("Hello from Automat!")
    
    def status_task():
        print(f"Agent status: Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    agent.add_task("hello", hello_task)
    agent.add_task("status", status_task, interval=5)
    
    # Run tasks once
    results = agent.run_once()
    
    # Print results
    print("\n=== Task Execution Results ===")
    for result in results:
        print(f"Task: {result['task']}")
        print(f"Status: {result['status']}")
        print(f"Message: {result['message']}")
        if result['error']:
            print(f"Error: {result['error']}")
        print()
    
    # Print task status
    print("\n=== Task Status ===")
    for status in agent.get_task_status():
        print(f"{status['name']}: {status['status']} (runs: {status['run_count']})")


if __name__ == "__main__":
    main()
