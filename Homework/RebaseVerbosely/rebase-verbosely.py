import sys
import subprocess

rebaseSha = str(sys.argv[2])
initial_history = [[message.split(" ")[0], " ".join(message.split(" ")[1:])] for message in subprocess.getoutput("git log --oneline").split('\n')]
# print([hist[0] for hist in initial_history])
print(f"calling git rebase {rebaseSha}")
print(subprocess.getoutput(f"git rebase {rebaseSha}"))
currentHistory = subprocess.getoutput("git log --oneline").split('\n')
for message in currentHistory:
    currentSha = message.split(" ")[0]
    currentMessage = " ".join(message.split(" ")[1:])
    if currentSha == rebaseSha:
        print(f"{currentSha} is the new base: {currentMessage}")
        break
    for commitSha, commitMessage in initial_history:
        if currentMessage == commitMessage:
            print(f"{commitSha} becomes {currentSha}:{currentMessage}")
            break 
