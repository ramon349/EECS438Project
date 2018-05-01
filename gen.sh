echo "we made it"
module load python

cd ~/EECS438/project
echo "changed dirs" 
python3 generate_bash.py $1 $2 $3 $4
echo "hopefully ran"
