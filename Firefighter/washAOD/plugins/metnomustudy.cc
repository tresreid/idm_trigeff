#include "Firefighter/washAOD/interface/metnomustudy.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "DataFormats/Math/interface/deltaR.h"

metnomustudy::metnomustudy(const edm::ParameterSet& ps) :
  muTrackTag_(ps.getParameter<edm::InputTag>("muTrack")),
  pfmuTrackTag_(ps.getParameter<edm::InputTag>("pfmuTrack")),
  genParticleTag_(ps.getParameter<edm::InputTag>("genParticle")),
  trigResultsTag_(ps.getParameter<edm::InputTag>("trigResult")),
  trigEventTag_(ps.getParameter<edm::InputTag>("trigEvent")),
  trigPathNoVer_(ps.getParameter<std::string>("trigPath")),
  processName_(ps.getParameter<std::string>("processName")),
  muTrackToken_(consumes<reco::TrackCollection>(muTrackTag_)),
  pfmuTrackToken_(consumes<std::vector<reco::Muon>>(pfmuTrackTag_)),
  genParticleToken_(consumes<reco::GenParticleCollection>(genParticleTag_)),
  trigResultsToken_(consumes<edm::TriggerResults>(trigResultsTag_)),
  trigEventToken_(consumes<trigger::TriggerEvent>(trigEventTag_))
{
  usesResource("TFileService");
}

metnomustudy::~metnomustudy() = default;

void
metnomustudy::fillDescriptions(edm::ConfigurationDescriptions& descriptions)
{
  edm::ParameterSetDescription desc;
  desc.add<edm::InputTag>("muTrack", edm::InputTag("displacedStandAloneMuons"));
  desc.add<edm::InputTag>("pfmuTrack", edm::InputTag("muons","","RECO"));
  desc.add<edm::InputTag>("genParticle", edm::InputTag("genParticles"));
  desc.add<edm::InputTag>("trigResult", edm::InputTag("TriggerResults","","HLT"));
  desc.add<edm::InputTag>("trigEvent", edm::InputTag("hltTriggerSummaryAOD","","HLT"));
  desc.add<std::string>("trigPath", "HLT_PFMET120_PFMHT120_IDTight");
  desc.add<std::string>("processName", "HLT");
  descriptions.add("metnomustudy", desc);
}

void
metnomustudy::beginJob()
{
  muTrackT_ = fs->make<TTree>("metnomustudy", "");

  muTrackT_->Branch("fired", &fired_, "fired/O");
  muTrackT_->Branch("pt_dsa1",   &pt_dsa1);
  muTrackT_->Branch("eta_dsa1",  &eta_dsa1);
  muTrackT_->Branch("phi_dsa1",  &phi_dsa1);
  muTrackT_->Branch("pt_dsa2",   &pt_dsa2);
  muTrackT_->Branch("eta_dsa2",  &eta_dsa2);
  muTrackT_->Branch("phi_dsa2",  &phi_dsa2);
  muTrackT_->Branch("pt_pf1",   &pt_pf1);
  muTrackT_->Branch("eta_pf1",  &eta_pf1);
  muTrackT_->Branch("phi_pf1",  &phi_pf1);
  muTrackT_->Branch("pt_pf2",   &pt_pf2);
  muTrackT_->Branch("eta_pf2",  &eta_pf2);
  muTrackT_->Branch("phi_pf2",  &phi_pf2);
}

void
metnomustudy::beginRun(edm::Run const& iRun, edm::EventSetup const& iSetup)
{
  using namespace std;
  using namespace edm;

  bool changed(true);
  if (hltConfig_.init(iRun,iSetup,processName_,changed)) {
    if (changed) {
      LogInfo("metnomustudy")<<"metnomustudy::beginRun: "<<"hltConfig init for Run"<<iRun.run();
      hltConfig_.dump("ProcessName");
      hltConfig_.dump("GlobalTag");
      hltConfig_.dump("TableName");
    }
  } else {
    LogError("metnomustudy")<<"metnomustudy::beginRun: config extraction failure with processName -> "
      <<processName_;
  }

}

void
metnomustudy::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
  using namespace std;
  using namespace edm;

  iEvent.getByToken(muTrackToken_, muTrackHandle_);
  if (!muTrackHandle_.isValid()) {
    LogError("metnomustudy")
      << "metnomustudy::analyze: Error in getting muTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(pfmuTrackToken_, pfmuTrackHandle_);
  if (!pfmuTrackHandle_.isValid()) {
    LogError("metnomustudy")
      << "metnomustudy::analyze: Error in getting pfmuTrack product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(genParticleToken_, genParticleHandle_);
  if (!genParticleHandle_.isValid()) {
    LogError("metnomustudy")
      << "metnomustudy::analyze: Error in getting genParticle product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(trigResultsToken_, trigResultsHandle_);
  if (!trigResultsHandle_.isValid()) {
    LogError("metnomustudy")
      << "metnomustudy::analyze: Error in getting triggerResults product from Event!"
      << endl;
    return;
  }
  iEvent.getByToken(trigEventToken_, trigEventHandle_);
  if (!trigEventHandle_.isValid()) {
    LogError("metnomustudy")
      << "metnomustudy::analyze: Error in getting triggerEvent product from Event!"
      << endl;
    return;
  }

  int nAccpted = count_if((*genParticleHandle_).begin(), (*genParticleHandle_).end(),
      [](const reco::GenParticle& g){return abs(g.pdgId())==13;});// and g.isHardProcess() and abs(g.eta())<2.4;});
  if (nAccpted<2) return;
  if (muTrackHandle_->size()<2) return;

//  for( std::vector<reco::Muon>::const_iterator m = pfmuTrackHandle_->begin(); m != pfmuTrackHandle_->end(); ++m){
//	double mpt = m->pt();
//}

  // sort mu key by pT
  vector<int> muTrackIdx{};
  for (size_t i(0); i!=muTrackHandle_->size(); ++i) muTrackIdx.push_back(i);
  sort(muTrackIdx.begin(), muTrackIdx.end(),
      [&](int l, int r){
        reco::TrackRef lhs(muTrackHandle_, l);
        reco::TrackRef rhs(muTrackHandle_, r);
        return lhs->pt() > rhs->pt();
      });

  // MC match
  vector<int> matchedGenMuIdx{};
  for (const int muid : muTrackIdx) {
    reco::TrackRef recoMu(muTrackHandle_, muid);
    for (size_t ig(0); ig!=genParticleHandle_->size(); ++ig) {
      if (find(matchedGenMuIdx.begin(), matchedGenMuIdx.end(), ig) != matchedGenMuIdx.end()) continue;
      reco::GenParticleRef genMu(genParticleHandle_, ig);
      if (deltaR(*(recoMu.get()), *(genMu.get())) > 0.3) continue;
      if (recoMu->charge() != genMu->charge()) continue;
      matchedGenMuIdx.push_back(ig);
    }
  }
  if (matchedGenMuIdx.size()<2) return;

 // /* general selection */
 // auto generalSelection = [&](const auto tid){
 //   reco::TrackRef t(muTrackHandle_, tid);
 //   bool pass = t->pt() > 5
 //            && abs(t->eta()) < 2
 //            && t->hitPattern().numberOfValidMuonHits() > 16
 //            && t->hitPattern().muonStationsWithValidHits() > 1
 //            && t->normalizedChi2() < 10;
 //   return pass;
 // };

 // int tracksPassedGS = count_if(muTrackIdx.begin(), muTrackIdx.end(), generalSelection);
 // if (tracksPassedGS<2) return;

  pt_  .clear(); pt_  .reserve(4);
  eta_ .clear(); eta_ .reserve(4);
  phi_ .clear(); phi_ .reserve(4);

  for (const int muid : muTrackIdx) {
    reco::TrackRef recoMu(muTrackHandle_, muid);
    pt_ .push_back(recoMu->pt());
    eta_.push_back(recoMu->eta());
    phi_.push_back(recoMu->phi());
  }

  // trigger firing condition
  const vector<string>& pathNames = hltConfig_.triggerNames();
  const vector<string> matchedPaths(hltConfig_.restoreVersion(pathNames, trigPathNoVer_));
  if (matchedPaths.size() == 0) {
    LogError("metnomustudy")<<"Could not find matched full trigger path with -> "<<trigPathNoVer_<<endl;
    return;
  }
  trigPath_ = matchedPaths[0];
  if (hltConfig_.triggerIndex(trigPath_) >= hltConfig_.size()) {
    LogError("metnomustudy")<<"Cannot find trigger path -> "<<trigPath_<<endl;
    return;
  }
  fired_ = trigResultsHandle_->accept(hltConfig_.triggerIndex(trigPath_));
  pt_dsa1=pt_.at(0);
  eta_dsa1=eta_.at(0);
  phi_dsa1=phi_.at(0);
  pt_dsa2=pt_.at(1);
  eta_dsa2=eta_.at(1);
  phi_dsa2=phi_.at(1);
  pt_pf1 =0;
  pt_pf2=0;
  for (std::vector<reco::Muon>::const_iterator pf = pfmuTrackHandle_->begin(); pf != pfmuTrackHandle_->end(); ++pf){
	double pfpt = pf->pt();
	if (pfpt >500){continue;}
	if (pfpt > pt_pf1){
		pt_pf2 = pt_pf1; eta_pf2 = eta_pf1; phi_pf2 = phi_pf1; 
		pt_pf1 = pfpt; eta_pf1 = pf->eta(); phi_pf1 = pf->phi(); }
	else if ( pfpt > pt_pf2 && pfpt<= pt_pf1){
		pt_pf2 = pfpt; eta_pf2 = pf->eta(); phi_pf2 = pf->phi(); }
}
  muTrackT_->Fill();

  return;
}

void
metnomustudy::endRun(edm::Run const& iRun, edm::EventSetup const& iSetup) {}

void
metnomustudy::endJob() {}
