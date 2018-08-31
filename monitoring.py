from ssh_handler import SSHWrapper 

x = SSHWrapper('rlc131@rider.case.edu','Omaiwa349!')
x.connect()
x.monitor_jobs()