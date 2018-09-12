import os, sys
import subprocess
print "cleaning files if they exist"

os.system("rm Mchi-*.txt")
masslist = ["Mchi-5p25_dMchi-0p5","Mchi-6p0_dMchi-2p0","Mchi-52p5_dMchi-5","Mchi-60_dMchi-20"]
lifelist = [1,10,100,1000]
for mass in masslist:
	if "Mchi-5p25_dMchi-0p5" in mass or "Mchi-6p0_dMchi-2p0" in mass:
		user = 'as2872'
		for life in lifelist:
			cmdx = "xrdfs root://cmseos.fnal.gov ls /store/user/{0}/iDM/AOD_Samples/{1}/lifetime_{2}mm >> {1}_{2}mm.txt".format(user,mass,life) 
			print cmdx
			process = subprocess.Popen(cmdx,shell=True, stdout=subprocess.PIPE)
			for line in iter(process.stdout.readline,b''):
				print line
			process.stdout.close()
			process.wait()

	user = 'mreid'
	for life in lifelist:
		cmdx = "xrdfs root://cmseos.fnal.gov ls /store/user/{0}/iDM/AOD_Samples/{1}/lifetime_{2}mm >> {1}_{2}mm.txt".format(user,mass,life) 
		print cmdx
		process = subprocess.Popen(cmdx,shell=True, stdout=subprocess.PIPE)
		for line in iter(process.stdout.readline,b''):
			print line
		process.stdout.close()
		process.wait()
		

		cms =  "sed -i -e 's#^#root://cmseos.fnal.gov/#' {0}_{1}mm.txt".format(mass,life)
		os.system(cms)
		cmsdel = "sed -i '/MINIAOD/d' {0}_{1}mm.txt".format(mass,life)
		os.system(cmsdel)
