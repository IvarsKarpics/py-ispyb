# coding: utf-8
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy


from app.extensions import db



class CrystalSizeDistribution(db.Model):
    __tablename__ = 'CrystalSizeDistribution'

    crystalSizeDistributionId = db.Column(db.Integer, primary_key=True, unique=True)
    crystalHabit = db.Column(db.String(255))
    characteristicDimensions = db.Column(db.Float)
    minDimension = db.Column(db.String(255), info='comma separated floats')
    maxDimension = db.Column(db.Float, info='comma separated floats')



class CrystalSlurry(db.Model):
    __tablename__ = 'CrystalSlurry'

    crystalSlurryId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    crystalId = db.Column(db.Integer, nullable=False, info='refers to BLSample.Crystal')
    crystalSizeDistributionId = db.Column(db.ForeignKey('CrystalSizeDistribution.crystalSizeDistributionId'), index=True)
    crystalDensity = db.Column(db.Float, info='1/mm3')
    bufferId = db.Column(db.Float, info='reference to Buffer.bufferId')
    micrographId = db.Column(db.ForeignKey('Micrograph.micrographId'), nullable=False, index=True)

    CrystalSizeDistribution = db.relationship('CrystalSizeDistribution', primaryjoin='CrystalSlurry.crystalSizeDistributionId == CrystalSizeDistribution.crystalSizeDistributionId', backref='crystal_slurries')
    Micrograph = db.relationship('Micrograph', primaryjoin='CrystalSlurry.micrographId == Micrograph.micrographId', backref='crystal_slurries')



class DataAcquisition(db.Model):
    __tablename__ = 'DataAcquisition'

    dataAcquisitionId = db.Column(db.Integer, primary_key=True, unique=True)
    loadedSampleId = db.Column(db.ForeignKey('LoadedSample.loadedSampleId'), nullable=False, index=True)
    dataCollectionId = db.Column(db.Integer, nullable=False, info='reference to DataCollection.dataCollectionId')
    experimentalPlanId = db.Column(db.ForeignKey('ExperimentalPlan.experimentalPlanId'), nullable=False, index=True)
    shortList = db.Column(db.String(255), nullable=False, info='url to shorlist file')
    autoprocessingProgrammId = db.Column(db.Integer, info='reference to AutoProcProgram.autoProcProgramId')

    ExperimentalPlan = db.relationship('ExperimentalPlan', primaryjoin='DataAcquisition.experimentalPlanId == ExperimentalPlan.experimentalPlanId', backref='data_acquisitions')
    LoadedSample = db.relationship('LoadedSample', primaryjoin='DataAcquisition.loadedSampleId == LoadedSample.loadedSampleId', backref='data_acquisitions')



class DataSet(db.Model):
    __tablename__ = 'DataSet'

    dataSetId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    dataAcquisitionId = db.Column(db.ForeignKey('DataAcquisition.dataAcquisitionId'), index=True)
    mergedResults = db.Column(db.String(255))

    DataAcquisition = db.relationship('DataAcquisition', primaryjoin='DataSet.dataAcquisitionId == DataAcquisition.dataAcquisitionId', backref='data_sets')



class ExperimentalPlan(db.Model):
    __tablename__ = 'ExperimentalPlan'

    experimentalPlanId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    numberOfRepetitions = db.Column(db.Integer, info='for micro-fluidic, jet, tape but not for chip')
    period = db.Column(db.Float, info='seconds but unknown/self adjusting for chip')
    masterTriggerId = db.Column(db.ForeignKey('MasterTrigger.masterTriggerId'), index=True)
    repeatedSequenceId = db.Column(db.ForeignKey('RepeatedSequence.repeatedSequenceId'), nullable=False, index=True)

    MasterTrigger = db.relationship('MasterTrigger', primaryjoin='ExperimentalPlan.masterTriggerId == MasterTrigger.masterTriggerId', backref='experimental_plans')
    RepeatedSequence = db.relationship('RepeatedSequence', primaryjoin='ExperimentalPlan.repeatedSequenceId == RepeatedSequence.repeatedSequenceId', backref='experimental_plans')



class LoadedSample(db.Model):
    __tablename__ = 'LoadedSample'

    loadedSampleId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), info='to be used as part of the image and processing file names\\n')
    sampleStockId = db.Column(db.ForeignKey('SampleStock.sampleStockId'), index=True)
    sampleDeliveryDevice = db.Column(db.Integer)
    loadingPattern = db.Column(db.Integer)
    description = db.Column(db.Text)

    SampleStock = db.relationship('SampleStock', primaryjoin='LoadedSample.sampleStockId == SampleStock.sampleStockId', backref='loaded_samples')



class MasterTrigger(db.Model):
    __tablename__ = 'MasterTrigger'

    masterTriggerId = db.Column(db.Integer, primary_key=True, unique=True)
    nameInShortlist = db.Column(db.String(255))
    triggerDevice = db.Column(db.Integer)
    description = db.Column(db.String(255))



class Micrograph(db.Model):
    __tablename__ = 'Micrograph'

    micrographId = db.Column(db.Integer, primary_key=True, unique=True)
    url = db.Column(db.String(255))
    objectSidePixelSize = db.Column(db.String(255), info='comma separated two floats')
    description = db.Column(db.String(255))



class RepeatedSequence(db.Model):
    __tablename__ = 'RepeatedSequence'

    repeatedSequenceId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))



class RepeatedSequenceHasAction(db.Model):
    __tablename__ = 'RepeatedSequenceHasAction'

    repeatedSequenceHasActionId = db.Column(db.Integer, primary_key=True, unique=True)
    repeatedSequenceId = db.Column(db.ForeignKey('RepeatedSequence.repeatedSequenceId'), index=True)
    timedExcitationId = db.Column(db.ForeignKey('TimedExcitation.timedExcitationId'), index=True)
    timedXrayExposureId = db.Column(db.ForeignKey('TimedXrayExposure.timedXrayExposureId'), index=True)
    timedXrayDetectionId = db.Column(db.ForeignKey('TimedXrayDetection.timedXrayDetectionId'), index=True)

    RepeatedSequence = db.relationship('RepeatedSequence', primaryjoin='RepeatedSequenceHasAction.repeatedSequenceId == RepeatedSequence.repeatedSequenceId', backref='repeated_sequence_has_actions')
    TimedExcitation = db.relationship('TimedExcitation', primaryjoin='RepeatedSequenceHasAction.timedExcitationId == TimedExcitation.timedExcitationId', backref='repeated_sequence_has_actions')
    TimedXrayDetection = db.relationship('TimedXrayDetection', primaryjoin='RepeatedSequenceHasAction.timedXrayDetectionId == TimedXrayDetection.timedXrayDetectionId', backref='repeated_sequence_has_actions')
    TimedXrayExposure = db.relationship('TimedXrayExposure', primaryjoin='RepeatedSequenceHasAction.timedXrayExposureId == TimedXrayExposure.timedXrayExposureId', backref='repeated_sequence_has_actions')



class SampleStock(db.Model):
    __tablename__ = 'SampleStock'

    sampleStockId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255), nullable=False)
    crystalSlurryId = db.Column(db.ForeignKey('CrystalSlurry.crystalSlurryId'), nullable=False, index=True)
    concentrationFactor = db.Column(db.Float, nullable=False)
    crystalDensity = db.Column(db.Float, nullable=False)
    additiveId = db.Column(db.Integer, info='reference to Additive.additiveId')
    note = db.Column(db.String(255))

    CrystalSlurry = db.relationship('CrystalSlurry', primaryjoin='SampleStock.crystalSlurryId == CrystalSlurry.crystalSlurryId', backref='sample_stocks')



class TimedExcitation(db.Model):
    __tablename__ = 'TimedExcitation'

    timedExcitationId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    timedSequenceId = db.Column(db.ForeignKey('TimedSequence.timedSequenceId'), index=True)
    ssxExcitation = db.Column(db.String(255))

    TimedSequence = db.relationship('TimedSequence', primaryjoin='TimedExcitation.timedSequenceId == TimedSequence.timedSequenceId', backref='timed_excitations')



class TimedSequence(db.Model):
    __tablename__ = 'TimedSequence'

    timedSequenceId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    timeOn = db.Column(db.Float, info='sec')
    timeOff = db.Column(db.Float, info='sec')
    nameInShortlist = db.Column(db.String(255))
    triggerDevice = db.Column(db.String(255))



class TimedXrayDetection(db.Model):
    __tablename__ = 'TimedXrayDetection'

    timedXrayDetectionId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    timedSequenceId = db.Column(db.ForeignKey('TimedSequence.timedSequenceId'), index=True)
    numberOfInternalTriggers = db.Column(db.Integer)
    internalTriggerPeriod = db.Column(db.Integer)
    internalGateDuration = db.Column(db.Integer)

    TimedSequence = db.relationship('TimedSequence', primaryjoin='TimedXrayDetection.timedSequenceId == TimedSequence.timedSequenceId', backref='timed_xray_detections')



class TimedXrayExposure(db.Model):
    __tablename__ = 'TimedXrayExposure'

    timedXrayExposureId = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(255))
    timedSequenceId = db.Column(db.ForeignKey('TimedSequence.timedSequenceId'), index=True)
    timedBunches = db.Column(db.String(255))
    shutter = db.Column(db.String(255))

    TimedSequence = db.relationship('TimedSequence', primaryjoin='TimedXrayExposure.timedSequenceId == TimedSequence.timedSequenceId', backref='timed_xray_exposures')