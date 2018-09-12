import os, sys
import subprocess
print "cleaning files if they exist"

#os.system("rm Mchi-*.txt")
#masslist = ["Mchi-5p25_dMchi-0p5","Mchi-6p0_dMchi-2p0","Mchi-52p5_dMchi-5","Mchi-60_dMchi-20"]
masslist = ["Mchi-60_dMchi-20"]
lifelist = [100,1000]
#lifelist = [1,10,100,1000]
for mass in masslist:
	for life in lifelist:
		cmdx = "cmsRun python/tuplizer_cfg.py year=2017 inputFiles_load=data/iDM/{0}_{1}mm.txt outputFile=output/output_{0}_{1}mm.root".format(mass,life)
		print cmdx
		process = subprocess.Popen(cmdx,shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline,b''):
			print line
		process.stdout.close()
		process.wait()
