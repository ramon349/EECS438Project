def gen_script(params):
    """ Creates a bash script by pluggin in information from params .
        Args:
            params(dict): Dictionary containing parameters to place into the bash script template.
    """
    template ="""#!/bin/sh
#SBATCH -c {param[num_cores]}
#SBATCH --output={param[output_file]}_%A_%a.txt
#SBATCH --mem={param[mem_size]}gb
#SBATCH -A eecs438
#SBATCH --array=0-{param[cases]}%{param[num_nodes]}
module load matlab
interestDir={param[main_dir]} 
cd "$interestDir"
echo "Hello we are interested in the path: ${{interestDir}}"
shopt -s nullglob
patientArray=(*/)
matlab -r "addpath('/home/rlc131/'); setup(); fun = @{param[fun_handle]};  fun('${{patientArray[${{SLURM_ARRAY_TASK_ID}}]}}'); " """
    template = template.format(param=params)
    return template

    