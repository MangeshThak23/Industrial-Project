# Duplicate File Cleaner & Log Automation

An advanced Python-based automation utility designed to scan directories, identify and remove duplicate files using MD5 cryptographic checksums, and automatically email comprehensive audit logs at user-defined intervals.

## Features

- **Checksum-Based Detection:** Utilizes `hashlib` (MD5) to accurately detect duplicate files by comparing file content rather than just names or sizes.
- **Automated Audit Logging:** Dynamically generates timestamped log files (`.log`) recording operation metrics, file paths, checksum values, and validation results.
- **Periodic Scheduling:** Integrates the `schedule` library to execute routine directory cleanups automatically at specified intervals.
- **Email Automation:** Automatically packages execution statistics and attaches audit log files, sending them securely via `smtplib` and `EmailMessage`.
- **Modular Validation:** Partners with a custom validation module (`UserDefineValidationModule`) to ensure secure command-line inputs, directory paths, file safety, and recipient email formatting.

## Tech Stack

- **Language:** Python
- **Modules & Libraries:** `os`, `sys`, `hashlib`, `time`, `datetime`, `argparse`, `smtplib`, `mimetypes`, `schedule`, `pathlib`, `UserDefineValidationModule`

## Getting Started

### Prerequisites

Ensure you have Python installed along with the required external dependencies:

```bash
pip install schedule
```

Make sure your custom validation module (`UserDefineValidationModule.py`) is placed in the same directory or available in your Python path.

### Usage

Run the script from the command line by passing the absolute directory path, the time interval (in minutes), and the receiver's email address:

```bash
python Duplicate_File_Removal_Final.py <DirectoryPath> <IntervalInMinutes> <ReceiverEmail>
```

**Example:**
```bash
python Duplicate_File_Removal_Final.py E:/Data/Demo 50 mangesh@gmail.com
```

### Sample Program Output

```text
True
SMTP connection validated successfully.
Automation started.
Automation completed.
Attached file: Marvellous_25_07_2026_18_30_00.log
✓ Email successfully sent to mangesh@gmail.com
```

### Help & Usage Flags

* To view detailed help documentation:
  ```bash
  python Duplicate_File_Removal_Final.py --help
  ```
* To view quick usage instructions:
  ```bash
  python Duplicate_File_Removal_Final.py Usage
  ```

## Author

**Mangesh Rajaram Thak**
