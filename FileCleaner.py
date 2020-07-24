# Imports
import os

# Variables
files = {}  # k = fileName, v = [instances], near certain matches
posFiles = {} # k = fileName, v = [instances that are simular]


def Compare(fileA, fileB):
    fileSize = False
    names = False
    
    if os.path.basename(fileA) == os.path.basename(fileB):
        names = True

    
    
    if not names:
        filename, fileExtension = os.path.splitext(fileA)
        fileNameTemp = os.path.basename(fileA).rsplit(" - Copy", 1)
        if not fileNameTemp[0].endswith(fileExtension):
            fileANameNoCopy = fileNameTemp[0] + fileExtension
        else:
            fileANameNoCopy = fileNameTemp[0]
            
        filename, fileExtension = os.path.splitext(fileB)
        fileNameTemp = os.path.basename(fileB).rsplit(" - Copy", 1)
        if not fileNameTemp[0].endswith(fileExtension):
            fileBNameNoCopy = fileNameTemp[0] + fileExtension
        else:
            fileBNameNoCopy = fileNameTemp[0]
        
        if fileANameNoCopy == fileBNameNoCopy:
            names = True        

    
    if os.path.getsize(fileA) == os.path.getsize(fileB):
        fileSize = True
        

    # Return the closeness of the files; Certain (Near certain that they are the same), Pos (Most likely they are the same), No (Most likely different)
    if fileSize and names:
        return "Certain"
    elif names:
        return "Pos"
    else:
        return "No"


dirToSort = input("Input the Directory to Sort: ")

for root, subfolders, filenames in os.walk(dirToSort):
    for file in filenames:
        filePath = root + "\\" + file
        if files != {}:
            added = False
            for f in files:
                sim = Compare(filePath, files[f][0])
                if sim == "Certain":
                    files[f].append(filePath)
                    added = True
                elif sim == "Pos":
                    try:
                        posFiles[f].append(filePath)
                    except KeyError:
                        posFiles[f] = []
                        posFiles[f].append(filePath)
                    added = True
                    
            if added == False:
                try:
                    files[os.path.basename(filePath)].append(filePath)
                except KeyError:
                    files[os.path.basename(filePath)] = []
                    files[os.path.basename(filePath)].append(filePath)
        else:
            files[os.path.basename(filePath)] = []
            files[os.path.basename(filePath)].append(filePath)

sameFiles = {}

for k in files:
    if len(files[k]) > 1:
        sameFiles[k] = files[k]

if len(sameFiles) > 0:
    print("\nThese Files have the same (or similar) name and the same file size; meaning they are most likely the same file")
    for k in sameFiles:
        print(k)
        for v in sameFiles[k]:
            print("    " + v)
        print("")

if len(posFiles) > 0:
    print("\nThese Files have the same (or similar) name; meaning they are possibly the same file")
    for k in posFiles:
        print(k)
        print("    " + files[k][0])
        for v in posFiles[k]:
            print("    " + v)
        print("")
        
