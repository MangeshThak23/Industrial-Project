# Automated Process Logger & Scheduling System

An automated system surveillance and logging utility built with Python. This script periodically captures critical system performance metrics—including CPU utilization, RAM usage, network statistics, and active process details—and logs them into structured, timestamped text files.

## Features

- **Periodic Automation:** Utilizes the `schedule` library to execute surveillance scans at user-defined time intervals.
- **System Health Metrics:** Captures active CPU core counts, overall CPU percentage, RAM consumption, and network upload/download statistics.
- **Process Monitoring:** Iterates through active system processes to extract individual Process IDs (PIDs), names, execution states, usernames, and resource utilization percentages (`psutil`).
- **Filesystem Management:** Automatically checks for the target log directory and creates it if it does not exist, appending clean, formatted records.
- **Command-Line Interface (CLI):** Built-in helper flags (`--h` for help and `--u` for usage instructions) for smooth user onboarding.

## Tech Stack

- **Language:** Python
- **Libraries:** `psutil`, `schedule`, `os`, `sys`, `time`

## Getting Started

### Prerequisites

Make sure you have Python installed along with the required external dependencies:

```bash
pip install psutil schedule
```

### Usage

Run the script from the command line by passing the desired **time interval (in minutes)** and the **folder name** where logs should be saved:

```bash
python script_name.py <Time_Interval> <Folder_Name>
```

**Example:**
```bash
python script_name.py 5 System_Logs
```

### Sample Program Output

```text
--------------------------------------------------
----Marvellous platform survillence system----
--------------------------------------------------
Scheduler started successfully.
Press Ctrl + C to abort the automation script.
[2026-07-19 12:00:00] System log successfully recorded.
Directory for log file gets created successfully.
Log file gets successfully create with name System_Logs/Marvellous_2026-07-19_12_00-00.log
```

### Help & Usage Flags

* To view detailed information about the script capabilities:
  ```bash
  python script_name.py --h
  ```
* To view usage instructions:
  ```bash
  python script_name.py --u
  ```

## Author

**Mangesh Rajaram Thak**
