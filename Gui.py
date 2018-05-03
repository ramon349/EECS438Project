import sys
#account for difference between python 2 and python 7 
if sys.version_info.major < 3.0:
    import Tkinter as tk
    from Tkinter import filedialog as fd
    from Tkinter import simpledialog
    from Tkinter import *
else: 
    import tkinter as tk 
    from tkinter import filedialog as fd
    from tkinter import simpledialog
    from tkinter import *
from ssh_handler import SSHWrapper
import json


def gen_script(params):
    """
        params(dict): Dictionary containing parameters to place into the string.
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

class SlurmDialog(simpledialog.Dialog):
    """
        Class meant to create a series of text dialogs and gerate a simple bash script
    """
    questions = ["num_cores", "output_file", "mem_size", "num_nodes", "main_dir", "fun_handle", "user@host", "password"]
    entity = list()
    options = list()
    param_dict = dict()
    def body(self, master):
        """ Creates a list of text boxes used to retrive slurm parameters """
        for index,txt in enumerate(self.questions):
            Label(master, text=txt).grid(row=index)
            if txt is not "password":
                self.entity.append(Entry(master))
            else:
                self.entity.append(Entry(master,show='*')) 
            self.entity[index].grid(row=index,column=1)
        return self.entity[0]
    def apply(self):
        """ Retrives the text values provided by the users and populates a dictionary"""
        for e in self.entity:
            self.options.append(e.get())
        self.param_dict = {questions:ans for  questions,ans in zip(self.questions,self.options) } 
    def gen_ssh(self):
        """  Creates paramiko ssh client object using users parameters """
        return SSHWrapper(self.param_dict["user@host"],self.param_dict["password"])
    def addToDict(self,key,value):
        self.param_dict[key] = value
if __name__.endswith('__main__'):
    root = tk.Tk()
    diag = SlurmDialog(root)
    handler = diag.gen_ssh()
    handler.connect()
    count = handler.send_searcher(diag.param_dict['main_dir'])
    diag.addToDict('cases',str(count))
    script = gen_script(diag.param_dict)
    slurm_script = "slurm_script.slurm"
    root_dir = "/home/{user}/{script}".format(user=handler.user,script=slurm_script)
    with open(slurm_script, encoding="utf-8",mode='w') as f:
        f.write(script)
   # handler.exec_generator(list(d.get_results() ) )
    handler.execute_bash(slurm_script,root_dir)
    handler.client.close()
