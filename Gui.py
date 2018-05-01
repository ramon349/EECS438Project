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
    dummy="""#!/bin/sh
#SBATCH -c {param[num_cores]}
#SBATCH --output={param[output_file]}.txt
#SBATCH --mem={param[mem_size]}gb
#SBATCH -A eecs438
#SBATCH --Array=0-{param[cases]}%{param[num_nodes]}


interestDir={param[main_dir]}
cd $interestDir
module load matlab
shopt -s nullglob 
patientArray=(*/)
matlab -r "  fun = @{param[fun_handle]};  fun(${{patientArray[${{SLURM_ARRAY_TASK_ID}}]}});"
quit""".format(param=params)
    return dummy

class SlurmDialog(simpledialog.Dialog):
        questions = ["num_cores","output_file","mem_size","num_nodes","main_dir","fun_handle","user@host","password"]
        entity = list()
        options = list()
        param_dict = dict() 
        def body(self,master):
            for index,txt in enumerate(self.questions):
                Label(master,text=txt).grid(row=index)
                if txt is not "password":
                    self.entity.append(Entry(master))
                else:
                    self.entity.append(Entry(master,show='*')) 
                self.entity[index].grid(row=index,column=1)
            return self.entity[0]
        def apply(self):
            for e in self.entity:
                self.options.append(e.get())
            self.param_dict = {questions:ans for  questions,ans in zip(self.questions,self.options) } 
        def gen_ssh(self):
            return SSHWrapper(self.param_dict["user@host"],self.param_dict["password"])
        def addToDict(self,key,value):
            self.param_dict[key] = value
if __name__ == "__main__":
    root = tk.Tk()
    diag = SlurmDialog(root)
   # script = gen_script(diag.param_dict)
    handler = diag.gen_ssh()
    handler.connect()
    count = handler.send_searcher(diag.param_dict['main_dir'])
    diag.addToDict('cases',str(count))
    script = gen_script(diag.param_dict)
    with open("test.bash",'w') as f:
        f.write(script)
   # handler.exec_generator(list(d.get_results() ) )
    handler.client.close()
