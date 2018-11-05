#!/usr/bin/env python3
# Ignore Insertions
# Account for S's N's, D's and M's
import re
import sys
import os
import argparse

def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument("-f", "--file", help="Input sam file", type = str, required = True)
        return parser.parse_args()

args = get_arguments()
file = args.file
# file = "/projects/bgmp/shared/deduper/Dataset1.sam"
outputFile = os.path.basename(file)[:-4] + "_adjusted.sam"

with open(file, "r") as sam, open(outputFile, "a+") as adjust:
    for line in sam:
        if line.startswith("@"):
            adjust.write(line)
            continue
        line = line.strip().split()
        #left Start
        pos = int(line[3])
        #right Start
        posE = pos
        cigar = line[5]
        # Find integer associated with soft clipping
        clip = re.findall('^\d+S', cigar)
        
        deletion = re.findall('\d+D', cigar)
        match = re.findall('\d+M', cigar)
        clipE = re.findall('\d+S$', cigar)
        ens = re.findall('\d+N', cigar)
        if ((int(line[1]) & 16) != 16):
        #Soft clipping/indels for forward strand  
            line.append("OS:Z:" + str(pos))
            if clip:               
                clip = clip[0][:-1]
                pos -= int(clip)
                line[3] = str(pos)
            elif not clip:
                pass             
        elif ((int(line[1]) & 16) != 0):
        #Soft clipping/indels for reverse strand
            line.append("OS:Z:" + str(posE))
            if deletion:
                for i in range(len(deletion)):
                    posE += int(deletion[i][:-1])
            else:
                pass

            if match:
                for m in range(len(match)):
                    posE += int(match[m][:-1])
            else:
                pass

            if clipE:
                for e in range(len(clipE)):
                    posE += int(clipE[e][:-1])
            else:
                pass
            if ens:
                for n in range(len(ens)):
                    posE += int(ens[n][:-1])
            else:
                pass
            line[3] = str(posE)
        line = "\t".join(line)
        line += "\n"
        adjust.write(line)
sam.close()
adjust.close()
# print(outputFile)

