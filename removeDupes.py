#!/usr/bin/env python3
import os
import argparse
import sys

def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", help="Input sam file", type = str, required = True)
        parser.add_argument("-p", "--paired", help="Specify if experiment was paired end", action = "store_true")
        parser.add_argument("-u", "--umi", help="Designates file that contains list of UMIs", type = str, required = False, default = "STL96.txt")
        parser.add_argument("-F", "--First", help="Keep first duplicate encountered", action = "store_true")
        parser.add_argument("-L", "--Last", help="Keep last duplicate encountered", action = "store_true")
        return parser.parse_args()


def getInfo(samRead):
    UMI = samRead[0][-8:]
    bflag = samRead[1]
    pos = samRead[3]
    chrom = samRead[2]
    Ident = bflag + "-" + UMI + "-" + pos + "-" + chrom
    return(Ident)

args = get_arguments()
if args.paired == True:
    sys.exit("Paired end deduplicating not developed yet.")
inputFile = args.file
outputFile = os.path.basename(inputFile)[:-4] + "_deDuped.sam"
outObj = open(outputFile, "a+")
inputObj = open(inputFile, "r")

uniqReads = {}
duplicates = 0
init = True

#Initiate dictionary with this loop, negating all header lines
while init == True:
    line = inputObj.readline()
    if line == "":
        print("File is empty, check input")
    if line.startswith('@'):
        outObj.write(line)
        continue
    line = line.strip().split()
    uniqIdent = getInfo(line)
    uniqReads[uniqIdent] = line
    init = False

while True:
    line = inputObj.readline()
    if line == "":
        break
    if line.startswith('@'):
#         outObj.write(line)
        continue
    line = line.strip().split()
    uniqIdent = getInfo(line)
    if uniqIdent in uniqReads.keys():
        if args.Last == True:
            uniqReads[uniqIdent] = line
        if args.First == True:
            pass
        duplicates += 1
    if uniqIdent not in uniqReads.keys():
        uniqReads[uniqIdent] = line  
        
#This for loop is used to replace previous start position from read that is being written
for read in uniqReads.values():
    prevStart = read[len(read) - 1].split(":")
    prevStart = prevStart[len(prevStart) - 1]
    read[3] = prevStart
    del read[-1]
    read = "\t".join(read)
    read = read + "\n"
    outObj.write(read)
print("Number of duplicates removed: ", duplicates)
#Find what duplicate was passed into argparse
for arg in vars(args):
    if getattr(args, arg) == True:
        dupKept = arg
print("Duplicate kept: ", dupKept)
outObj.close()
inputObj.close()

