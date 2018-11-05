#!/usr/bin/bash
#SBATCH --partition=short       ### Partition (like a queue in PBS)
#SBATCH --job-name=sort      ### Job Name
#SBATCH --time=1-00:00:00       ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --nodes=1               ### Number of nodes needed for the job
#SBATCH --ntasks-per-node=7    ### Number of tasks to be launched per Node

module load easybuild intel/2017a Python/3.6.1
module load samtools/1.5


python adjustSoft.py -f "/projects/bgmp/shared/deduper/Dataset1.sam"

samtools sort "Dataset1_adjusted.sam" -o "Dataset1_sorted.sam"

python removeDupes.py -f "Dataset1_sorted.sam" -L