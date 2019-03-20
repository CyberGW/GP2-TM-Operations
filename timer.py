import subprocess
import timeit

subprocess.run("gp2 program.gp2 ; cd /tmp/gp2 ; make", shell = True)
print ( timeit.timeit ( 'subprocess.run("cd /tmp/gp2 ; ./gp2run ~/Desktop/graph.host", shell = True)' , setup = 'import subprocess', number = 1000) / 1000 )
