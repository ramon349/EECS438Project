import paramiko
import socket
import getpass
import time 
import os
from paramiko.py3compat import input


class SSHWrapper():
    def __init__(self,logIn,password):
        (self.user,self.host) = logIn.split('@')
        self.password = password
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(self.host,port=22,username=self.user,password=self.password)
    def exec_generator(self,param_list):
        py_command ="bash ./gen.sh {0} {1} {2} {3} >> athing.txt".format(*param_list)
        (std_in,std_out,std_err) =self.client.exec_command(py_command) 
        print(std_out)
    def send_searcher(self,path):
        ftp =self.client.open_sftp()
        count =0
        for e in ftp.listdir(path):
            info = str(ftp.lstat(path+e)).split()[0]
            if 'd' in info: 
                count = count +1
                print(e)
        return count 
