#Neelie Shah

import subprocess as shelly# <---- da shell
import sys # <--- get the arguments

#get the args passed in
all_args = sys.argv

#gather all the tree sha's
def get_tree_shahs():
    tree_shahs = []
    for x in range(0, len(all_args)):
        if all_args[x] == "-t":
            tree_shahs.append(all_args[x+1])
    return tree_shahs

tree_shahs = get_tree_shahs()
output_branch_name = all_args[len(all_args)-1]

#commit the first tree
shell_output = shelly.run(["git","commit-tree", tree_shahs.pop(),"-m","alternative begin"], capture_output = True).stdout.decode('utf-8').strip().split("\n")[0]
# print(shell_output)


#add all the commit all the trees
for tree in tree_shahs:
    shell_output = shelly.run(["git","commit-tree", tree,"-p",shell_output,"-m","alternative follow up"], capture_output = True).stdout.decode('utf-8').strip().split("\n")[0]
    # print(shell_output)


shelly.run(["git","update-ref","refs/heads/"+output_branch_name,shell_output], capture_output = False)