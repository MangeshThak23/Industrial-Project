##########################################################
#
#   Importing required libraries
#
##########################################################
import sys
import os
import hashlib
from pathlib import Path
import UserDefineValidationModule as UVM
import time
import datetime
import argparse
import smtplib
from email.message import EmailMessage
import mimetypes
import schedule

##########################################################
#
#   Function name :     Directorysanitize
#   Input :             Name of Directory, Email, Interval 
#   Description :       Deletes all Duplicate files periodically
#   Date :              25/07/2026   
#   Author :            Mangesh Rajaram Thak
#
########################################################## 
def calculatechecksum(filename):

    fobj = open(filename,"rb")
    hohj = hashlib.md5()
    Buffer = fobj.read(1000)
    while len(Buffer) > 0:
        hohj.update(Buffer)
        Buffer = fobj.read(1000)
    fobj.close()
    return hohj.hexdigest()

def IdentfyDuplicateFiles(derectortypath,emailstatus,email): 
             file_count = 0
             duplicatefound = 0
             duplicatedeleted = 0
             deletedduplicate = []
             duplicatechecksumvalues = []
             starttime = time.ctime()
             scanDirectory = os.path.abspath(derectortypath)
             timestam = time.ctime()
             TimeStamp = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
             
             LogFileName = "Marvellous_%s.log"%(TimeStamp)
        
             fobj = open(LogFileName,"w")
             Filecount = {}
             fobj.write("\n" + "=" * 80 + "\n")
             fobj.write(f"Starting time of directory scanning: {starttime}\n")
             fobj.write(f"Name of the directory scanned: {scanDirectory}\n")
             for FolderName,subFolder,Filename in os.walk(derectortypath):
              for fname in Filename:
                    file_count = file_count + 1
                    filepath = os.path.join(FolderName, fname)
                    errors = UVM.filevalidate(filepath)
                    if errors:
                        print("File Validation failed:")
                        fobj.write(f"Validation failed for file: {filepath}\n")
                        for error in errors:
                         fobj.write(f"- {error}\n")
                         continue
                    else:
                         fobj.write(f"File validation successful: {filepath}\n")
                    try:
                        checksum = calculatechecksum(filepath)
                        if checksum in Filecount:
                              duplicatefound = duplicatefound + 1
                              fobj.write(f"Duplicate file found: {filepath}\n")
                              fobj.write(f"Original file kept: {Filecount[checksum]}\n")
                              fobj.write(f"Checksum value: {checksum}\n")
                              os.remove(filepath)
                              duplicatedeleted = duplicatedeleted + 1
                              deletedduplicate.append(filepath)
                              duplicatechecksumvalues.append(checksum)
                              fobj.write(f"Deleted duplicate file: {filepath}\n")
                        else:
                              Filecount[checksum] = filepath
                    except Exception as e:
                     
                     fobj.write(f"Error processing {filepath}: {e}\n")
             end_time = time.ctime()

             fobj.write(f"Completion time of directory scanning: {end_time}\n")
             fobj.write(f"Total number of files scanned: {file_count}\n")
             fobj.write(f"Total number of duplicate files found: {duplicatefound}\n")
             fobj.write(f"Total number of duplicate files deleted: {duplicatedeleted}\n")

             fobj.write("Complete paths of all deleted duplicate files:\n")
             if deletedduplicate:
              for deleted_file in deletedduplicate:
                 fobj.write(f"- {deleted_file}\n")
             else:
              fobj.write("- None\n")

             fobj.write("Checksum values of duplicate files:\n")
             if duplicatechecksumvalues:
              for checksum in duplicatechecksumvalues:
                 fobj.write(f"- {checksum}\n")
             else:
                fobj.write("- None\n")

             fobj.write(f"Email delivery status: {emailstatus}\n")
             fobj.write("Complete paths of all deleted duplicate files:\n")
             fobj.write("=" * 80 + "\n")
             isvalid, message = UVM.emailvalidate(email)
             fobj.close()
             if isvalid:
              sendsimpleemail(email,file_count,starttime,end_time,scanDirectory,duplicatefound,duplicatedeleted,LogFileName)
             else:
              print(isvalid)
              print(message)

def sendsimpleemail(recipient_email,file_count,starttime,end_time,scanDirectory,duplicatefound,duplicatedeleted,attachment_path):
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 587

    SENDER_EMAIL = os.getenv("SENDER_EMAIL", "mangesht.2324@gmail.com")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "abc1231234")
    msg = EmailMessage()
    msg["Subject"] = "Duplicate email from Automation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = recipient_email
    msg.set_content(f"""Jay Ganesh,

The duplicate-file removal operation has been completed successfully.

Operation Statistics:

Start time of scanning          : {starttime}
Completion time of scanning     : {end_time}
Directory scanned               : {scanDirectory}
Total number of files scanned   : {file_count}
Total number of duplicates found: {duplicatefound}
Total number of duplicate files deleted: {duplicatedeleted}

Please find the detailed log file attached to this email.

Regards,
Marvellous Automation System
""")

    # Attach file if provided
    if attachment_path:
        if os.path.exists(attachment_path):
            mime_type, _ = mimetypes.guess_type(attachment_path)
            if mime_type:
                maintype, subtype = mime_type.split("/", 1)
            else:
                maintype, subtype = "application", "octet-stream"
            
            with open(attachment_path, "rb") as f:
                msg.add_attachment(
                    f.read(),
                    maintype=maintype,
                    subtype=subtype,
                    filename=os.path.basename(attachment_path),
                )

            print(f"Attached file: {attachment_path}")
        else:
            print(f"Attachment not found: {attachment_path}")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            print(f"✓ Email successfully sent to {recipient_email}")
    except Exception as e:
        print(f"✗ Failed to send email: {e}")  

##########################################################
#
#   Function name :     main
#   Input :             Command line arguments
#   Description :       It controls the script
#   Date :              25/07/2026   
#   Author :           Mangesh Rajaram Thak
#
##########################################################

def main():
    isvalid, message = UVM.validatecommandline()
    if sys.argv[1] == "--help":
        print("""
------------------------------------------------------------
          Duplicate File Removal Automation
------------------------------------------------------------

Description:
    This script scans a directory, identifies duplicate files
    using file checksums, deletes duplicate files, creates a
    log file, and sends the log file through email.

Usage:
    python DuplicateFileRemoval.py <DirectoryPath> <IntervalInMinutes> <ReceiverEmail>

Arguments:
    <DirectoryPath>
        Path of the directory to scan for duplicate files.

    <IntervalInMinutes>
        Time interval (in minutes) between consecutive scans.

    <ReceiverEmail>
        Email address where the generated log file will be sent.

Example:
    python DuplicateFileRemoval.py E:/Data/Demo 50 mangesh@gmail.com

Help:
    python DuplicateFileRemoval.py --help
    python DuplicateFileRemoval.py -h

------------------------------------------------------------
""")
        sys.exit(1)
    if sys.argv[1] == "Usage":
       print("""
Usage:
    python DuplicateFileRemoval.py <AbsoluteDirectoryPath> <TimeIntervalInMinutes> <ReceiverEmailAddress>

Example:
    python DuplicateFileRemoval.py E:/Data/Demo 50 mangesh@gmail.com
""")
       sys.exit(1)
       
    if not isvalid:
     print(message)
     sys.exit(1)

    isvalid, message = UVM.smtpconnectionvalidate(smtp_server="smtp.gmail.com",smtp_port=587,username=sys.argv[2],password="abc1231234")
    print(isvalid)
    print(message)

    errors = UVM.DirectoryValidation(sys.argv[1])
    if errors:
     print("Validation Directory failed:")
    for error in errors:
        print(f"- {error}")
    else:
      isvalid, message = UVM.validateinterval(int(sys.argv[3]))
      if isvalid:
         print("Automation started.")
         schedule.every(int(sys.argv[3])).hour.do(IdentfyDuplicateFiles,sys.argv[1],message,sys.argv[2])
         #IdentfyDuplicateFiles(sys.argv[1],message,sys.argv[2])
         print("Automation completed.")
      else:
         print(f"Valid: {isvalid}")
         print(f"Message: {message}")      
          
    while True:
        schedule.run_pending()
        time.sleep(1)
##########################################################
#
#   Starter of the automation script
#
##########################################################
if __name__ == "__main__":    
    main()