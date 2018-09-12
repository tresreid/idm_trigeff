import ROOT
ROOT.gROOT.SetBatch(True)
rfile = ROOT.TFile.Open("trigeff.root")

def setrange(h1,h2,h3,h4,h5):
        max1 = max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum()]) if h5 is None else max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum(),h5.GetMaximum()])
        min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum()]) if h5 is None else min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum()])
        h1.SetMaximum(max1*1.1)
        if min1 ==0:
        #       inte = max([h1.Integral(),h2.Integral(),h3.Integral(),h4.Integral(),h5.Integral()])
                h1.SetMinimum(0.9)
        else:
                h1.SetMinimum(min1*0.9)
def setrangenorm(h1,h2,h3,h4,h5):
        #inte = max([h1.Integral(),h2.Integral(),h3.Integral(),h4.Integral(),h5.Integral(),1])
        inte = max([h1.GetEntries(),h2.GetEntries(),h3.GetEntries(),h4.GetEntries(),h5.GetEntries(),1])
        les1 = norm(h1)
        les2 = norm(h2)
        les3 = norm(h3)
        les4 = norm(h4)
        les5 = norm(h5)
        max1 = max([h1.GetMaximum(),h2.GetMaximum(),h3.GetMaximum(),h4.GetMaximum(),h5.GetMaximum()])
        min1 = min([h1.GetMinimum(),h2.GetMinimum(),h3.GetMinimum(),h4.GetMinimum(),h5.GetMinimum()])
        h1.SetMaximum(max1*1.1)
        less = max([les1,les2,les3,les4,les5])
        if min1 ==0:
                #print h1.GetName(), less
                h1.SetMinimum(0.9*less)
                #h1.SetMinimum(.000001)
        else:
                h1.SetMinimum(min1*0.9)

def norm(histogram):
        if histogram.Integral() != 0:
                n = 1/histogram.Integral()
                histogram.Scale(n)
        else:
                n=1
        return n
def contract_plotsingle(hist,sym):
        total_bin = hist.GetSize()-2
        cut = total_bin
        cutoff = 1*(0.9/hist.GetEntries()) if hist.GetEntries() != 0 else 0
        too_small = True
        for binnum in range(total_bin,0,-5):
                empty = True
                for step in range(5):
                        if hist.GetBinContent(binnum+step) >=cutoff:
                                empty = False
                        if sym and hist.GetBinContent(total_bin-(binnum+step)) >= cutoff:
                                empty = False
                if not empty:
                        cut = binnum
                        too_small = False
                        break
        if too_small:
                for binnum in range(total_bin,0,-1):
                        empty = True
                        if hist.GetBinContent(binnum+step) >0:
                                empty = False
                        if sym and hist.GetBinContent(total_bin-(binnum+step)) > 0:
                                empty = False
                        if not empty:
                                cut = binnum
                                break
        if cut == total_bin:
                return 0
        else:
                return cut

def contract_plot(hist1,hist2,hist3,hist4,hist5,mini):
        sym = False
        if -1*(hist1.GetXaxis().GetXmin()) == hist1.GetXaxis().GetXmax():
                sym = True
        cut1 = contract_plotsingle(hist1,sym)
        cut2 = contract_plotsingle(hist2,sym)
        cut3 = contract_plotsingle(hist3,sym)
        cut4 = contract_plotsingle(hist4,sym)
        cut5 = contract_plotsingle(hist5,sym)
        cut = max([cut1,cut2,cut3,cut4,cut5])+5
        if cut == 5:
                cut = hist1.GetSize()
        if sym:
                hist1.GetXaxis().SetRange((hist1.GetSize()-2)-cut,cut)
        else:
                hist1.GetXaxis().SetRange(mini,cut)
def drawall(hist1,hist2,hist3,hist4,hist5,key,leglist,pp,sel,leg,normalized):
        pp.cd(sel+1)
        if hist2 is None:
                hist2 = ROOT.TH1F()
        if hist3 is None:
                hist3 = ROOT.TH1F()
        if hist4 is None:
                hist4 = ROOT.TH1F()
        if hist5 is None:
                hist5 = ROOT.TH1F()
        #format titles
        name = hist1.GetName()
        xtitle = "MET [GeV]" if "met" in name else ('pt [GeV]' if ('pt' in name) else ('eta' if ('eta' in name) else ('phi' if ('phi' in name) else 'unknown')))

        hist1.GetXaxis().SetTitle(xtitle)
        hist1.GetXaxis().SetTitleOffset(1.4)
	if 'nomu' in name:
		hist1.SetTitle("Met no mu: %s"%key)
	else:
		hist1.SetTitle("MET: %s"%key)
        angle_redo = False
        if "ptmet" in name and sel >= 2:
                contract_plot(hist1,hist2,hist3,hist4,hist5,hist1.GetXaxis().FindBin(120))
        elif "ptjet" in name and sel >= 3:
                contract_plot(hist1,hist2,hist3,hist4,hist5,hist1.GetXaxis().FindBin(120))
        elif ("dR" in name or "dphi" in name) and key == "anglelog":
                angle_redo = True
                hist1.GetXaxis().SetRangeUser(0,3)
        else:
                contract_plot(hist1,hist2,hist3,hist4,hist5,1)
        #set histogram format
        hist1.SetLineColor(2)
        hist2.SetLineColor(3)
        hist3.SetLineColor(4)
        hist4.SetLineColor(6)
        hist5.SetLineColor(5)
        hist1.SetMarkerColorAlpha(2,.6)
        hist2.SetMarkerColorAlpha(3,.6)
        hist3.SetMarkerColorAlpha(4,.6)
        hist4.SetMarkerColorAlpha(6,.6)
        hist5.SetMarkerColorAlpha(5,.6)
	hist1.SetMarkerStyle(8)
        hist2.SetMarkerStyle(8)
        hist3.SetMarkerStyle(8)
        hist4.SetMarkerStyle(8)
        hist5.SetMarkerStyle(8)

        if 'eff' in name:
                pp.SetLogy(0)
                hist1.SetMaximum(1.05)
                hist1.SetMinimum(0.0)
                hist1.GetYaxis().SetTitle("Efficiency")
                hist1.Draw('E1')
                hist2.Draw('E1 Same')
                hist3.Draw('E1 Same')
                hist4.Draw('E1 Same')
                hist5.Draw('E1 Same')
        if 'eff' not in name:
                hist1.GetYaxis().SetTitle("Counts")
                if normalized:
                        #norm(hist1)
                        #norm(hist2)
                        #norm(hist3)
                        #norm(hist4)
                        #norm(hist5)
                        hist1.GetYaxis().SetTitle("Normalized Counts")
                        setrangenorm(hist1,hist2,hist3,hist4,hist5)
                else:
                        setrange(hist1,hist2,hist3,hist4,hist5)
                p1 = pp.cd(sel+1)
                p1.SetLogy(1) if not angle_redo else p1.SetLogy(0)
                hist1.Draw('HIST')
                hist2.Draw('HIST Same')
                hist3.Draw('HIST Same')
                hist4.Draw('HIST Same')
                hist5.Draw('HIST Same')


        for hist,li in zip([hist1,hist2,hist3,hist4],leglist):
                if hist.GetEntries() != 0:
                        leg.AddEntry(hist,li,"f")
        leg.Draw("same")
        pp.Update()


def table_entry(hist,pp):
	hist.Draw()
	ps = pp.GetPrimitive('mystats')
	li = ps.GetLineWith('x98')
	x98 = li.ls()
	print "line", x98
#li.GetWcsTitle()


hists = {}
for  mass,split in [('5p25','0p5'),('6p0','2p0'),('52p5','5'),('60','20')]:
	for life in [1,10,100,1000]:
		hists['Mchi-%s_dMchi-%s_%smm'%(mass,split,life)] = rfile.Get("hist_eff_met-Mchi-%s_dMchi-%s_%smm"%(mass,split,life))
		hists['Mchi-%s_dMchi-%s_%smm'%(mass,split,life)].GetFunction('erf_met').Delete()
		hists['nomuMchi-%s_dMchi-%s_%smm'%(mass,split,life)] = rfile.Get("hist_eff_metnomu-Mchi-%s_dMchi-%s_%smm"%(mass,split,life))
		hists['nomuMchi-%s_dMchi-%s_%smm'%(mass,split,life)].GetFunction('erf_met').Delete()


pp = ROOT.TCanvas('pp','canv',800,800)
pp.Print("overlay.pdf(")

table = {}
templates = ['Mchi-5p25_dMchi-0p5_{0}mm','Mchi-6p0_dMchi-2p0_{0}mm','Mchi-52p5_dMchi-5_{0}mm','Mchi-60_dMchi-20_{0}mm','nomuMchi-5p25_dMchi-0p5_{0}mm','nomuMchi-6p0_dMchi-2p0_{0}mm','nomuMchi-52p5_dMchi-5_{0}mm','nomuMchi-60_dMchi-20_{0}mm']
lifes = ['1','10','100','1000']
for template in templates:
	leg = ROOT.TLegend(.7,.05,.85,.15)
	leglist = ['1','10','100','1000']
	drawall(hists[template.format(1)],hists[template.format(10)],hists[template.format(100)],hists[template.format(1000)],None,template[:-6],leglist,pp,0,leg,True)
	pp.Print("overlay.pdf")
	pp.Clear()
	
#	for life in lifes:
#		table_entry(hists[template.format(life)],pp)



for life in lifes:
	leg = ROOT.TLegend(.7,.05,.85,.15)
	leglist = ['5 10%','5 40%','50 10%','50 40%']
	drawall(hists[templates[0].format(life)],hists[templates[1].format(life)],hists[templates[2].format(life)],hists[templates[3].format(life)],None,life+'mm',leglist,pp,0,leg,True)
	pp.Print("overlay.pdf")
	pp.Clear()
	drawall(hists[templates[4].format(life)],hists[templates[5].format(life)],hists[templates[6].format(life)],hists[templates[7].format(life)],None,life+'mm',leglist,pp,0,leg,True)
	pp.Print("overlay.pdf")
	pp.Clear()

pp.Print("overlay.pdf)")
