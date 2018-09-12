import FWCore.ParameterSet.Config as cms

trigEffiForMuTrack = cms.EDAnalyzer('trigEffiForMuTrack',
    muTrack = cms.InputTag("displacedStandAloneMuons"),
    genParticle = cms.InputTag("genParticles"),
    trigResult = cms.InputTag("TriggerResults","","HLT"),
    trigEvent = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
    trigPath = cms.string('HLT_PFMET120_PFMHT120_IDTight'),
    processName = cms.string('HLT')
  )
