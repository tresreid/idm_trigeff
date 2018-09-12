import FWCore.ParameterSet.Config as cms

trigEffiForMetTrack = cms.EDAnalyzer('trigEffiForMetTrack',
    muTrack = cms.InputTag("displacedStandAloneMuons"),
    jetTrack = cms.InputTag("ak4GenJets"),
    metTrack = cms.InputTag("genMetTrue"),
    genParticle = cms.InputTag("genParticles"),
    trigResult = cms.InputTag("TriggerResults","","HLT"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    trigPath = cms.string('HLT_PFMET120_PFMHT120_IDTight'),
    processName = cms.string('HLT')
  )
