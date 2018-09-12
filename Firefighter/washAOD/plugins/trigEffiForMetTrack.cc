#include "Firefighter/washAOD/interface/trigEffiForMetTrack.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Math/interface/deltaR.h"

trigEffiForMetTrack::trigEffiForMetTrack(const edm::ParameterSet& ps) :
  muTrackTag_(ps.getParameter<edm::InputTag>("muTrack")),
  jetTrackTag_(ps.getParameter<edm::InputTag>("jetTrack")),
  metTrackTag_(ps.getParameter<edm::InputTag>("metTrack")),
  genParticleTag_(ps.getParameter<edm::InputTag>("genParticle")),
  recojetTrackTag_(ps.getParameter<edm::InputTag>("recojetTrack")),
  recometTrackTag_(ps.getParameter<edm::InputTag>("recometTrack")),
  trigResultsTag_(ps.getParameter<edm::InputTag>("trigResult")),
  trigEventTag_(ps.getParameter<edm::InputTag>("trigEvent")),
  trigPathNoVer_(ps.getParameter<std::string>("trigPath")),
  processName_(ps.getParameter<std::string>("processName")),
  muTrackToken_(consumes<reco::TrackCollection>(muTrackTag_)),
  jetTrackToken_(consumes<std::vector<reco::GenJet>>(jetTrackTag_)),
  metTrackToken_(consumes<std::vector<reco::GenMET>>(metTrackTag_)),
  genParticleToken_(consumes<reco::GenParticleCollection>(genParticleTag_)),
  recojetTrackToken_(consumes<std::vector<reco::PFJet>>(recojetTrackTag_)),
  recometTrackToken_(consumes<std::vector<reco::PFMET>>(recometTrackTag_)),
  trigResultsToken_(consumes<edm::TriggerResults>(trigResultsTag_)),
  trigEventToken_(consumes<trigger::TriggerEvent>(trigEventTag_))
{
  usesResource("TFileService");
}

trigEffiForMetTrack::~trigEffiForMetTrack() = default;

void
trigEffiForMetTrack::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("muTrack", edm::InputTag("displacedStandAloneMuons"));
  desc.add<edm::InputTag>("jetTrack", edm::InputTag("ak4GenJets","","HLT"));
  desc.add<edm::InputTag>("metTrack", edm::InputTag("genMetTrue","","HLT"));
  desc.add<edm::InputTag>("genParticle", edm::InputTag("genParticles"));
  desc.add<edm::InputTag>("recojetTrack", edm::InputTag("ak4PFJets","","RECO"));
  desc.add<edm::InputTag>("recometTrack", edm::InputTag("pfMet","","RECO"));
  desc.add<edm::InputTag>("trigResult", edm::InputTag("TriggerResults","","HLT"));
  desc.add<edm::InputTag>("trigEvent", edm::InputTag("hltTriggerSummaryAOD","","HLT"));
  desc.add<std::string>("trigPath", "HLT_PFMET120_PFMHT120_IDTight");
  desc.add<std::string>("processName", "HLT");
  descriptions.add("trigEffiForMetTrack", desc);
}

void
trigEffiForMetTrack::beginJob()
{
  muTrackT_ = fs->make<TTree>("trigEffiForMetTrack", "");
  muTrackT_->Branch("fired", &fired_, "fired/O");
  muTrackT_->Branch("mu_pt",   &mupt_);
  muTrackT_->Branch("mu_eta",  &mueta_);
  muTrackT_->Branch("mu_phi",  &muphi_);
  muTrackT_->Branch("mu1_pt",  &mu1pt);
  muTrackT_->Branch("mu1_eta",  &mu1eta);
  muTrackT_->Branch("mu1_phi",  &mu1phi);
  muTrackT_->Branch("met_met",  &met);
  muTrackT_->Branch("met_nomu",  &metnomu);
  muTrackT_->Branch("jet1_pt",  &jet1pt);
  muTrackT_->Branch("jet1_eta",  &jet1eta);
  muTrackT_->Branch("jet1_phi",  &jet1phi);
//  muTrackT_->Branch("entries",  &selentries);
  muFiredTrackT_ = fs->make<TTree>("trigEffiForMetTrackFired", "");
  muFiredTrackT_->Branch("fired", &fired_, "fired/O");
  muFiredTrackT_->Branch("mu_pt",   &mupt_);
  muFiredTrackT_->Branch("mu_eta",  &mueta_);
  muFiredTrackT_->Branch("mu_phi",  &muphi_);
  muFiredTrackT_->Branch("mu1_pt",  &mu1pt);
  muFiredTrackT_->Branch("mu1_eta",  &mu1eta);
  muFiredTrackT_->Branch("mu1_phi",  &mu1phi);
  muFiredTrackT_->Branch("met_met",  &met);
  muFiredTrackT_->Branch("met_nomu",  &metnomu);
  muFiredTrackT_->Branch("jet1_pt",  &jet1pt);
  muFiredTrackT_->Branch("jet1_eta",  &jet1eta);
  muFiredTrackT_->Branch("jet1_phi",  &jet1phi);
 // muFiredTrackT_->Branch("entries",  &firedentries);
}

void
trigEffiForMetTrack::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
  using namespace std;
  using namespace edm;

  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      LogInfo("trigEffiForMetTrack")<<"trigEffiForMetTrack::beginRun: "<<"hltConfig init for Run"<<iRun.run();
      hltConfig_.dump("ProcessName");
      hltConfig_.dump("GlobalTag");
      hltConfig_.dump("TableName");
    }
  } else {
    LogError("trigEffiForMetTrack")<<"trigEffiForMetTrack::beginRun: config extraction failure with processName -> "
      <<processName_;
  }

}

void
trigEffiForMetTrack::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace std;
  using namespace edm;

  iEvent.getByToken(recometTrackToken_, recometTrackHandle_);
  if (!recometTrackHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting recometTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(recojetTrackToken_, recojetTrackHandle_);
  if (!recojetTrackHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting recojetTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(metTrackToken_, metTrackHandle_);
  if (!metTrackHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting metTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(jetTrackToken_, jetTrackHandle_);
  if (!jetTrackHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting jetTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(muTrackToken_, muTrackHandle_);
  if (!muTrackHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting muTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(genParticleToken_, genParticleHandle_);
  if (!genParticleHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting genParticle product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(trigResultsToken_, trigResultsHandle_);
  if (!trigResultsHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting triggerResults product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(trigEventToken_, trigEventHandle_);
  if (!trigEventHandle_.isValid()) {
    LogError("trigEffiForMetTrack")
      << "trigEffiForMetTrack::analyze: Error in getting triggerEvent product from Event!"
      << endl;
    return;
  }

  met = 0.0;
  for( std::vector<reco::PFMET>::const_iterator m = recometTrackHandle_->begin(); m != recometTrackHandle_->end(); ++m) {
             double mpt = m->pt();
	     if( mpt > met){ met = mpt;}
}
	
     if (muTrackHandle_->empty()) {metnomu = met;}
	else{ metnomu=-1;}
  // sort mu key by pT
  vector<int> muTrackIdx{};
  for (size_t i(0); i!=muTrackHandle_->size(); ++i) muTrackIdx.push_back(i);
  sort(muTrackIdx.begin(), muTrackIdx.end(),
      [&](int l, int r){
        reco::TrackRef lhs(muTrackHandle_, l);
        reco::TrackRef rhs(muTrackHandle_, r);
        return lhs->pt() > rhs->pt();
      });




//  // MC match
//  vector<int> matchedGenMuIdx{};
//  for (const int muid : muTrackIdx) {
//    reco::TrackRef recoMu(muTrackHandle_, muid);
//    for (size_t ig(0); ig!=genParticleHandle_->size(); ++ig) {
//      if (find(matchedGenMuIdx.begin(), matchedGenMuIdx.end(), ig) != matchedGenMuIdx.end()) continue;
//      reco::GenParticleRef genMu(genParticleHandle_, ig);
//      if (deltaR(*(recoMu.get()), *(genMu.get())) > 0.3) continue;
//      if (recoMu->charge() != genMu->charge()) continue;
//      matchedGenMuIdx.push_back(ig);
//    }
//  }
//  if (matchedGenMuIdx.size()<4) return;

  /* general selection */
  auto generalSelection = [&](const auto tid){
    reco::TrackRef t(muTrackHandle_, tid);
    bool pass = t->pt() > 5
             && abs(t->eta()) < 2
             && t->hitPattern().numberOfValidMuonHits() > 16
             && t->hitPattern().muonStationsWithValidHits() > 1
             && t->normalizedChi2() < 10;
    return pass;
  };

  int tracksPassedGS = count_if(muTrackIdx.begin(), muTrackIdx.end(), generalSelection);
 // if (tracksPassedGS<2) return;

  mupt_  .clear(); mupt_  .reserve(4);
  mueta_ .clear(); mueta_ .reserve(4);
  muphi_ .clear(); muphi_ .reserve(4);

  for (const int muid : muTrackIdx) {
    reco::TrackRef recoMu(muTrackHandle_, muid);
    mupt_ .push_back(recoMu->pt());
    mueta_.push_back(recoMu->eta());
    muphi_.push_back(recoMu->phi());
  }
// sort out Ht and Mht via jets 
     int nj_ht = 0, nj_mht = 0;
     double ht = 0.0;
     double mhx = 0.0;
     double mhy = 0.0;
     int minNJetHt_ =0;
     int minNJetMht_ =0;
     double minPtJetHt_ = 20.0;
     double minPtJetMht_ =20.0;
     double maxEtaJetHt_ = 5.2;
     double maxEtaJetMht_ =5.2;
     jet1pt = 0.0;
     jet1eta = 0.0;
     jet1phi = 0.0;
     if (!recojetTrackHandle_->empty()) {
         for( std::vector<reco::PFJet>::const_iterator j = recojetTrackHandle_->begin(); j != recojetTrackHandle_->end(); ++j) {
             double pt = j->pt();
             double eta = j->eta();
             double phi = j->phi();
             double px = j->px();
             double py = j->py();
             if( pt > jet1pt){
        	jet1pt = pt;
        	jet1eta = eta;
        	jet1phi = phi;
        	}
 
             if (pt > minPtJetHt_ && std::abs(eta) < maxEtaJetHt_) {
                 ht += pt;
                 ++nj_ht;
             }
 
             if (pt > minPtJetMht_ && std::abs(eta) < maxEtaJetMht_) {
                 mhx -= px;
                 mhy -= py;
                 ++nj_mht;
             }
         }
     }
     else { return;}
     if (jet1pt < 30.0) {return;}
 
    // if (excludePFMuons_) {
    //     for (auto const & j : *pfCandidates) {
    //         if (std::abs(j.pdgId()) == 13) {
    //             mhx += j.px();
    //             mhy += j.py();
    //         }
    //     }
    // }
     if (ht <0) {ht = 0;} 
     if (nj_ht  < minNJetHt_ ) { ht = 0; }
     if (nj_mht < minNJetMht_) { mhx = 0; mhy = 0; }
     double mht = sqrt(mhx*mhx+mhy*mhy);
   //  if (mht<120){return;}  
     //reco::MET::LorentzVector p4(mhx, mhy, 0, sqrt(mhx*mhx + mhy*mhy));
     //reco::MET::Point vtx(0, 0, 0);
     //reco::MET htmht(ht, p4, vtx);
     //result->push_back(htmht);/

  // trigger firing condition
  const vector<string>& pathNames = hltConfig_.triggerNames();
  const vector<string> matchedPaths(hltConfig_.restoreVersion(pathNames, trigPathNoVer_));
  if (matchedPaths.size() == 0) {
    LogError("trigEffiForMetTrack")<<"Could not find matched full trigger path with -> "<<trigPathNoVer_<<endl;
    return;
  }
  trigPath_ = matchedPaths[0];
  if (hltConfig_.triggerIndex(trigPath_) >= hltConfig_.size()) {
    LogError("trigEffiForMetTrack")<<"Cannot find trigger path -> "<<trigPath_<<endl;
    return;
  }
  fired_ = trigResultsHandle_->accept(hltConfig_.triggerIndex(trigPath_));

  mu1pt = mupt_.front();
  mu1eta = mueta_.front();
  mu1phi = muphi_.front();
  //jet1pt = jetpt_.front();
  //jet1eta = jeteta_.front();
  //jet1phi = jetphi_.front();
  muTrackT_->Fill();
  muTrackT_->SetEntries();
  if (fired_) { muFiredTrackT_->Fill();muFiredTrackT_->SetEntries();}
  return;
}

void
trigEffiForMetTrack::endRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {}

void
trigEffiForMetTrack::endJob() {}
