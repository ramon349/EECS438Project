#!/bin/sh
#SBATCH -c 10
#SBATCH --output=10.txt
#SBATCH --mem=10gb
#SBATCH -A eecs438
#SBATCH --Array=0-4%10


interestDir=/home/rlc131/EECS438/
cd $interestDir
module load matlab
shopt -s nullglob 
patientArray=(*/)
matlab -r "  fun = @pokemon;  fun(${patientArray[${SLURM_ARRAY_TASK_ID}]});"
quit
