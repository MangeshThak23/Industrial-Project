# Marvellous Data Shield – Automated Backup & File Monitoring System

An automated file backup, synchronization, and monitoring system built with Python. **Marvellous Data Shield** securely manages and backs up important data directories by performing efficient incremental backups using MD5 checksum validation, followed by automated timestamped ZIP archive creation and execution scheduling.

---

## Features

- **Incremental Backup:** Automatically detects newly added or modified files to avoid redundant copying.
- **MD5 Checksum Verification:** Compares file content hashes rather than relying solely on timestamps or file sizes, ensuring high data integrity.
- **Directory Structure Preservation:** Replicates the exact nested folder hierarchy from the source directory to the backup location and inside the ZIP archive.
- **Automated Compression:** Automatically packages the backup folder into a compressed, timestamped ZIP archive (`.zip`) for space-efficient long-term storage and portability.
- **Periodic Scheduling:** Uses Python's `schedule` module to execute backups automatically at user-defined time intervals.
- **Command-Line Interface (CLI):** Fully manageable via command-line arguments with built-in help (`--h`) and usage (`--u`) guides.

---

## Tech Stack

- **Language:** Python 3.x
- **Standard Libraries:** `sys`, `time`, `os`, `shutil`, `hashlib`, `zipfile`
- **Third-Party Libraries:** `schedule`

---

## Project Structure

```text
Marvellous-Data-Shield/
│
├── Data_Shield.py   # Main application script
├── Data/            # Default source directory (user data)
├── Backup/          # Automated backup destination folder
└── *.zip            # Generated compressed backup archives
```

---

## Installation & Prerequisites

1. Ensure you have **Python 3.x** installed on your system.
2. Install the required external scheduling dependency via pip:
   ```bash
   pip install schedule
   ```

---

## Usage Instructions

The script is executed from the command line and supports different modes of operation based on the arguments provided.

### 1. View Help Documentation
To view what the script does:
```bash
python Data_Shield.py --h
```

### 2. View Usage Syntax
To see the required command-line parameters:
```bash
python Data_Shield.py --u
```

### 3. Run Scheduled Incremental Backup
To run backups automatically at a specified time interval (in minutes):
```bash
python Data_Shield.py 30 Data
```
*This command schedules the `Data` directory to be incrementally backed up every 30 minutes.*

---

## Example Execution Output

```text
------------------------------------------------------------
-------- Marvellous Data Shield - Automated Backup & File Monitoring System --------
------------------------------------------------------------
Time Interval    : 30 minutes
Source Directory : Data
------------------------------------------------------------
------------------------------------------------------------
 Marvellous Data Shield - Protection Active 
------------------------------------------------------------
Status          : Running and Monitoring
Action Required : Press Ctrl + C to terminate execution safely
------------------------------------------------------------

------------------------------------------------------------
Backup Process Started at : Fri May 15 14:30:00 2026
------------------------------------------------------------
Initializing destination directory : Backup
Setting up backup folder...
Backup Completed Successfully
Total Files Copied : 3
ZIP File Created   : Backup_2026-05-15_14-30-00.zip
```

---

## How It Works

1. **Initialization:** The script starts a scheduler loop waiting for the configured time interval.
2. **Traversal & Hashing (`BackUpFiles`):** 
   - It walks through the source directory.
   - For every file, it calculates an MD5 checksum chunk-by-chunk to handle large files efficiently.
   - If the file does not exist in the `Backup` folder or its hash differs from the existing backup copy, it uses `shutil.copy2()` to copy it along with its metadata.
3. **Archiving (`MakeZip`):** Once file copying concludes, it compiles the entire backup directory into a compressed `.zip` file annotated with a unique timestamp (e.g., `Backup_2026-05-15_14-30-00.zip`).
4. **Execution Log:** Outputs summary details including total files copied and the generated ZIP archive name.

---

## Author

- **Mangesh Thak**
- **Date:** 15/05/2026
