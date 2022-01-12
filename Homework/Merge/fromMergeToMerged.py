
prefix_string = "#####"
current_conflict = open('input.txt','r')
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
# print(writing_lines)

out_file = open("testing.txt","w")
out_file.writelines(writing_lines)
out_file.close()