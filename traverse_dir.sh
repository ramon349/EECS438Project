#!/bin/sh 
#SBATCH -c 1
#SBATCH --mem=2gb 
#SBATCH -A eecs438 
#SBATCH -o setup_log.txt


mainDir=$1 
shopt -s nullglob
cd "$mainDir"
subDirs=(*/)
num_elements=${#array[@]}


echo "CD to $mainDir"
for subDir in *; do 
  echo "Looking at path $subDir"
done 
