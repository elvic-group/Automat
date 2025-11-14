#!/usr/bin/env python3
"""
Example tasks and workflows for the Automat agent.
"""

import os
import subprocess
from datetime import datetime
from pathlib import Path


def backup_files():
    """Example: Backup important files."""
    print("Backing up files...")
    # Placeholder for actual backup logic
    print("Backup completed successfully")


def check_disk_space():
    """Example: Check available disk space."""
    import shutil
    usage = shutil.disk_usage("/")
    used_percent = (usage.used / usage.total) * 100
    print(f"Disk usage: {used_percent:.1f}%")
    if used_percent > 80:
        print("Warning: Disk space is running low!")


def send_notification(message: str):
    """Example: Send a notification."""
    print(f"[NOTIFICATION] {message}")


def health_check():
    """Example: Perform system health check."""
    print("Running health check...")
    checks = {
        "python_version": f"Python {os.sys.version.split()[0]}",
        "timestamp": datetime.now().isoformat(),
        "working_directory": os.getcwd()
    }
    
    for key, value in checks.items():
        print(f"  {key}: {value}")
    
    print("Health check completed")


def cleanup_temp_files():
    """Example: Clean up temporary files."""
    print("Cleaning up temporary files...")
    temp_dir = Path("/tmp")
    if temp_dir.exists():
        # Count files (example - not actually deleting)
        file_count = sum(1 for _ in temp_dir.glob("*"))
        print(f"Found {file_count} items in temp directory")
    print("Cleanup completed")


def generate_report():
    """Example: Generate a status report."""
    report = f"""
    === Automat Status Report ===
    Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    
    System Status: Operational
    Tasks Completed: Various automation tasks
    Next Check: Scheduled per configuration
    
    ============================
    """
    print(report)


if __name__ == "__main__":
    # Demonstrate example tasks
    print("=== Automat Example Tasks ===\n")
    
    print("1. Health Check")
    health_check()
    print()
    
    print("2. Disk Space Check")
    check_disk_space()
    print()
    
    print("3. Generate Report")
    generate_report()
    print()
    
    print("4. Send Notification")
    send_notification("All systems operational")
    print()
