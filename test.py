import subprocess

# Run the command: where.exe xtb on win32 and which xtb on linux 
# and get the path to the xtb executable
#
#* Get the path to the xtb executable
xtb_path = subprocess.run(["where.exe", "xtb"], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
xtb_path = xtb_path.strip()
