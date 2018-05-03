import paramiko
import socket
import getpass
import time 
import os
from paramiko.py3compat import input


class SSHWrapper():
    def __init__(self,logIn,password):
        """  Creates sshWrapper instnace with user specifications needed to make ssh connection"""
        (self.user,self.host) = logIn.split('@')
        self.password = password
    def connect(self):
        """ Uses user information to connect to the hpc server """
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(self.host,port=22,username=self.user,password=self.password)
    def send_searcher(self,path):
        """ determines how many  subdirectories are present in a specified path """
        ftp =self.client.open_sftp()
        count =0
        for e in ftp.listdir(path):
            info = str(ftp.lstat(path+e)).split()[0]
            if 'd' in info: 
                count = count +1
                print(e)
        return count
    def execute_bash(self,filename,path):
        filler =  95
        ftp = self.client.open_sftp()
        response = ftp.put(filename,path)
        self.client.exec_command("dos2unix {f}".format(f=filename))
        py_command = "sbatch {f} ".format(f=filename)
        (std_in,std_out,std_err) = self.client.exec_command(py_command)
        time.sleep(1)
        for e in std_out:
            print(e)
        print("----------------")
        while True :
            print(" Our Program is still running")
            (_,std_out,_) = self.client.exec_command("squeue -u {user}".format(user=self.user))
            if len(list(std_out)) ==1:
                break
            time.sleep(60)