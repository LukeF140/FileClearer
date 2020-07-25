# Imports
import os

# Variables
files = {}  # k = fileName, v = [instances], near certain matches
saveSpace = 0 # Amount of storage that can be saved (in bytes)

def WriteReport(dirClean, sameFiles, ss):
    # REPORT WRITING
    report = ['-------------------- REPORT FROM FILE CLEANER --------------------\n----------------------- MADE BY LUKE FAIRS -----------------------\n'] # Title
    report.append('Report about directory: ' + dirClean) # Directory concerned in the report
    report.append('\nA "near certain duplicate" is a file that has the same name (disregarding any \' - Copy\') and has the same file size\n') # File system expliation
    report.append('Number of near certain duplicates: ' + str(len(sameFiles))) # Number of near certain duplicates
    # Coverts the save space to the largest possible unit for it to be easily understanderble
    unit = "B"
    if ss >= 1024:
        ss = ss/1024
        unit = "KB"
        if ss >= 1024:
            ss = ss/1024
            unit = "MB"
            if ss >= 1024:
                ss = ss/1024
                unit = "GB"
                if ss >= 1024:
                    ss = ss/1024
                    unit = "TB"
                    if ss >= 1024:
                        ss = ss/1024
                        unit = "PB"
                        if ss >= 1024:
                            ss = ss/1024
                            unit = "EB"
                            if ss >= 1024:
                                ss = ss/1024
                                unit = "ZB"
                                if ss >= 1024:
                                    ss = ss/1024
                                    unit = "YB"
    report.append('If all files removed how much space can be saved: ' + str(round(ss,2)) + unit) # How much space can be saved
    # Listing of Duplicate files
    report.append('\n\n***** NEAR CERTAIN DUPLICATES: *****')
    for k in sameFiles:
        report.append(k)
        for v in sameFiles[k]:
            report.append('    ' + v)
        report.append('')
    report.append('\n')

    # Returns the report
    return report


# Gets the directory to check
dirToSort = input("Input the Directory to Check: ")
while not os.path.exists(dirToSort): # Makes sure the directory exists
    print(dirToSort + ", DOES NOT EXIST, PLEASE ENTER A VALID DIRECTORY")
    dirToSort = input("Input the Directory to Check: ")

# Gets if a report should be outputted to the console
printReport = input("Do you want the report outputed to the console: (yes or no) ").upper()
while not (printReport == "YES" or printReport == "NO" or printReport == "Y" or printReport == "N"): # Makes sure there is a valid input
    print(printReport + ", IS NOT A VALID ANSWER")
    printReport = input("Do you want the report outputed to the console: (yes or no) ").upper()

# Gets if a report should be exported to a .txt
extractFile = input("Do you want the report to be put in a .txt file: (yes or no) ").upper()
while not (extractFile == "YES" or extractFile == "NO" or extractFile == "Y" or extractFile == "N"): # Makes sure there is a valid input
    print(extractFile + ", IS NOT A VALID ANSWER")
    extractFile = input("Do you want the report to be put in a .txt file: (yes or no) ").upper()


try:
    curRoot = "" # Used to see if the folder currently in has changed
    # Walks through directory
    for root, subfolders, filenames in os.walk(dirToSort):
        # Iterates through all files in the current directory
        for file in filenames:
            filePath = root + "\\" + file # Creates file path to the file
            # Tells the user what is currently occuring
            if root != curRoot:
                curRoot = root
                print("Currently in: " + root)
            # Removes a " - Copy" from the file if there is one
            filename, fileExtension = os.path.splitext(file)
            fileNameTemp = file.rsplit(" - Copy", 1)
            if not fileNameTemp[0].endswith(fileExtension):
                tempName = fileNameTemp[0] + fileExtension
            else:
                tempName = fileNameTemp[0]
            # Trys to compare the file sizes, if there is no file of that name then the file is added
            try:
                if os.path.getsize(filePath) == os.path.getsize(files[tempName][0]):
                    files[tempName].append(filePath)
                    saveSpace += os.path.getsize(filePath)
            except KeyError:
                files[tempName] = [filePath]

except KeyboardInterrupt:
    # If the user interupted the checking process a report can still be obtained
    print("\nINTERRUPTED MOVING ONTO REPORT\n\n")


try:
    # Files that are the same
    sameFiles = {}

    # Gets all files that have multiple occurences
    for k in files:
        if len(files[k]) > 1:
            sameFiles[k] = files[k]

    # Gets a report writen
    report = WriteReport(dirToSort, sameFiles, saveSpace)
    
    if extractFile == "YES" or extractFile == "Y": # Check if a .txt file is being created
        print("\nEXPORTING REPORT")
        reportFileName = ("REPORT---" + dirToSort.replace("\\", "-") + ".txt").replace(":","")
        # Remove existing report for this directory to make room for this one
        if os.path.exists(reportFileName):
            os.unlink(reportFileName)
        # Creates a new report file
        exRep = open(reportFileName, "a+")
        for line in report:
            exRep.write(line + '\n')
        exRep.close()
        print("FINISHED EXPORTING REPORT\n\n\n")
            
    if printReport == "YES" or printReport == "Y": # Check if report is getting printed to console
        # Prints report to console
        print("\n\n\n PRINTING FULL REPORT \n")
        # Collects the output to one string making printing faster
        fullRep = ""
        for line in report:
            fullRep = fullRep + "\n" + line
        print(fullRep)
            
except KeyboardInterrupt:
    # If the user interrupts report writing the process stops and end message is shown
    print("\nSTOPPED WRITING REPORT")


# End Message
print("\n\nTHANK YOU FOR USING FILE CLEANER")
print("Created By Luke Fairs")
