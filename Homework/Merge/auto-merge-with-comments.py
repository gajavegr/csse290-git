import sys
import subprocess

useBranch = str(sys.argv[2])
commitifyBranch = str(sys.argv[4])
branchName = str(sys.argv[6])
prefixName = str(sys.argv[8])

subprocess.getoutput("git reset --hard")
subprocess.getoutput(f"git checkout {useBranch}")
subprocess.getoutput(f"git merge {commitifyBranch}")
mergeConflicts = subprocess.getoutput("git diff --name-only --diff-filter=U").strip().split()

for i,mergeConflict in enumerate(mergeConflicts):
    summarizeLines = []
    resolvedLines = []
    with open(mergeConflict,'r') as mergeDoc:
        currentSpecialChar = ""
        #should be a list of 3 nums: [<index,=index,>index]
        currentMergeRange = []
        for j,line in enumerate(mergeDoc):
            if currentSpecialChar == ">":
                summarizeLines.append(currentMergeRange)
                currentMergeRange = []
                currentSpecialChar = ""
            if line.find("<<<<<<<") != -1:
                currentSpecialChar = "<"
                currentMergeRange.append(j)
            elif line.find("=======") != -1:
                currentSpecialChar = "="
                currentMergeRange.append(j)
            elif line.find(">>>>>>>") != -1:
                currentSpecialChar = ">"
                currentMergeRange.append(j)
                
            

        docLine = mergeDoc.readlines()
        for j,specialLine in enumerate(summarizeLines):
            if j == 0:
                if specialLine[0] != 0:
                    rawLines = [rawLine for rawLine in docLine[0:specialLine[0]-1]]
                    resolvedLines+=rawLines
                
            comm = specialLine[0]
            sep = specialLine[1]
            keep = specialLine[2]
            #adding lines to comment
            commLines = [prefixName + lineToComment for lineToComment in docLine[comm+1:sep-1]]
            resolvedLines += commLines
            #adding lines to keep
            keepLines = [lineToComment for lineToComment in docLine[sep+1:keep-1]]
            resolvedLines += keepLines
            if j == len(summarizeLines)-1:
                if specialLine[2] != len(docLine)-1:
                    rawLines = [rawLine for rawLine in docLine[specialLine[2]+1:len(docLine)-1]]
                    resolvedLines += rawLines
    # print(resolvedLines)
    with open(mergeConflict,'w') as mergedDoc:
            mergedDoc.writelines(resolvedLines)
                

# add all the merged/resolved files
subprocess.getoutput("git add .")

# switch to desired branch
subprocess.getoutput(f"git checkout -b {branchName}")

# commit resolved merge
subprocess.getoutput("git commit -m \"auto-merge-with-comments tool\"")