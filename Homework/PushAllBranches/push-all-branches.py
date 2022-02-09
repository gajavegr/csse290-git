import sys
import subprocess

#push-all-branches.py --remote /tmp/testrepo

remoteRepo = str(sys.argv[2])
# print([hist[0] for hist in initial_history])
branchOutput = subprocess.getoutput("git branch").split()
for eachBranch in branchOutput[1:]:
  pushEachBranch = subprocess.getoutput(f"git push {remoteRepo} {eachBranch}")
  print(pushEachBranch)