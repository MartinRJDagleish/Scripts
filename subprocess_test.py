import subprocess

# subprocess.run([f"echo Test{i}" for i in range(3)], shell=True, check=True, stdout=subprocess.PIPE)
# my_list = [["echo", "test1"], ["echo", "test2"]]

temp1_path = "..\\temp1"
namespace = "myfile"
import os

cwd = os.getcwd()

my_list = [
    ("copy " + f"{temp1_path}\\{namespace}.{ext} " + cwd).split()
    for ext in ("out", "molden", "xtbopt.trj.xyz", "xtbopt.xyz")
]

[subprocess.run(cmd, stdout=subprocess.PIPE, shell=True, check=True) for cmd in my_list]

# subprocess.run(my_list, shell=True, check=True)
