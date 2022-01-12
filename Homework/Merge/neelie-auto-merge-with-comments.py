#Neelie Shah

import subprocess as shelly# <---- da shell
import sys # <--- get the arguments

#get the args passed in
all_args = sys.argv

#gather all the inputs
def get_tree_shahs():
    use_shah = ""
    commit_shah = ""
    branch_name = ""
    prefix_string = ""
    for x in range(0, len(all_args)):
        if all_args[x] == "--use":
            use_shah = all_args[x+1]
        elif all_args[x] == "--commitify":
            commit_shah = all_args[x+1]
        elif all_args[x] == "--branch":
            branch_name = all_args[x+1]
        elif all_args[x] == "--prefix":
            prefix_string = all_args[x+1]

    return [use_shah, commit_shah, branch_name, prefix_string]

use_shah = get_tree_shahs()[0]
commit_shah = get_tree_shahs()[1]
branch_name = get_tree_shahs()[2]
prefix_string = get_tree_shahs()[3]

print(use_shah)
#first step as per Buffalo's recommendation:
shelly.getoutput("git reset --hard")

#git checkout the useShah
shelly.getoutput("git checkout "+ use_shah)

# merge committify shah
shelly.getoutput("git merge "+ commit_shah)

#get conflicts from merge using special command:
merge_conflicts = shelly.getoutput("git diff --name-only --diff-filter=U").strip().split()
# print(merge_conflicts)

#go through lines in merge_conflict and add as comments:
for x in range(0, len(merge_conflicts)):
    current_conflict = open(merge_conflicts[x])
    conflict_lines = current_conflict.readlines()
    current_conflict.close()
    writing_lines = []
    # startKeepingLines = False
    # startCommentingLines = False
    y = 0
    while y  < len(conflict_lines):
        line = conflict_lines[y]
        # startKeepingLines = True
        print(line)
        #get all lines to keep
        if "<<<<<<<" in  line:
            y+=1
            while "=======" not in line:
                line = conflict_lines[y]
                if "=======" in line:
                    break
                comment_line = prefix_string+line
                print(f"appending commented line: {y}: {comment_line}")
                writing_lines.append(comment_line)
                y+=1
        #get all lines to comment
        elif "=======" in  line:
            #switch to commenting
            y+=1
            while ">>>>>>>" not in line:
                line = conflict_lines[y]
                if ">>>>>>>" in line:
                    y+=1
                    break
                print(f"appending line to keep: {y}: {line}")
                writing_lines.append(line)
                y+=1
        #add lines that are not merge conflicts
        else:
            line = conflict_lines[y]
            print(f"appending line to keep: {y}: {line}")
            writing_lines.append(line)
            y+=1
            # startKeepingLines = False
            # startCommentingLines = True
        # y+=1

    #write new merged changes to file with merge conflicy
    out_file = open(merge_conflicts[x],"w")
    out_file.writelines(writing_lines)
    out_file.close()

# add all the merged/resolved files
shelly.getoutput("git add .")

# switch to desired branch
shelly.getoutput("git checkout -b "+branch_name)

# commit resolved merge
shelly.getoutput("git commit -m \"auto-merge-with-comments tool\"")