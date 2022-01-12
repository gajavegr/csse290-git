#!/usr/bin/python3
"""
Author: Austin Derrow-Pinion
Assignment: Merge
Date: 01/10/2017

This script merges two branches together. If there are any merge conflicts,
it resolves the conflict by using the current version as the correct version
and including it unmodified, but including the other version as comment in
the source code.

Parameters:
--use SHA this is the SHA of the commit that we want to use unmodified in case
    of conflicts
--commentify SHA this is the SHA of the commit we want to insert as comments
    only
--branch NAME this is the name of the branch where the output will go
--prefix STRING this is the prefix that will make a line a comment. So we'd use
    "// " in C++ or "# " in Ruby.
"""

import sys
import subprocess

# exit if proper values aren't passed
if len(sys.argv) < 5:
  print("Must enter the following parameters:\n\t--use SHA\n\t-commentify SHA" +
    "\n\t--branch NAME\n\t--prefix STRING\n")
  exit(1)

# first clean any uncommitted changes
subprocess.getoutput("git reset --hard")

# checkout -use commit
subprocess.getoutput("git checkout {}".format(sys.argv[2]))

# try to merge
subprocess.getoutput("git merge {}".format(sys.argv[4]))

# check for any conflicting files
conflicts = subprocess.getoutput("git diff --name-only --diff-filter=U").split()

# resolve each conflict
for conflict in conflicts:
  output = []
  keep = []
  flag_keep = False
  flag_commentify = False

  # make a list of lines to output in final file
  with open(conflict, 'r') as file:
    for line in file:
      if line.startswith("<<<<<<<"):
        # beginning of -use file's contents
        flag_keep = True
        flag_commentify = False
      elif line.startswith("======"):
        # beginning of -commentify file's contents
        flag_keep = False
        flag_commentify = True
      elif line.startswith(">>>>>>>"):
        # end of -commentify file's contents
        flag_keep = False
        flag_commentify = False

        # add lines to keep into the output after the commented lines
        for line_to_keep in keep:
          output.append(line_to_keep)
        keep = []
      elif flag_keep:
        keep.append(line)
      elif flag_commentify:
        output.append("{}{}".format(sys.argv[8], line))

  # rewrite the file with the commented source code
  with open(conflict, 'w') as file:
    for line in output:
      file.write(line)

# tell git the conflicts have been resolved
subprocess.getoutput("git add .")

# switch to output branch
subprocess.getoutput("git checkout -b {}".format(sys.argv[6]))

# commit finished auto-merge
subprocess.getoutput("git commit -m 'auto-merge-with-comments'")