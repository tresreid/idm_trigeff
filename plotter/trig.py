import ROOT
import argparse
from ROOT import TMath
import csv
ROOT.gROOT.SetBatch(True)

parser = argparse.ArgumentParser()
parser.add_argument('-i','--input',type=str, required = True)
args= parser.parse_args()

def err_func(p0,p1,p2,p3,x):
	return p2+p3*TMath.Erf((x-p1)/p0)
 
def get_x98(p0,p1,p2,p3,eff):
	max_eff98 = (p2+p3)*(eff/100.)
	closest= 100000
	x_val = 0
	for i in range(0,300):
		if abs(err_func(p0,p1,p2,p3,i) - max_eff98) <closest:
			closest = abs(err_func(p0,p1,p2,p3,i) - max_eff98)
			#print closest
			x_val = i
	return x_val
metnomu = True
runeff = False
ifile = args.input
if ifile == 'test':
	f1 = ROOT.TFile("~/nobackup/metnomustudy/output_Mchi-60_dMchi-20_1mm.root")
	ofile = "output_test.pdf"
	t1 = f1.Get("TRIG_dsa2/trigEffiForMetTrack")
	t2 = f1.Get("TRIG_dsa2/trigEffiForMetTrackFired")
	t3 = f1.Get("TRIG_dsa2/trigEffiForMetTrackTotal")
	if metnomu:
		tmetnomu = f1.Get("TRIG_metnomustudy/metnomustudy")
		ofilemnm = "output_testmnm.pdf"
	dy_range = 250
else:
	ofile = "output/trigeff_%s.pdf"%ifile
	f1 = ROOT.TFile("~/nobackup/metnomustudy/output_%s.root"%ifile)
	t1 = f1.Get("TRIG_dsa2/trigEffiForMetTrack")
	t2 = f1.Get("TRIG_dsa2/trigEffiForMetTrackFired")
	t3 = f1.Get("TRIG_dsa2/trigEffiForMetTrackTotal")
	if metnomu:
		tmetnomu = f1.Get("TRIG_metnomustudy/metnomustudy")
		ofilemnm = "output/metnomu_%s.pdf"%ifile
if runeff:
	use_dybins = False
	#dynamic_ranges = [[180,190,190,190],[240,240,220,180],[250,195,250,180],[198,200,200,230]]
	#dynamic_good = [[F,F,F,],[240,240,220,200],[250,200,250,200],[198,200,200,230]]
	dynamic_ranges = [[250,250,250,250],[240,240,250,250],[250,250,250,250],[250,250,250,250]]
	#dynamic_rangeslow = 100 #[[100,0,0,0],[0,0,0,0],[0,0,100,0],[0,0,0,0]]
	renamemass = ['five','six','fifty','sixty']
	renamelife = ['xmm','xxmm','xxxmm','xxxxmm']
	rename = ''
	if 'Mchi-60' in ifile:
		massdy_range = dynamic_ranges[3]
		rename += renamemass[3]
	if 'Mchi-52p5' in ifile:
		massdy_range = dynamic_ranges[2]
		rename += renamemass[2]
	if 'Mchi-6p0' in ifile:
		massdy_range = dynamic_ranges[1]
		rename += renamemass[1]
		if '1000mm' in ifile:
			use_dybins = True
	if 'Mchi-5p25' in ifile:
		use_dybins = True
		rename += renamemass[0]
		massdy_range = dynamic_ranges[0]
	if '1mm' in ifile:
		dy_range = massdy_range[0]	
		rename += renamelife[0]
	if '10mm' in ifile:
		dy_range = massdy_range[1]	
		rename += renamelife[1]
	if '100mm' in ifile:
		dy_range = massdy_range[2]	
		rename += renamelife[2]
	if '1000mm' in ifile:
		dy_range = massdy_range[3]	
		rename += renamelife[3]
	
	hist_total_events = ROOT.TH1F("total","tot",3,0,3)
	for entry in t3:
		total =entry.sel
		hist_total_events.Fill(total) 
	
	xbins = [2.7**(i/10.0) for i in range(0,57,1)]
	if use_dybins:
		hist_sel_met = ROOT.TH1F("histselmet","Met",75,0,300)
		hist_sel_metnomu = ROOT.TH1F("histselmetnomu","Met nomu",75,0,300)
	else:
		hist_sel_met = ROOT.TH1F("histselmet","Met",100,0,300)
		hist_sel_metnomu = ROOT.TH1F("histselmetnomu","Met nomu",100,0,300)
	hist_sel_jetpt = ROOT.TH1F("histseljetpt","leading jet pt",100,0,500)
	hist_sel_jeteta = ROOT.TH1F("histseljeteta","leading jet eta",20,-6,6)
	hist_sel_jetphi = ROOT.TH1F("histseljetphi","leading jet phi",20,-6,6)
	hist_sel_mupt = ROOT.TH1F("histselmupt","leading mu pt",50,0,150)
	hist_sel_mueta = ROOT.TH1F("histselmueta","leading mu eta",20,-6,6)
	hist_sel_muphi = ROOT.TH1F("histselmuphi","leading mu phi",20,-6,6)
	hist_sel_met.Sumw2() 
	hist_sel_metnomu.Sumw2() 
	hist_sel_jetpt.Sumw2() 
	hist_sel_jeteta.Sumw2() 
	hist_sel_jetphi.Sumw2() 
	hist_sel_mupt.Sumw2() 
	hist_sel_mueta.Sumw2() 
	hist_sel_muphi.Sumw2() 
	hist_sel_met.GetXaxis().SetTitle("MET [GeV]") 
	hist_sel_met.GetYaxis().SetTitle("Counts") 
	hist_sel_metnomu.GetXaxis().SetTitle("MET [GeV]") 
	hist_sel_metnomu.GetYaxis().SetTitle("Counts") 
	hist_sel_jetpt.GetXaxis().SetTitle("pt [GeV]") 
	hist_sel_jetpt.GetYaxis().SetTitle("Counts") 
	hist_sel_jeteta.GetXaxis().SetTitle("eta")
	hist_sel_jeteta.GetYaxis().SetTitle("Counts") 
	hist_sel_jetphi.GetXaxis().SetTitle("phi")
	hist_sel_jetphi.GetYaxis().SetTitle("Counts") 
	hist_sel_mupt.GetXaxis().SetTitle("pt [GEV]")
	hist_sel_mupt.GetYaxis().SetTitle("Counts") 
	hist_sel_mueta.GetXaxis().SetTitle("eta")
	hist_sel_mueta.GetYaxis().SetTitle("Counts") 
	hist_sel_muphi.GetXaxis().SetTitle("phi")
	hist_sel_muphi.GetYaxis().SetTitle("Counts") 
	for entry in t1:
		met =entry.met_met
		metnomu =entry.met_nomu
		jetpt =entry.jet1_pt
		jeteta =entry.jet1_eta
		jetphi =entry.jet1_phi
		mupt =entry.mu1_pt
		mueta =entry.mu1_eta
		muphi =entry.mu1_phi
		hist_sel_met.Fill(met)
		hist_sel_jetpt.Fill(jetpt)
		hist_sel_jeteta.Fill(jeteta)
		hist_sel_jetphi.Fill(jetphi)
		hist_sel_mupt.Fill(mupt)
		hist_sel_mueta.Fill(mueta)
		hist_sel_muphi.Fill(muphi)
		if metnomu >= 0.0:
			hist_sel_metnomu.Fill(metnomu)
	
	#hist_fired_met =   ROOT.TH1F("histfiredmet","(triggered) Met",100,0,300)
	if use_dybins:
		hist_fired_met = ROOT.TH1F("histfiredmet","(triggered) Met",75,0,300)
		hist_fired_metnomu = ROOT.TH1F("histfiredmetnomu","(triggered) Met nomu",75,0,300)
	else:
		hist_fired_met = ROOT.TH1F("histfiredmet","(triggered) Met",100,0,300)
		hist_fired_metnomu = ROOT.TH1F("histfiredmetnomu","(triggered) Met nomu",100,0,300)
	hist_fired_jetpt = ROOT.TH1F("histfiredjetpt","(triggered) leading jet pt",100,0,500)
	hist_fired_jeteta =ROOT.TH1F("histfiredjeteta","(triggered) leading jet eta",20,-6,6)
	hist_fired_jetphi =ROOT.TH1F("histfiredjetphi","(triggered) leading jet phi",20,-6,6)
	hist_fired_mupt =  ROOT.TH1F("histfiredmupt","(triggered) leading mu pt",50,0,150)
	hist_fired_mueta = ROOT.TH1F("histfiredmueta","(triggered) leading mu eta",20,-6,6)
	hist_fired_muphi = ROOT.TH1F("histfiredmuphi","(triggered) leading mu phi",20,-6,6)
	hist_fired_met.Sumw2() 
	hist_fired_metnomu.Sumw2() 
	hist_fired_jetpt.Sumw2() 
	hist_fired_jeteta.Sumw2() 
	hist_fired_jetphi.Sumw2() 
	hist_fired_mupt.Sumw2() 
	hist_fired_mueta.Sumw2() 
	hist_fired_muphi.Sumw2() 
	hist_fired_met.GetXaxis().SetTitle("MET [GeV]") 
	hist_fired_met.GetYaxis().SetTitle("Counts") 
	hist_fired_metnomu.GetXaxis().SetTitle("MET [GeV]") 
	hist_fired_metnomu.GetYaxis().SetTitle("Counts") 
	hist_fired_jetpt.GetXaxis().SetTitle("pt [GeV]") 
	hist_fired_jetpt.GetYaxis().SetTitle("Counts") 
	hist_fired_jeteta.GetXaxis().SetTitle("eta")
	hist_fired_jeteta.GetYaxis().SetTitle("Counts") 
	hist_fired_jetphi.GetXaxis().SetTitle("phi")
	hist_fired_jetphi.GetYaxis().SetTitle("Counts") 
	hist_fired_mupt.GetXaxis().SetTitle("pt [GEV]")
	hist_fired_mupt.GetYaxis().SetTitle("Counts") 
	hist_fired_mueta.GetXaxis().SetTitle("eta")
	hist_fired_mueta.GetYaxis().SetTitle("Counts") 
	hist_fired_muphi.GetXaxis().SetTitle("phi")
	hist_fired_muphi.GetYaxis().SetTitle("Counts") 
	for entry in t2:
		met =entry.met_met
		metnomu =entry.met_nomu
		jetpt =entry.jet1_pt
		jeteta =entry.jet1_eta
		jetphi =entry.jet1_phi
		mupt =entry.mu1_pt
		mueta =entry.mu1_eta
		muphi =entry.mu1_phi
		hist_fired_met.Fill(met)
		hist_fired_jetpt.Fill(jetpt)
		hist_fired_jeteta.Fill(jeteta)
		hist_fired_jetphi.Fill(jetphi)
		hist_fired_mupt.Fill(mupt)
		hist_fired_mueta.Fill(mueta)
		hist_fired_muphi.Fill(muphi)
		if metnomu >=0.0:
			hist_fired_metnomu.Fill(metnomu)
	
	hist_eff_met =   hist_fired_met.Clone("histeffmet")
	hist_eff_met.Divide(hist_sel_met) 
	hist_eff_met.SetMaximum(1.1) 
	hist_eff_met.SetMinimum(-0.10) 
	hist_eff_metnomu =   hist_fired_metnomu.Clone("histeffmetnomu")
	hist_eff_metnomu.Divide(hist_sel_metnomu) 
	hist_eff_metnomu.SetMaximum(1.1) 
	hist_eff_metnomu.SetMinimum(-0.10) 
	hist_eff_jetpt = hist_fired_jetpt.Clone("histeffjetpt")
	hist_eff_jetpt.Divide(hist_sel_jetpt) 
	hist_eff_jetpt.SetMaximum(1.0) 
	hist_eff_jetpt.SetMinimum(0.0) 
	hist_eff_jeteta =hist_fired_jeteta.Clone("histeffjeteta")
	hist_eff_jeteta.Divide(hist_sel_jeteta) 
	#hist_eff_jeteta.SetMaximum(1.0) 
	hist_eff_jeteta.SetMinimum(0.0) 
	hist_eff_jetphi =hist_fired_jetphi.Clone("histeffjetphi")
	hist_eff_jetphi.Divide(hist_sel_jetphi) 
	#hist_eff_jetphi.SetMaximum(1.0) 
	hist_eff_jetphi.SetMinimum(0.0) 
	hist_eff_mupt =  hist_fired_mupt.Clone("histeffmupt")
	hist_eff_mupt.Divide(hist_sel_mupt)
	hist_eff_mupt.SetMaximum(0.5) 
	hist_eff_mupt.SetMinimum(0.0) 
	hist_eff_mueta = hist_fired_mueta.Clone("histeffmueta")
	hist_eff_mueta.Divide(hist_sel_mueta) 
	#hist_eff_mueta.SetMaximum(1.0) 
	hist_eff_mueta.SetMinimum(0.0) 
	hist_eff_muphi = hist_fired_muphi.Clone("histeffmuphi")
	hist_eff_muphi.Divide(hist_sel_muphi) 
	#hist_eff_muphi.SetMaximum(1.0) 
	hist_eff_muphi.SetMinimum(0.0) 
	hist_eff_met.GetXaxis().SetTitle("MET [GeV]") 
	hist_eff_met.GetYaxis().SetTitle("efficiency") 
	hist_eff_jetpt.GetXaxis().SetTitle("pt [GeV]") 
	hist_eff_jetpt.GetYaxis().SetTitle("efficiency") 
	hist_eff_jeteta.GetXaxis().SetTitle("eta")
	hist_eff_jeteta.GetYaxis().SetTitle("efficiency") 
	hist_eff_jetphi.GetXaxis().SetTitle("phi")
	hist_eff_jetphi.GetYaxis().SetTitle("efficiency") 
	hist_eff_mupt.GetXaxis().SetTitle("pt [GEV]")
	hist_eff_mupt.GetYaxis().SetTitle("efficiency") 
	hist_eff_mueta.GetXaxis().SetTitle("eta")
	hist_eff_mueta.GetYaxis().SetTitle("efficiency") 
	hist_eff_muphi.GetXaxis().SetTitle("phi")
	hist_eff_muphi.GetYaxis().SetTitle("efficiency") 
	hist_eff_met.SetTitle("Met")
	hist_eff_jetpt.SetTitle("leading jet pt")
	hist_eff_jeteta.SetTitle("leading jet eta")
	hist_eff_jetphi.SetTitle("leading jet phi")
	hist_eff_mupt.SetTitle("leading mu pt")
	hist_eff_mueta.SetTitle("leading mu eta")
	hist_eff_muphi.SetTitle("leading mu phi")
	
	erf_met = ROOT.TF1("erf_met","[2]+[3]*TMath::Erf((x-[1])/[0])",125,dy_range) 
	#erf_met.SetParameters(30,125,100,0.5)
	erf_met.SetParameters(30,125,100,0.5)
	erf_met.SetParLimits(1,120,130)
	erf_met.SetParLimits(3,.40,.60)
	erf_met.SetParLimits(2,.40,.60)
	
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
	#ROOT.gStyle.SetOptFit(0111)
	hist_eff_met.Fit("erf_met","R")
	met_chi = hist_eff_met.GetFunction("erf_met").GetChisquare() 
	met_p0 = hist_eff_met.GetFunction("erf_met").GetParameter(0) 
	met_p1 = hist_eff_met.GetFunction("erf_met").GetParameter(1) 
	met_p2 = hist_eff_met.GetFunction("erf_met").GetParameter(2) 
	met_p3 = hist_eff_met.GetFunction("erf_met").GetParameter(3) 
	hist_eff_met.Draw("E1")
	plateau = met_p3 + met_p2
	x_val = get_x98(met_p0,met_p1,met_p2,met_p3,98)
	x_val100 = get_x98(met_p0,met_p1,met_p2,met_p3,100)
	print "parameters ", met_p0, met_p1, met_p2, met_p3
	print "plateau = ", plateau, " x98= ", x_val
	trigpass_met = float(hist_fired_met.GetEntries())
	trigeffi_met = 100*trigpass_met/float(hist_total_events.GetEntries())
	
	pp.Update()
	ps = pp.GetPrimitive("stats")
	ps.SetName("mystats")
	listolines = ps.GetListOfLines()
	line_p0 = ROOT.TLatex(0,0,"p0 = %.2f"%met_p0)
	line_p1 = ROOT.TLatex(0,0,"p1 = %.2f"%met_p1)
	line_p2 = ROOT.TLatex(0,0,"p2 = %.2f"%met_p2)
	line_p3 = ROOT.TLatex(0,0,"p3 = %.2f"%met_p3)
	line_chi = ROOT.TLatex(0,0,"chi2 = %.2f"%met_chi)
	line_plat = ROOT.TLatex(0,0,"plateau = %.4f"%plateau)
	line_x98 = ROOT.TLatex(0,0,"x98 = %s [GeV]"%x_val)
	line_x100 = ROOT.TLatex(0,0,"x100 = %s [GeV]"%x_val100)
	line_passeff = ROOT.TLatex(0,0,"pass = %s(%.2f%%)"%(trigpass_met,trigeffi_met))
	line_p0.SetTextFont(42)
	line_p0.SetTextSize(0.015)
	line_p1.SetTextFont(42)
	line_p1.SetTextSize(0.015)
	line_p2.SetTextFont(42)
	line_p2.SetTextSize(0.015)
	line_p3.SetTextFont(42)
	line_p3.SetTextSize(0.015)
	line_chi.SetTextFont(42)
	line_chi.SetTextSize(0.015)
	line_plat.SetTextFont(42)
	line_plat.SetTextSize(0.015)
	line_x98.SetTextFont(42)
	line_x98.SetTextSize(0.015)
	line_x100.SetTextFont(42)
	line_x100.SetTextSize(0.015)
	line_passeff.SetTextFont(42)
	line_passeff.SetTextSize(0.015)
	
	listolines.Add(line_p0)
	listolines.Add(line_p1)
	listolines.Add(line_p2)
	listolines.Add(line_p3)
	listolines.Add(line_chi)
	listolines.Add(line_plat)
	listolines.Add(line_x98)
	listolines.Add(line_x100)
	listolines.Add(line_passeff)
	hist_eff_met.SetStats(0)
	pp.Modified()
	pp.Print(ofile)
	pp.Clear()
	
	
	#hist_eff_metnomu.Fit("erf_met","R")
	#metnomu_chi = hist_eff_metnomu.GetFunction("erf_met").GetChisquare() 
	#metnomu_p0 = hist_eff_metnomu.GetFunction("erf_met").GetParameter(0) 
	#metnomu_p1 = hist_eff_metnomu.GetFunction("erf_met").GetParameter(1) 
	#metnomu_p2 = hist_eff_metnomu.GetFunction("erf_met").GetParameter(2) 
	#metnomu_p3 = hist_eff_metnomu.GetFunction("erf_met").GetParameter(3) 
	#hist_eff_metnomu.Draw("E1")
	#plateaunomu = metnomu_p3 + metnomu_p2
	#x_valnomu = get_x98(metnomu_p0,metnomu_p1,metnomu_p2,metnomu_p3,98)
	#x_val100nomu = get_x98(metnomu_p0,metnomu_p1,metnomu_p2,metnomu_p3,100)
	#print "parameters ", metnomu_p0, metnomu_p1, metnomu_p2, metnomu_p3
	#print "plateau = ", plateaunomu, " x98= ", x_valnomu
	#trigpass_nomu = float(hist_fired_metnomu.GetEntries())
	#trigeffi_nomu = 100*trigpass_nomu/float(hist_sel_metnomu.GetEntries())
	#
	#
	#pp.Update()
	#ps = pp.GetPrimitive("stats")
	#ps.SetName("mystats")
	#listolines = ps.GetListOfLines()
	#line_p0 = ROOT.TLatex(0,0,"p0 = %.2f"%metnomu_p0)
	#line_p1 = ROOT.TLatex(0,0,"p1 = %.2f"%metnomu_p1)
	#line_p2 = ROOT.TLatex(0,0,"p2 = %.2f"%metnomu_p2)
	#line_p3 = ROOT.TLatex(0,0,"p3 = %.2f"%metnomu_p3)
	#line_chi = ROOT.TLatex(0,0,"chi2 = %.2f"%metnomu_chi)
	#line_plat = ROOT.TLatex(0,0,"plateau = %.4f"%plateaunomu)
	#line_x98 = ROOT.TLatex(0,0,"x98 = %s [GeV]"%x_valnomu)
	#line_x100 = ROOT.TLatex(0,0,"x100 = %s [GeV]"%x_val100nomu)
	#line_passeff = ROOT.TLatex(0,0,"pass = %s(%.2f%%)"%(trigpass_nomu,trigeffi_nomu))
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
	#hist_eff_metnomu.SetStats(0)
	#pp.Modified()
	#pp.Print(ofile)
	#pp.Clear()
	
	
	#erf_jet = ROOT.TF1("erf_jet","[2]+[3]*TMath::Erf((x-[1])/[0])",50,275) 
	#erf_jet.SetParameters(30,125,1,0.5)
	#hist_eff_jetpt.Fit("erf_jet","R")
	#jet_chi = hist_eff_jetpt.GetFunction("erf_jet").GetChisquare() 
	#jet_p0 = hist_eff_jetpt.GetFunction("erf_jet").GetParameter(0) 
	#jet_p1 = hist_eff_jetpt.GetFunction("erf_jet").GetParameter(1) 
	#jet_p2 = hist_eff_jetpt.GetFunction("erf_jet").GetParameter(2) 
	#jet_p3 = hist_eff_jetpt.GetFunction("erf_jet").GetParameter(3) 
	hist_eff_jetpt.Draw("E1")
	#jet_plateau = jet_p3 + jet_p2
	#jet_x_val = get_x98(jet_p0,jet_p1,jet_p2,jet_p3,98)
	#
	#print "jet parameters ", jet_p0, jet_p1, jet_p2, jet_p3
	#print "jet plateau = ", jet_plateau, " x98= ", jet_x_val
	#
	#jet_st = ROOT.TText(160,0.05,"plateau=%s; x98=%s[GeV]; chi2=%s"%(jet_plateau,jet_x_val,jet_chi))
	#jet_st.SetTextSize(0.015)
	#jet_st.Draw()
	pp.Update()
	
	pp.Print(ofile)
	pp.Clear()
	hist_eff_jeteta.Draw("E1")
	pp.Print(ofile)
	pp.Clear()
	hist_eff_jetphi.Draw("E1")
	pp.Print(ofile)
	
	#erf_mu = ROOT.TF1("erf_mu","[2]+[3]*TMath::Erf((x-[1])/[0])",0,70) 
	#erf_mu.SetParameters(30,125,1,0.5)
	#hist_eff_mupt.Fit("erf_mu","R")
	#mu_chi = hist_eff_mupt.GetFunction("erf_mu").GetChisquare() 
	#mu_p0 = hist_eff_mupt.GetFunction("erf_mu").GetParameter(0) 
	#mu_p1 = hist_eff_mupt.GetFunction("erf_mu").GetParameter(1) 
	#mu_p2 = hist_eff_mupt.GetFunction("erf_mu").GetParameter(2) 
	#mu_p3 = hist_eff_mupt.GetFunction("erf_mu").GetParameter(3) 
	hist_eff_mupt.Draw("E1")
	#mu_plateau = mu_p3 + mu_p2
	#mu_x_val = get_x98(mu_p0,mu_p1,mu_p2,mu_p3,98)
	
	#print "mu parameters ", mu_p0, mu_p1, mu_p2, mu_p3
	#print "mu plateau = ", mu_plateau, " x98= ", mu_x_val
	
	#mu_st = ROOT.TText(20,0.03,"plateau=%s; x98=%s[GeV]; chi2=%s"%(mu_plateau,mu_x_val,mu_chi))
	#mu_st.SetTextSize(0.015)
	#mu_st.Draw()
	pp.Update()
	#hist_eff_mupt.Draw("E1")
	
	
	pp.Print(ofile)
	pp.Clear()
	hist_eff_mueta.Draw("E1")
	pp.Print(ofile)
	pp.Clear()
	hist_eff_muphi.Draw("E1")
	pp.Print(ofile)
	pp.Clear()
	pp.SetLogy(1)
	hist_sel_met.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_sel_jetpt.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_sel_jeteta.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_sel_jetphi.Draw()
	pp.Print(ofile)
	hist_sel_mupt.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_sel_mueta.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_sel_muphi.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_fired_met.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_fired_jetpt.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_fired_jeteta.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_fired_jetphi.Draw()
	pp.Print(ofile)
	hist_fired_mupt.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_fired_mueta.Draw()
	pp.Print(ofile)
	pp.Clear()
	hist_fired_muphi.Draw()
	pp.Print(ofile+")")
	del pp
	print "dy_range =", dy_range
	rfile = ROOT.TFile("trigeff.root","UPDATE")
	hist_eff_met.Write("hist_eff_met-%s"%ifile)
	#hist_eff_metnomu.Write("hist_eff_metnomu-%s"%ifile)
	#tree = ROOT.TTree("valuesmet%s"%rename,"values")
	
	table = open("trigger_eff_table.txt","a+")
	table.write("met: %s x98=%s x100=%s plateau=%.5f pass=%s eff=%.4%%f\n"%(ifile,x_val,x_val100,plateau,trigpass_met,trigeffi_met))
	#table.write("met no mu: %s x98=%s x100=%s plateau=%.5f pass=%s eff=%.4f\n"%(ifile,x_valnomu,x_val100nomu,plateaunomu,trigpass_nomu,trigeffi_nomu))
	table.close()
	
	with open('trigger_eff_table.csv',mode='a+') as table:
		table_writer = csv.writer(table, delimiter=',')
		table_writer.writerow([ifile,x_val,x_val100,plateau,trigpass_met,trigeffi_met])

if metnomu:
	hist_leadpt = ROOT.TH1F("histleadpt","leading: dsa_pt - pf_pt/((dsa_pt+pf_pt)/2)",100,-10,10)
	hist_leadpt.Sumw2() 
	hist_leadpt.GetXaxis().SetTitle("dsa_pt - pf_pt/((dsa_pt+pf_pt)/2)") 
	hist_leadpt.GetYaxis().SetTitle("Counts") 
	hist_leadeta = ROOT.TH1F("histleadeta","leading: dsa_eta - pf_eta/((dsa_eta+pf_eta)/2)",100,-6,6)
	hist_leadeta.Sumw2() 
	hist_leadeta.GetXaxis().SetTitle("dsa_eta - pf_eta/((dsa_eta+pf_eta)/2)") 
	hist_leadeta.GetYaxis().SetTitle("Counts") 
	hist_leadphi = ROOT.TH1F("histleadphi","leading: dsa_phi - pf_phi/((dsa_phi+pf_phi)/2)",100,-6,6)
	hist_leadphi.Sumw2() 
	hist_leadphi.GetXaxis().SetTitle("dsa_phi - pf_phi/((dsa_phi+pf_phi)/2)") 
	hist_leadphi.GetYaxis().SetTitle("Counts") 
	hist_subleadpt = ROOT.TH1F("histsubleadpt","subleading: dsa_pt - pf_pt/((dsa_pt+pf_pt)/2)",100,-10,10)
	hist_subleadpt.Sumw2() 
	hist_subleadpt.GetXaxis().SetTitle("dsa_pt - pf_pt/((dsa_pt+pf_pt)/2)") 
	hist_subleadpt.GetYaxis().SetTitle("Counts") 
	hist_subleadeta = ROOT.TH1F("histsubleadeta","subleading: dsa_eta - pf_eta/((dsa_eta+pf_eta)/2)",100,-6,6)
	hist_subleadeta.Sumw2() 
	hist_subleadeta.GetXaxis().SetTitle("dsa_eta - pf_eta/((dsa_eta+pf_eta)/2)") 
	hist_subleadeta.GetYaxis().SetTitle("Counts") 
	hist_subleadphi = ROOT.TH1F("histsubleadphi","subleading: dsa_phi - pf_phi/((dsa_phi+pf_phi)/2)",100,-6,6)
	hist_subleadphi.Sumw2() 
	hist_subleadphi.GetXaxis().SetTitle("dsa_phi - pf_phi/((dsa_phi+pf_phi)/2)") 
	hist_subleadphi.GetYaxis().SetTitle("Counts") 
	hist_leadpt2d = ROOT.TH2F("histleadpt2d","leading: dsa_pt vs pf_pt",200,0,200,200,0,200)
	hist_leadpt2d.Sumw2() 
	hist_leadpt2d.GetXaxis().SetTitle("dsa_pt") 
	hist_leadpt2d.GetYaxis().SetTitle("pf_pt") 
	hist_leadeta2d = ROOT.TH2F("histleadeta2d","leading: dsa_eta vs pf_eta",100,-6,6,100,-6,6)
	hist_leadeta2d.Sumw2() 
	hist_leadeta2d.GetXaxis().SetTitle("dsa_eta") 
	hist_leadeta2d.GetYaxis().SetTitle("pf_eta") 
	hist_leadphi2d = ROOT.TH2F("histleadphi2d","leading: dsa_phi vs pf_phi",100,-4,4,100,-4,4)
	hist_leadphi2d.Sumw2() 
	hist_leadphi2d.GetXaxis().SetTitle("dsa_phi") 
	hist_leadphi2d.GetYaxis().SetTitle("pf_phi") 
	hist_subleadpt2d = ROOT.TH2F("histsubleadpt2d","subleading: dsa_pt vs pf_pt",60,0,60,60,0,60)
	hist_subleadpt2d.Sumw2() 
	hist_subleadpt2d.GetXaxis().SetTitle("dsa_pt") 
	hist_subleadpt2d.GetYaxis().SetTitle("pf_pt") 
	hist_subleadeta2d = ROOT.TH2F("histsubleadeta2d","subleading: dsa_eta vs pf_eta",100,-6,6,100,-6,6)
	hist_subleadeta2d.Sumw2() 
	hist_subleadeta2d.GetXaxis().SetTitle("dsa_eta") 
	hist_subleadeta2d.GetYaxis().SetTitle("pf_eta") 
	hist_subleadphi2d = ROOT.TH2F("histsubleadphi2d","subleading: dsa_phi vs pf_phi",100,-4,4,100,-4,4)
	hist_subleadphi2d.Sumw2() 
	hist_subleadphi2d.GetXaxis().SetTitle("dsa_phi") 
	hist_subleadphi2d.GetYaxis().SetTitle("pf_phi") 
	for entry in tmetnomu:
		pt_dsa1 =entry.pt_dsa1
		eta_dsa1 =entry.eta_dsa1
		phi_dsa1 =entry.phi_dsa1
		pt_dsa2 =entry.pt_dsa2
		eta_dsa2 =entry.eta_dsa2
		phi_dsa2 =entry.phi_dsa2
		pt_pf1 =entry.pt_pf1
		eta_pf1 =entry.eta_pf1
		phi_pf1 =entry.phi_pf1
		pt_pf2 =entry.pt_pf2
		eta_pf2 =entry.eta_pf2
		phi_pf2 =entry.phi_pf2
		hist_leadpt.Fill( (pt_dsa1-pt_pf1)/((pt_dsa1+pt_pf1)/2.))
		hist_leadeta.Fill( (eta_dsa1-eta_pf1)/((eta_dsa1+eta_pf1)/2.))
		hist_leadphi.Fill( (phi_dsa1-phi_pf1)/((phi_dsa1+phi_pf1)/2.))
		hist_subleadpt.Fill( (pt_dsa2-pt_pf2)/((pt_dsa2+pt_pf2)/2.))
		hist_subleadeta.Fill( (eta_dsa2-eta_pf2)/((eta_dsa2+eta_pf2)/2.))
		hist_subleadphi.Fill( (phi_dsa2-phi_pf2)/((phi_dsa2+phi_pf2)/2.))
		hist_leadpt2d.Fill(pt_dsa1,pt_pf1)
		hist_leadeta2d.Fill(eta_dsa1,eta_pf1)
		hist_leadphi2d.Fill(phi_dsa1,phi_pf1)
		hist_subleadpt2d.Fill(pt_dsa2,pt_pf2)
		hist_subleadeta2d.Fill(eta_dsa2,eta_pf2)
		hist_subleadphi2d.Fill(phi_dsa2,phi_pf2)

	pp = ROOT.TCanvas("pp","pp",800,800)
	t1 = ROOT.TText(0.5,0.5,"%s"%(ifile))
	t1.SetTextAlign(22)
	t1.SetTextSize(0.05)
	t1.Draw()
	pp.Print(ofilemnm+"(")
	pp.SetLogy(1)
	pp.Clear()
	hist_leadpt.Draw()
	pp.Print(ofilemnm)
	pp.Clear()
	hist_leadeta.Draw()
	pp.Print(ofilemnm)
	pp.Clear()
	hist_leadphi.Draw()
	pp.Print(ofilemnm)
	pp.Clear()
	hist_subleadpt.Draw()
	pp.Print(ofilemnm)
	pp.Clear()
	hist_subleadeta.Draw()
	pp.Print(ofilemnm)
	pp.Clear()
	hist_subleadphi.Draw()
	pp.Print(ofilemnm)

	pp.SetLogy(0)
	pp.Clear()
	hist_leadpt2d.Draw("COLZ")
	pp.Print(ofilemnm)
	pp.Clear()
	hist_leadeta2d.Draw("COLZ")
	pp.Print(ofilemnm)
	pp.Clear()
	hist_leadphi2d.Draw("COLZ")
	pp.Print(ofilemnm)
	pp.Clear()
	hist_subleadpt2d.Draw("COLZ")
	pp.Print(ofilemnm)
	pp.Clear()
	hist_subleadeta2d.Draw("COLZ")
	pp.Print(ofilemnm)
	pp.Clear()
	hist_subleadphi2d.Draw("COLZ")
	pp.Print(ofilemnm+")")
