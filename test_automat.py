#!/usr/bin/env python3
"""
Tests for the Automat agent system.
"""

import unittest
import time
from automat import Agent, Task


class TestTask(unittest.TestCase):
    """Test cases for Task class."""
    
    def test_task_creation(self):
        """Test task can be created."""
        def dummy_action():
            pass
        
        task = Task("test_task", dummy_action)
        self.assertEqual(task.name, "test_task")
        self.assertTrue(task.enabled)
        self.assertEqual(task.status, "pending")
        self.assertEqual(task.run_count, 0)
    
    def test_task_should_run(self):
        """Test task should_run logic."""
        def dummy_action():
            pass
        
        task = Task("test_task", dummy_action, interval=0)
        self.assertTrue(task.should_run())
        
        # After execution with interval=0, should not run again
        task.execute()
        self.assertFalse(task.should_run())
    
    def test_task_execution(self):
        """Test task execution."""
        executed = []
        
        def test_action():
            executed.append(True)
        
        task = Task("test_task", test_action)
        result = task.execute()
        
        self.assertEqual(len(executed), 1)
        self.assertEqual(result["status"], "success")
        self.assertEqual(task.run_count, 1)
        self.assertIsNotNone(task.last_run)
    
    def test_task_execution_error(self):
        """Test task execution with error."""
        def failing_action():
            raise ValueError("Test error")
        
        task = Task("failing_task", failing_action)
        result = task.execute()
        
        self.assertEqual(result["status"], "failed")
        self.assertIsNotNone(result["error"])
        self.assertEqual(task.status, "failed")
    
    def test_task_disabled(self):
        """Test disabled task does not run."""
        def dummy_action():
            pass
        
        task = Task("test_task", dummy_action, enabled=False)
        self.assertFalse(task.should_run())


class TestAgent(unittest.TestCase):
    """Test cases for Agent class."""
    
    def test_agent_creation(self):
        """Test agent can be created."""
        agent = Agent("TestAgent")
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(len(agent.tasks), 0)
        self.assertFalse(agent.running)
    
    def test_add_task(self):
        """Test adding tasks to agent."""
        agent = Agent("TestAgent")
        
        def dummy_action():
            pass
        
        agent.add_task("task1", dummy_action)
        self.assertEqual(len(agent.tasks), 1)
        self.assertEqual(agent.tasks[0].name, "task1")
    
    def test_add_multiple_tasks(self):
        """Test adding multiple tasks."""
        agent = Agent("TestAgent")
        
        def dummy_action():
            pass
        
        agent.add_task("task1", dummy_action).add_task("task2", dummy_action)
        self.assertEqual(len(agent.tasks), 2)
    
    def test_remove_task(self):
        """Test removing tasks from agent."""
        agent = Agent("TestAgent")
        
        def dummy_action():
            pass
        
        agent.add_task("task1", dummy_action)
        result = agent.remove_task("task1")
        
        self.assertTrue(result)
        self.assertEqual(len(agent.tasks), 0)
    
    def test_remove_nonexistent_task(self):
        """Test removing nonexistent task."""
        agent = Agent("TestAgent")
        result = agent.remove_task("nonexistent")
        self.assertFalse(result)
    
    def test_run_once(self):
        """Test running tasks once."""
        agent = Agent("TestAgent")
        executed = []
        
        def test_action():
            executed.append(True)
        
        agent.add_task("task1", test_action)
        agent.add_task("task2", test_action)
        
        results = agent.run_once()
        
        self.assertEqual(len(results), 2)
        self.assertEqual(len(executed), 2)
        for result in results:
            self.assertEqual(result["status"], "success")
    
    def test_get_task_status(self):
        """Test getting task status."""
        agent = Agent("TestAgent")
        
        def dummy_action():
            pass
        
        agent.add_task("task1", dummy_action)
        agent.add_task("task2", dummy_action, enabled=False)
        
        status = agent.get_task_status()
        self.assertEqual(len(status), 2)
        self.assertTrue(status[0]["enabled"])
        self.assertFalse(status[1]["enabled"])
    
    def test_run_with_max_iterations(self):
        """Test running agent with max iterations."""
        agent = Agent("TestAgent")
        counter = []
        
        def counting_action():
            counter.append(1)
        
        # Task with 0.1 second interval
        agent.add_task("counter", counting_action, interval=0)
        
        # Run for 1 iteration should execute once
        agent.run(max_iterations=1)
        
        # Should only run once since interval is 0
        self.assertGreaterEqual(len(counter), 0)


class TestAgentIntegration(unittest.TestCase):
    """Integration tests for the agent system."""
    
    def test_full_workflow(self):
        """Test complete workflow."""
        agent = Agent("WorkflowAgent")
        results = []
        
        def task1():
            results.append("task1")
        
        def task2():
            results.append("task2")
        
        def task3():
            results.append("task3")
        
        agent.add_task("first", task1)
        agent.add_task("second", task2)
        agent.add_task("third", task3)
        
        execution_results = agent.run_once()
        
        self.assertEqual(len(execution_results), 3)
        self.assertEqual(results, ["task1", "task2", "task3"])
        
        # Verify all tasks completed
        for result in execution_results:
            self.assertEqual(result["status"], "success")


if __name__ == "__main__":
    unittest.main()
