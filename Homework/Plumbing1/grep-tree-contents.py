import sys
import subprocess
import re
import logging

matchingLines = []
inputSha = str(sys.argv[2])
# treeSha = "7d3b207"
#7d3b207
inputString = str(sys.argv[4])
# print(arguments)

def grepTreeContents(treeSha,searchString,currentFolder):
    blobsAndTrees = subprocess.run(["git","cat-file","-p",f"{treeSha}"],stdout=subprocess.PIPE).stdout.decode('utf-8').strip().split("\n")
    for line in blobsAndTrees:
        # if i == 0:
        result = re.search(r"\d{6}\s(blob|tree)\s([a-z0-9]{40})\s+(.*)",line)
        fileType = result.group(1)
        eachSha = result.group(2)
        filename = result.group(3)
        if (fileType == "blob"):
            grepCommand = ["grep",f"{searchString}",f"{currentFolder}{filename}"]
            grepResult = subprocess.run(grepCommand,stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
            if len(grepResult) > 0:
                logging.debug(f"{filename}:")
                for matchingLine in grepResult.split("\n"):
                    logging.debug(matchingLine)
                    matchingLines.append(matchingLine)
        else:
            grepTreeContents(eachSha,searchString,f"{filename}/")

def main():
    level = logging.INFO
    fmt = '[%(levelname)s] - %(message)s'
    logging.basicConfig(level=level, format=fmt)
    grepTreeContents(inputSha,inputString,'')
    logging.info('\n'.join(matchingLines))

if __name__ == '__main__':
    main()