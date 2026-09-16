#========================================================================
#Project Name : System Process Logger with Scheduling
#Author       : Mangesh Thak
#Created Date : 13/06/2026
#Description  : A Python automation tool that periodically captures active 
#               system processes, PIDs, user permissions, and memory usage,
#               saving the detailed report into timestamped log files.
#Dependencies : psutil, schedule, time, os, datetime
#========================================================================

import os
import psutil
import time
import schedule
from datetime import datetime

#========================================================================
#Logs running system processes into a timestamped file.
#Parameters:log_folder (str): The directory path where log files will be stored.
#Behavior:
#      - Automatically creates the log folder if it does not exist.
#      - Generates a unique filename using the current timestamp.
#      - Iterates through all active system processes using psutil.
#      - Safely handles missing/None attributes and access exceptions.
#      - Writes PID, Process Name, User, and Memory % into a formatted text file.
#========================================================================

def log_processes(log_folder):
       
    # Create log folder if it doesn't exist
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # Timestamped log filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_folder, f"process_log_{timestamp}.txt")

    # Open log file for writing
    with open(log_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write(f"System Process Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")
        f.write("{:<10} {:<30} {:<20} {:<15}\n".format("PID", "Process Name", "User", "Memory %"))
        f.write("-"*75 + "\n")

        # Fetch process details
        for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_percent']):
            try:
                pid = proc.info['pid']
                name = (proc.info['name'] or "Unknown")
                user = (proc.info['username'] or "N/A")
                memory = round(proc.info['memory_percent'], 2)
                f.write("{:<10} {:<30} {:<20} {:<15}\n".format(pid, name, user, memory))
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    print(f"Log file created: {log_file}")

#========================================================================
#Schedules process logging tasks at specified user-defined intervals.
#Parameters:
#           folder_name (str): Directory where log files should be saved.
#           interval_minutes (int): Time gap in minutes between each log capture.
#Behavior:
#      - Triggers an immediate initial log creation on startup.
#      - Registers a recurring job using the 'schedule' library.
#      - Runs an infinite loop monitoring pending tasks with graceful exit (Ctrl+C).
#========================================================================

def schedule_process_logger(folder_name, interval_minutes):
    """Schedules process logging at given intervals."""
    
    print("\n=== System Process Logger with Scheduling ===")
    print(f"Logs will be saved in: {folder_name}")
    print(f"Logging interval: Every {interval_minutes} minute(s)\n")
    
    # Schedule the task
    schedule.every(interval_minutes).minutes.do(log_processes, log_folder=folder_name)

    # Run indefinitely
    while True:
        schedule.run_pending()
        time.sleep(1)

#========================================================================
#Main entry point to gather user configurations and start the scheduler.
#Behavior:
#        - Displays project and function details using docstrings.
#        - Prompts the user to specify a custom log directory and interval.
#        - Handles invalid interval inputs safely with a default fallback.
#        - Kicks off the continuous scheduler workflow.
#========================================================================

def main():
    # Get custom folder name and interval from user
    folder = input("Enter folder name to save logs (default: 'Process_Logs'): ") or "Process_Logs"
    interval = input("Enter interval in minutes (default: 1): ") or "1"

    try:
        interval = int(interval)
    except ValueError:
        print("Invalid interval, using default of 1 minute.")
        interval = 1

    # Start scheduled process logging
    schedule_process_logger(folder, interval)

#========================================================================
#Starter
#========================================================================
if __name__ == "__main__":
    main()