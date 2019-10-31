import subprocess

comando = 'sudo apt update'
#ejecucion = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
#print(ejecucion.stdout)
p = subprocess.Popen(["sudo", "apt", "update"], stdout=subprocess.PIPE, universal_newlines=True)
while True:
    line = p.stdout.readline()
    if not line:
        break
    print(line)
print("Fin primer comando")