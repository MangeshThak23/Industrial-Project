######################################################
#  
#  Importing required libraries
#
######################################################

import psutil
import sys
import os
import time
import schedule

######################################################
#   Function Name :         Platform Survillence
#   Input :                 Time and Name of Directory
#   Description :           Create the process logs periodically
#   Date :                  19/07/2026
#   Author :                Mangesh Rajaram Thak
#
######################################################


def ProcessScan():
    listprocess = []

    #Get details for every running process-(Iterate)--->
    for proc in psutil.process_iter():
        info = proc.as_dict(attrs=["pid","name","username","status"])
        info["cpu_percent"] = proc.cpu_percent(None)
        info["memory_percent"] = proc.memory_percent()

        listprocess.append(info)

    return listprocess

def PlatformSurvillence(FolderName):
    Border = "-"*50

    Ret = False
    Ret = os.path.exists(FolderName)

    if(Ret == True):
        Ret = os.path.isdir(FolderName)
        if(Ret == False):
            print("Unable to proceed as directory name is existing but it's not a directory")
            return
    else:
        os.mkdir(FolderName)
        print("Directory for log file gets created sucessfully.")

    #strftime used for string format time
    timestamp = time.strftime("%Y-%m-%d_%H_%M-%S")

    FileName = os.path.join(FolderName,"Marvellous_%s.log" %timestamp)

    fobj = open(FileName,"w")

    print(f"Log file gets successfully create with name {FileName}")

    fobj.write(Border+"\n")
    fobj.write("----Marvellous platform survillence system----\n")
    fobj.write("Log file gets created at: "+timestamp+"\n")
    fobj.write(Border+"\n\n")

    fobj.write("--------System Report--------\n")

    #CPU Information---->
    fobj.write("Number of active CPU cores: %s\n"%psutil.cpu_count())
    fobj.write("CPU Usage: %s %%\n"%psutil.cpu_percent())
    fobj.write(Border+"\n")

    #RAM Information---->
    memory = psutil.virtual_memory()
    fobj.write("RAM Usage: %s %%\n"%memory.percent)
    fobj.write("Total RAM Available: %s\n"%memory.total)
    fobj.write(Border+"\n")

    #Network Usage---->
    netobj = psutil.net_io_counters()
    
    fobj.write("Network Usage Report\n")

    #Convert bytes to MB for upload
    fobj.write("Sent : %.2f MB\n"%(netobj.bytes_sent / (1024*1024))) 

    #Convert bytes to MB for download
    fobj.write("Received : %.2f MB\n"%(netobj.bytes_recv / (1024*1024))) 

    #Process log---->
    Data = ProcessScan()

    for info in Data:
           
        fobj.write("PID:       %s\n"%info.get("pid"))
        fobj.write("Name:      %s\n"%info.get("name"))
        fobj.write("User Name: %s\n"%info.get("username"))
        fobj.write("Status:    %s\n"%info.get("status"))
        fobj.write("CPU usage: %.2f\n"%info.get("cpu_percent"))
        fobj.write("RAM usage: %.2f\n"%info.get("memory_percent"))
        
        fobj.write(Border+"\n")

    fobj.write(Border+"\n")
    fobj.write("----------------------End of log file----------------------\n")
    fobj.write(Border+"\n")

    fobj.close()


######################################################
#   Function Name :         main
#   Input :                 Command line arguments
#   Description :           It controls the script
#   Date :                  19/07/2026
#   Author :                Mangesh Rajaram Thak
#
######################################################
def main():
    
    Border = "-"*50
    print(Border)
    print("----Marvellous platform survillence system----")
    print(Border)

    #--h and --u handling
    if(len(sys.argv) == 2):
        if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
            print("This automation script is used to perform.")
            print("1 : It fetch the information of running processes.")
            print("2 : It fetch the information about the primary storage as RAM.")
            print("3 : It fetch the information about the secondary storage as HDD.")
            print("4 : It fetch the information about the microprocessor.")
            print("5 : It gets auto scheduled periodically.")
            print("6 : It maintains all records into log file.")
            print("7 : It sends the log files through mail periodically.")

        elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
            print("Use the automation script as: ")
            print(f"python {sys.argv[0]} Time_Interval Folder_Name")
            print("Time_Interval : Time in minutes for periodic execution.")
            print("Folder_Name : Name of folder for the log file creation")
           
        else:
            print("Unable to proceed as there is no matcing arguments.")
            print("Please use --h or --u flag for getting more details.")

    #Actual project code
    elif(len(sys.argv) == 3):
        
        print("Schedular started sucessfully.")
        print("Press Ctrl + C to abort the automation script.")

        schedule.every(int(sys.argv[1])).minutes.do(PlatformSurvillence,sys.argv[2])
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        print("Invalid number of arguments.")
        print("Unable to proceed as arguments are not matching.")
        print("Please use --h or --u flag for getting more details.")
        
    print(Border)
    print("----Thank you for using our automation system.----")
    print(Border)
    
######################################################
#  
#  Starter of the automation script
#
######################################################

if __name__ == "__main__":
    main()