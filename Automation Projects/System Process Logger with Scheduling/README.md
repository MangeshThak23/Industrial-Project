# 🖥️ System Process Logger with Scheduling

A robust, lightweight Python automation tool that periodically captures active system processes, Process IDs (PIDs), user permissions, and memory usage percentages, saving detailed reports into timestamped log files.

---

## 🚀 Features

- **Automated Scheduling**: Uses the `schedule` library to run process audits at custom, user-defined time intervals (in minutes).
- **Immediate Startup**: Automatically triggers an initial process capture upon script launch so you don't have to wait for the first interval.
- **Robust Exception Handling**: Safely handles system-level process exceptions (`NoSuchProcess`, `AccessDenied`, `ZombieProcess`) and sanitizes `NoneType` values for process names, users, and memory percentages.
- **Dynamic Metadata Inspection**: Features a built-in documentation inspector (`show_project_details()`) that dynamically displays project metadata and function docstrings on startup.
- **Graceful Termination**: Designed with clean KeyboardInterrupt exception management for safe command-line shutdowns.

---

## 🛠️ Prerequisites & Dependencies

Ensure you have Python 3.x installed along with the required third-party libraries:

```bash
pip install psutil schedule
```

---

## 📂 Project Structure

```text
System-Process-Logger/
│
├── process_logger.py       # Main Python automation script
├── Process_Logs/           # Default output directory for generated log files
│   └── process_log_*.txt   # Timestamped execution reports
└── README.md               # Project documentation
```

---

## 💻 Code Overview

The script is cleanly structured into modular, documented functions:

1. **`log_processes(log_folder)`**: 
   - Scans all running system processes using `psutil`.
   - Formats and writes PID, Process Name, User, and Memory percentage into a structured text report.
2. **`schedule_process_logger(folder_name, interval_minutes)`**: 
   - Manages the execution loop, triggers the immediate initial run, and schedules recurring background tasks.
3. **`show_project_details()`**: 
   - Dynamically prints project information and function docstrings (`__doc__`) for better code documentation.
4. **`main()`**: 
   - Handles user configuration inputs (custom folder names and intervals) with smart error handling and default fallbacks.

---

## 🚀 How to Run

1. Clone or download this repository.
2. Open your terminal/command prompt in the project directory.
3. Run the script:
   ```bash
   python process_logger.py
   ```
4. Follow the interactive prompts in the terminal:
   - Enter your preferred log folder name (or press `Enter` to use the default `'Process_Logs'`).
   - Enter your desired logging interval in minutes (or press `Enter` to use the default `1` minute).

---

## 📄 Example Log Output

```text
============================================================
System Process Log - 2026-06-13 14:30:00
============================================================

PID        Process Name                   User                 Memory %       
---------------------------------------------------------------------------
0          System Idle Process            N/A                  0.0            
4          System                         N/A                  0.15           
824        smss.exe                       NT AUTHORITY\SYSTEM  0.02           
...
```

---

## 👤 Author

- **Mangesh Thak**
- **Created Date**: 13/06/2026
