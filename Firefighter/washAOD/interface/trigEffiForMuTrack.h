#ifndef washAOD_trigEffiForMuTrack_H
#define washAOD_trigEffiForMuTrack_H

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
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"
#include "DataFormats/HLTReco/interface/TriggerObject.h"
#include "DataFormats/HLTReco/interface/TriggerEvent.h"
#include "HLTrigger/HLTcore/interface/HLTConfigProvider.h"

#include "TTree.h"

class trigEffiForMuTrack :
  public edm::one::EDAnalyzer<edm::one::WatchRuns, edm::one::SharedResources>
{
  public:
    explicit trigEffiForMuTrack(const edm::ParameterSet&);
    ~trigEffiForMuTrack();

    static void fillDescriptions(edm::ConfigurationDescriptions&);

  private:
    virtual void beginJob() override;
    virtual void beginRun(edm::Run const&, edm::EventSetup const&) override;
    virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
    virtual void endRun(edm::Run const&, edm::EventSetup const&) override;
    virtual void endJob() override;

    const edm::InputTag muTrackTag_;
    const edm::InputTag genParticleTag_;
    const edm::InputTag trigResultsTag_;
    const edm::InputTag trigEventTag_;
    const std::string trigPathNoVer_;
    const std::string processName_;
    const edm::EDGetTokenT<reco::TrackCollection> muTrackToken_;
    const edm::EDGetTokenT<reco::GenParticleCollection> genParticleToken_;
    const edm::EDGetTokenT<edm::TriggerResults> trigResultsToken_;
    const edm::EDGetTokenT<trigger::TriggerEvent> trigEventToken_;

    edm::Service<TFileService> fs;
    edm::Handle<reco::TrackCollection> muTrackHandle_;
    edm::Handle<reco::GenParticleCollection> genParticleHandle_;
    edm::Handle<edm::TriggerResults> trigResultsHandle_;
    edm::Handle<trigger::TriggerEvent> trigEventHandle_;

    std::string trigPath_;
    HLTConfigProvider hltConfig_;

    bool fired_;

    std::vector<float> pt_;
    std::vector<float> eta_;
    std::vector<float> phi_;

    TTree *muTrackT_;
};

#endif
