#ifndef washAOD_trigEffiForMetTrack_H
#define washAOD_trigEffiForMetTrack_H

/**
 * Trigger efficiencies in terms of events
 * =======================================
 * Require:
 *   - 4 gen muons in |eta|<2.4
 *   - 4 dSA muons matched with gen muons (dR<0.3)
 *   - >=2 dSA muons passing general selections
 * Check trigger firing condition
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/TrackReco/interface/TrackFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"
#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/METReco/interface/GenMET.h"
#include "DataFormats/METReco/interface/GenMETFwd.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/JetReco/interface/GenJetCollection.h"
#include "DataFormats/JetReco/interface/PFJet.h"
#include "DataFormats/METReco/interface/PFMET.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "TTree.h"

class trigEffiForMetTrack :
  public edm::one::EDAnalyzer<edm::one::WatchRuns, edm::one::SharedResources>
{
  public:
    explicit trigEffiForMetTrack(const edm::ParameterSet&);
    ~trigEffiForMetTrack();

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    virtual void beginJob() override;
    virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
    virtual void endJob() override;

    const edm::InputTag muTrackTag_;
    const edm::InputTag jetTrackTag_;
    const edm::InputTag metTrackTag_;
    const edm::InputTag genParticleTag_;
    const edm::InputTag recojetTrackTag_;
    const edm::InputTag recometTrackTag_;
    const edm::InputTag trigResultsTag_;
    const edm::InputTag trigEventTag_;
    const std::string trigPathNoVer_;
    const std::string processName_;
    const edm::EDGetTokenT<reco::TrackCollection> muTrackToken_;
    const edm::EDGetTokenT<std::vector<reco::GenJet>> jetTrackToken_;
    const edm::EDGetTokenT<std::vector<reco::GenMET>> metTrackToken_;
    const edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken_;
    const edm::EDGetTokenT<std::vector<reco::PFJet>> recojetTrackToken_;
    const edm::EDGetTokenT<std::vector<reco::PFMET>> recometTrackToken_;
    const edm::EDGetTokenT<edm::TriggerResults> trigResultsToken_;
    const edm::EDGetTokenT<trigger::TriggerEvent> trigEventToken_;

    edm::Service<TFileService> fs;
    edm::Handle<reco::TrackCollection> muTrackHandle_;
    edm::Handle<std::vector<reco::GenJet>> jetTrackHandle_;
    edm::Handle<std::vector<reco::GenMET>> metTrackHandle_;
    edm::Handle<reco::GenParticleCollection> genParticleHandle_;
    edm::Handle<std::vector<reco::PFJet>> recojetTrackHandle_;
    edm::Handle<std::vector<reco::PFMET>> recometTrackHandle_;
    edm::Handle<edm::TriggerResults> trigResultsHandle_;
    edm::Handle<trigger::TriggerEvent> trigEventHandle_;

    std::string trigPath_;
    HLTConfigProvider hltConfig_;
    bool fired_;

    std::vector<float> mupt_;
    std::vector<float> mueta_;
    std::vector<float> muphi_;
    float mu1pt;
    float mu1eta;
    float mu1phi;
   // std::vector<float> jetpt_;
    //std::vector<float> jeteta_;
    //std::vector<float> jetphi_;
    float jet1pt;
    float jet1eta;
    float jet1phi;
    float met;
    float metnomu;

    TTree *muTrackT_;
    TTree *muFiredTrackT_;
};

#endif
