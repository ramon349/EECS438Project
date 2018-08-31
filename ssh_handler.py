import paramiko
import socket
import getpass
import time 
import os
import sys
from paramiko.py3compat import input

class SSHWrapper():
    def __init__(self,logIn,password):
        """  Creates sshWrapper instnace with user specifications needed to make ssh connection"""
        self.connected = False
        if self.validate(logIn):
            (self.user,self.host) = logIn.split('@')
            self.password = password
        else:
            #need to throw exception
            print('Error')
            raise Exception(" Illegal argument: loginInfo should be: username@service.stuff"  )
    def validate(self,login):
        """ Check if the supplied login credentials are in the expected format
            Args: 
                login(str): Log in crentials  should follow username@service.stuff format. 
        """
        if '@' in login:
            return True 
        else: 
            return False

    def connect(self):
        """ Uses user information to connect to the hpc server """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(self.host,port=22,username=self.user,password=self.password)
        self.connected = True
    
    def disconnect(self):
        """ """
        self.client.close()
        self.connected = False

    def send_searcher(self,path):
        """ determines how many  subdirectories are present in a specified path 
            Args: 
                path(str): absolute path pointing to where data of interest is located.
        """
        ftp =self.client.open_sftp()
        count =0
        for e in ftp.listdir(path):
            info = str(ftp.lstat(path+e)).split()[0]
            if 'd' in info: 
                count = count +1
                print(e)
        return count

    def transmit_file(self,filename,path):
        """  transmit bash code to HPC server and execute it with sbatch. Code cheks every minute to check if script 
             is complete. 
            Args: 
                filename(str): Name of file to be executed. 
                path(str): Absolute to store/execute the file.  
        """
        ftp=self.client.open_sftp()
        response=ftp.put(filename,path)
        if sys.platform == 'win32':
             self.client.exec_command("dos2unix {f}".format(f=filename))

    def execute_bash(self,filename):
        """  Execute the bash file specified by filename in HPC using sbatch.
            Args: 
                filename(str): Name of file to be executed. 
        """
        py_command = "sbatch {f} ".format(f=filename)
        (std_in,std_out,std_err) = self.client.exec_command(py_command)
        time.sleep(1)
        for e in std_out:
            print(e)
        print("----------------")
        while True : #infinite loop to check if slurm jobs are still running
            print(" Our Program is still running")
            (_,std_out,_) = self.client.exec_command("squeue -u {USER}".format(USER=self.user))
            if len(list(std_out)) ==1:
                break
            time.sleep(60)
    def monitor_jobs(self):
            py_command = "squeue -u {USER}".format(USER=self.user)
            while True: 
                print(" Our Programs are still running")
                (_,std_out,_) = self.client.exec_command("squeue -u {USER}".format(USER=self.user))
                consumed_std_out = list(std_out)
                if len(consumed_std_out) ==1:
                    break
                else: 
                    for job in consumed_std_out:
                        print(job)
                time.sleep(60)

    def get_file(self,filename,path):
        """ Using sftp connect to the server and obtain the file of interest. 
            Args: 
                filename(str): name of file to search for
                path(str): absolute path where file should be contained
        """
        ftp = self.client.open_sftp()
        cwd = "{PATH}\\{NAME}".format(PATH=os.getcwd(),NAME=filename)
        fileOfInterest = "{F}/{NAME}".format(F=path,NAME=filename)
        ftp.get(fileOfInterest,cwd)
    
    def __str__(self):
        return "user:{USER}@{HOST} connected:{STATUS}".format(USER=self.user,HOST=self.host,STATUS=self.connected)