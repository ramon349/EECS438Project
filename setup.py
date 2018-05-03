from cx_Freeze import setup, Executable
import os 
os.environ['TCL_LIBRARY']= r"C:\Users\ramon\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6"
os.environ['TK_LIBRARY'] = r"C:\Users\ramon\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6"
base = None
executables = [Executable("Gui.py", base=base)]

packages = ["tkinter"]
includes =[]
include_files = [r"C:\Users\ramon\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",  r"C:\Users\ramon\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]
setup(
    name = "<any name>",
    options =  {"build_exe": {"includes": includes, "packages": ['os',"bcrypt","cffi",'paramiko','idna'],"include_files": include_files}},
    version = "<any number>",
    description = '<any description>',
    executables = executables,
    icon = "futurama_ico.ico"
)