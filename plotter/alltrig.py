import subprocess
import os,sys

os.system("rm trigger_eff_table.csv")
os.system("rm trigger_eff_table.txt")
os.system("rm trigeff.root")
os.system('echo "name,x98,x100,plateau,number passing trigger, trigger efficiency in % (from all events) " > trigger_eff_table.csv')


masslist = ["Mchi-5p25_dMchi-0p5","Mchi-6p0_dMchi-2p0","Mchi-52p5_dMchi-5","Mchi-60_dMchi-20"]
lifelist = [1]#,10,100,1000]
for mass in masslist:
        for life in lifelist:
                cmdx = "python trig.py -i {0}_{1}mm".format(mass,life)
                print cmdx
                process = subprocess.Popen(cmdx,shell=True, stdout=subprocess.PIPE)
                for line in iter(process.stdout.readline,b''):
                        print line
                process.stdout.close()
                process.wait()
