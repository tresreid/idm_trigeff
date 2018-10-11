import ROOT
import argparse
from ROOT import TMath
import csv
ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',type=str, required = True)
args= parser.parse_args()

def err_func(p0,p1,p2,p3,p4,x):
	return p2+p3*TMath.Erf((p4*x-p1)/p0)
 
def get_x98(p0,p1,p2,p3,p4,eff):
	max_eff98 = (p2+p3)*(eff/100.)
	closest= 100000
	x_val = 0
	for i in range(0,300):
		if abs(err_func(p0,p1,p2,p3,p4,i) - max_eff98) <closest:
			closest = abs(err_func(p0,p1,p2,p3,p4,i) - max_eff98)
			#print closest
			x_val = i
	return x_val

ifile = args.input
if ifile == 'test':
	f1 = ROOT.TFile("metTriggerEfficiency_recoil_monojet.root")
	ifile = "metTriggerEfficiency_recoil_monojet"
	ofile = "metTriggerEfficiency_recoil_monojet.pdf"
	hist_eff_met1 = f1.Get("efficiency")
	hist_eff_metp= hist_eff_met1.GetCopyPassedHisto()
	hist_eff_mett= hist_eff_met1.GetCopyTotalHisto()
	hist_eff_metp.Sumw2() 
	hist_eff_mett.Sumw2() 
	hist_eff_met =   hist_eff_metp.Clone("histeffmet")
	hist_eff_met.Divide(hist_eff_mett) 
	hist_eff_met.SetMaximum(1.1) 
	hist_eff_met.SetMinimum(-0.10) 
	test_func = f1.Get("efficiency_func")
	testpar0 = test_func.GetParameter(0)
	testpar1 = test_func.GetParameter(1)
	testpar2 = test_func.GetParameter(2)
	testpar3 = test_func.GetParameter(3)
	testpar4 = test_func.GetParameter(4)
	print "par 0", test_func.GetParameter(0)
	print "par 1", test_func.GetParameter(1)
	print "par 2", test_func.GetParameter(2)
	print "par 3", test_func.GetParameter(3)
	print "par 4", test_func.GetParameter(4)
	print "par 5", test_func.GetParameter(5)
	dy_range = 250
elif ifile == 'testz':
	f1 = ROOT.TFile("metTriggerEfficiency_recoil_monojet_zmm.root")
	ifile = "metTriggerEfficiency_recoil_monojet_zmm"
	ofile = "metTriggerEfficiency_recoil_monojet_zmm.pdf"
	hist_eff_met1 = f1.Get("efficiency")
	hist_eff_metp= hist_eff_met1.GetCopyPassedHisto()
	hist_eff_mett= hist_eff_met1.GetCopyTotalHisto()
	hist_eff_metp.Sumw2() 
	hist_eff_mett.Sumw2() 
	hist_eff_met =   hist_eff_metp.Clone("histeffmet")
	hist_eff_met.Divide(hist_eff_mett) 
	hist_eff_met.SetMaximum(1.1) 
	hist_eff_met.SetMinimum(-0.10) 
	test_func = f1.Get("efficiency_func")
	print "par 0", test_func.GetParameter(0)
	print "par 1", test_func.GetParameter(1)
	print "par 2", test_func.GetParameter(2)
	print "par 3", test_func.GetParameter(3)
	print "par 4", test_func.GetParameter(4)
	print "par 5", test_func.GetParameter(5)
	dy_range = 250
erf_met = ROOT.TF1("erf_met","[2]+[3]*TMath::Erf(([4]*x-[1])/[0])",110,1200) 
erf_met.SetParameters(50,132,3,0.55,0.75)
#erf_met.SetParameters(30,125,100,0.5)
#erf_met.SetParLimits(0,30,50)
#erf_met.SetParLimits(1,120,150)
#erf_met.SetParLimits(2,0,50)
#erf_met.SetParLimits(3,0.50,0.8)
#erf_met.SetParLimits(4,0.7,0.9)
erf_met.FixParameter(0,testpar2)
erf_met.FixParameter(1,testpar0)
erf_met.FixParameter(2,testpar4/10.)
erf_met.FixParameter(3,testpar3/10.)
erf_met.FixParameter(4,testpar1/100.)
#erf_met.FixParameter(0,80.2)
#erf_met.FixParameter(3,.602)
#
pp = ROOT.TCanvas("pp","pp",800,800)
t1 = ROOT.TText(0.5,0.5,"%s"%(ifile))
t1.SetTextAlign(22)
t1.SetTextSize(0.05)
t1.Draw()
pp.Print(ofile+"(")
pp.SetLogy(0)

ROOT.gStyle.SetStatW(.15)
ROOT.gStyle.SetStatH(.2)
ROOT.gStyle.SetOptStat()
##ROOT.gStyle.SetOptFit(0111)
#hist_eff_met.Fit("erf_met", "WR")
#met_chi = hist_eff_met.GetFunction("erf_met").GetChisquare() 
#met_p0 = hist_eff_met.GetFunction("erf_met").GetParameter(0) 
#met_p1 = hist_eff_met.GetFunction("erf_met").GetParameter(1) 
#met_p2 = hist_eff_met.GetFunction("erf_met").GetParameter(2) 
#met_p3 = hist_eff_met.GetFunction("erf_met").GetParameter(3) 
#met_p4 = hist_eff_met.GetFunction("erf_met").GetParameter(4) 
met_p0 =1
met_p1 =1
met_p2 =2
met_p3 =3
met_p4 =4
hist_eff_met.Draw("E1")
erf_met.Draw("SAME")
test_func.Draw("SAME")
#erf_met.Draw("SAME")
plateau = met_p3 + met_p2
x_val = get_x98(met_p0,met_p1,met_p2,met_p3,met_p4,98)
x_val100 = get_x98(met_p0,met_p1,met_p2,met_p3,met_p4,100)
print "parameters ", met_p0, met_p1, met_p2, met_p3
print "plateau = ", plateau, " x98= ", x_val
#trigpass_met = float(hist_fired_met.GetEntries())
#trigeffi_met = 100*trigpass_met/float(hist_total_events.GetEntries())
#
pp.Update()
#ps = pp.GetPrimitive("stats")
#ps.SetName("mystats")
#listolines = ps.GetListOfLines()
#line_p0 = ROOT.TLatex(0,0,"p0 = %.2f"%met_p0)
#line_p1 = ROOT.TLatex(0,0,"p1 = %.2f"%met_p1)
#line_p2 = ROOT.TLatex(0,0,"p2 = %.2f"%met_p2)
#line_p3 = ROOT.TLatex(0,0,"p3 = %.2f"%met_p3)
#line_chi = ROOT.TLatex(0,0,"chi2 = %.2f"%met_chi)
#line_plat = ROOT.TLatex(0,0,"plateau = %.4f"%plateau)
#line_x98 = ROOT.TLatex(0,0,"x98 = %s [GeV]"%x_val)
#line_x100 = ROOT.TLatex(0,0,"x100 = %s [GeV]"%x_val100)
#line_passeff = ROOT.TLatex(0,0,"pass = %s(%.2f%%)"%(trigpass_met,trigeffi_met))
#line_p0.SetTextFont(42)
#line_p0.SetTextSize(0.015)
#line_p1.SetTextFont(42)
#line_p1.SetTextSize(0.015)
#line_p2.SetTextFont(42)
#line_p2.SetTextSize(0.015)
#line_p3.SetTextFont(42)
#line_p3.SetTextSize(0.015)
#line_chi.SetTextFont(42)
#line_chi.SetTextSize(0.015)
#line_plat.SetTextFont(42)
#line_plat.SetTextSize(0.015)
#line_x98.SetTextFont(42)
#line_x98.SetTextSize(0.015)
#line_x100.SetTextFont(42)
#line_x100.SetTextSize(0.015)
#line_passeff.SetTextFont(42)
#line_passeff.SetTextSize(0.015)
#
#listolines.Add(line_p0)
#listolines.Add(line_p1)
#listolines.Add(line_p2)
#listolines.Add(line_p3)
#listolines.Add(line_chi)
#listolines.Add(line_plat)
#listolines.Add(line_x98)
#listolines.Add(line_x100)
#listolines.Add(line_passeff)
hist_eff_met.SetStats(0)
pp.Modified()
pp.Print(ofile+")")
pp.Clear()
with open('trigger_eff_table.csv',mode='a+') as table:
	table_writer = csv.writer(table, delimiter=',')
	table_writer.writerow([ifile,x_val,x_val100,plateau])
#
#
