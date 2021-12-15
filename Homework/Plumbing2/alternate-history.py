import sys
import subprocess

shasList = [str(sys.argv[2]),str(sys.argv[4]),str(sys.argv[6])]
branchName = str(sys.argv[8])W

parent = subprocess.run(["git", "commit-tree", shasList[0], "-m", "alternative branch"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip().split("\n")
parent = subprocess.run(["git", "commit-tree", shasList[0], "-m", "alternative begin"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
parent = subprocess.run(["git", "commit-tree", shasList[1], "-p", parent, "-m", "alternative followup"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
parent = subprocess.run(["git", "commit-tree", shasList[2], "-p", parent, "-m", "alternative followup"], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

refPath = f"refs/heads/{branchName}"
subprocess.run(["git","update-ref",refPath,parent],stdout=subprocess.PIPE)