
import sys 


class 


if __name__ == "__main__":
    elements = sys.argv[1:]
    dummy="""#!/bin/sh
#SBATCH -c {num_cores}
#SBATCH --output={output_file}.txt
#SBATCH --mem={mem_size}gb
#SBATCH -A eecs438
#SBATCH --Array=0-{cases}%{num_nodes}

interestDir={main_dir}
cd $interestDir
module load matlab
shopt -s nullglob 
patientArray=(*/)
matlab -r "  fun = @{fun_handle};  fun(${patientArray[${SLURM_ARRAY_TASK_ID}]);"
quit""".format(*elements)
    with open("test.bash",'w') as f: 
        f.write(dummy)
