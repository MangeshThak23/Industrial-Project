###################################################################################################
#
#   Project Name    : Marvellous Data Shield – Automated Backup & File Monitoring System   
#   File Name       : Data_Shield.py
#   Description     : This application performs automated incremental backup of files by copying
#                     only newly added or modified files using MD5 hashing. It also creates a
#                     compressed ZIP archive of the backup for efficient storage.
#
#   Author          : Mangesh Thak
#   Date            : 15/05/2026
#
###################################################################################################

import sys
import time
import os
import schedule
import shutil
import hashlib
import zipfile

Border = "-" * 60

###################################################################################################
#
#   Function Name   : MakeZip
#   Description     : Compresses the backup directory into a timestamped ZIP archive for storage.
#   Input           : FolderName (string)
#   Output          : ZipFileName (string)
#
###################################################################################################
def MakeZip(FolderName):
    # Generate unique timestamp for zip file
    TimeStamp = time.strftime("%Y-%m-%d_%H-%M-%S")
    ZipFileName = FolderName + "_" + TimeStamp + ".zip"

    # Create zip object in write mode
    zobj = zipfile.ZipFile(ZipFileName, "w", zipfile.ZIP_DEFLATED)

    # Traverse entire folder structure
    for root, dirs, files in os.walk(FolderName):
        for file in files:
            # Full path of file
            FullPath = os.path.join(root, file)

            # Maintain relative structure inside zip
            RelativePath = os.path.relpath(FullPath, FolderName)

            # Add file to zip
            zobj.write(FullPath, RelativePath)

    zobj.close()

    return ZipFileName

###################################################################################################
#
#   Function Name   : CalculateHash
#   Description     : Calculates MD5 hash value of a given file.
#   Input           : FilePath (string)
#   Output          : Hash value (string)
#
###################################################################################################
def CalculateHash(FilePath):
    # Create MD5 hash object
    hobj = hashlib.md5()

    # Open file in binary mode
    with open(FilePath, "rb") as fobj:
        while True:
            # Read file in chunks (efficient for large files)
            Data = fobj.read(1024)

            if not Data:
                break

            # Update hash with data chunk
            hobj.update(Data)

    # Return hexadecimal hash value
    return hobj.hexdigest()

###################################################################################################
#
#   Function Name   : BackUpFiles
#   Description     : Performs incremental backup by copying only new or modified files.
#   Input           : Source (string), Destination (string)
#   Output          : List of copied files
#
###################################################################################################
def BackUpFiles(Source, Destination):
    CopiedFiles = []

    print("Initializing destination directory :", Destination)
    print("Setting up backup folder...")

    # Create destination folder if not exists
    os.makedirs(Destination, exist_ok=True)

    # Traverse source directory
    for root, dirs, files in os.walk(Source):
        for file in files:

            # Source file path
            SourcePath = os.path.join(root, file)

            # Maintain same folder structure in destination
            RelativePath = os.path.relpath(SourcePath, Source)
            DestPath = os.path.join(Destination, RelativePath)

            # Create required directories in destination
            os.makedirs(os.path.dirname(DestPath), exist_ok=True)

###################################################################
# Copy Condition:
# 1. File does not exist in destination
# 2. File exists but content has changed (hash mismatch)
###################################################################
            if (not os.path.exists(DestPath)) or \
               (CalculateHash(SourcePath) != CalculateHash(DestPath)):

                # Copy file with metadata (timestamp, permissions)
                shutil.copy2(SourcePath, DestPath)

                # Track copied file
                CopiedFiles.append(RelativePath)

    return CopiedFiles

###################################################################################################
#
#   Function Name   : DataShieldStart
#   Description     : Initiates backup process and creates ZIP archive.
#   Input           : Source directory (default = "Data")
#   Output          : None
#
###################################################################################################
def DataShieldStart(Source="Data"):
    BackupFolder = "Backup"

    print(Border)
    print("Backup Process Started at :", time.ctime())
    print(Border)

    # Perform incremental backup
    Files = BackUpFiles(Source, BackupFolder)

    # Create compressed archive of backup
    ZipFile = MakeZip(BackupFolder)

    print("Backup Completed Successfully")
    print("Total Files Copied :", len(Files))
    print("ZIP File Created   :", ZipFile)

###################################################################################################
#
#   Function Name   : main
#   Description     : Entry point of the application. Handles command-line arguments and scheduling.
#   Input           : Command-line arguments
#   Output          : None
#
###################################################################################################
def main():

    print(Border)
    print("-------- Marvellous Data Shield - Automated Backup & File Monitoring System --------")
    print(Border)

###################################################################
#   Case 1 : Help / Usage Information
###################################################################
    if len(sys.argv) == 2:

        if sys.argv[1].lower() == "--h":
            
            print("This script is used to:")
            print("1. Perform automated incremental backup")
            print("2. Sync files using MD5 checksum validation")
            print("3. Generate compressed timestamped ZIP archives")

        elif sys.argv[1].lower() == "--u":
            print("Usage:")
            print("python Data_Shield.py <TimeInterval> <SourceDirectory>")
            print("TimeInterval   : Time in minutes")
            print("SourceDirectory: Folder to backup")

        else:
            print("Invalid option. Use --h or --u")

###################################################################
# Case 2 : Execute Backup with Scheduler
###################################################################
    elif len(sys.argv) == 3:

        TimeInterval = int(sys.argv[1])
        SourceDirectory = sys.argv[2]

        print("Time Interval    :", TimeInterval, "minutes")
        print("Source Directory :", SourceDirectory)

        # Schedule backup job at given interval
        schedule.every(TimeInterval).minutes.do(DataShieldStart, SourceDirectory)

        print(Border)
        
        print(" Marvellous Data Shield - Protection Active ")
        print(Border)
        print("Status          : Running and Monitoring")
        print("Action Required : Press Ctrl + C to terminate execution safely")
        print(Border)

        # Infinite loop to keep scheduler running
        while True:
            schedule.run_pending()
            time.sleep(1)

###################################################################
# Case 3 : Invalid Input
###################################################################
    else:
        print("Invalid arguments. Use --h or --u")

    print(Border)
    print("------------- Thank You ----------------")
    print(Border)

###################################################################################################
#
#   Application Starter
#
###################################################################################################
if __name__ == "__main__":
    main()