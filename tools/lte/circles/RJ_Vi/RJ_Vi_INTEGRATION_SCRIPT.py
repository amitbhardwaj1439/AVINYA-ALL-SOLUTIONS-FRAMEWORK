# 03 GPL / LMS, all technologies (L900 / L1800 / L2100 FDD + TDD band 41), made from the kget of LMWUKES02 by
# Downloads/Vi_RJ_4G_GPL/make_vi_4g_gpl.py (03_Vi_RJ_4G_GPL_LMS_script.txt, 2026-11-13)
RJ_Vi_GPL_LMS_DST_SCRIPT = """
lt all
rbs
rbs


Confbd+
gs+

get Router=OAM,RouteTableIPv.*Static=.*,Dst=.*,NextHop= address$ > $OAM-Nexthop
get Router=LTEUP,RouteTableIPv4Static=.*,Dst=.*,NextHop= address$ > $UP-Nexthop
get Router=LTECP,RouteTableIPv4Static=.*,Dst=.*,NextHop= address$ > $CP-Nexthop


crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM_Sevice
dst 10.84.234.0/25
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=ENM_Sevice,NextHop=47
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS
dst 10.84.228.0/23
end

crn Transport=1,Router=OAM,RouteTableIPv4Static=1,Dst=OSS,NextHop=1
address $OAM-Nexthop
adminDistance 1
bfdMonitoring true
discard false
reference
end


gs-

cvms After_Routeaddd


Confbd-
gs-


lt all
rbs
rbs
confbd+
gs+

$date = `date +%y%m%d_%H%M`
cvms GPL_UpdatedLP_$date


# frequencies + frequency relations (own and all technologies): in the 02 Cell_Def script
###########
unset all

$Par[1] = L2100
$Par[2] = L1800
$Par[3] = L900
$Par[4] = TDD41

mr L2100
mr L1800
mr L900
mr TDD41

ma L2100 ^EUtranCellFDD= freqBand ^1$
ma L1800 ^EUtranCellFDD= freqBand ^3$
ma L900 ^EUtranCellFDD= freqBand ^8$
ma TDD41 ^EUtranCellTDD= freqBand ^41$

############################ FREQ Creation###########
# EUtranFrequency creation: in the 02 Cell_Def (before the cells), not here

# GeraNetwork, GeranFreqGroup 1 / 2 and GeranFrequency 57, 58, 59, 60, 61, 62, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84: created by the 01 TN_RN_GPS_MME, not here

pr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=71$
if $nr_of_mos = 0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=71
71
0
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=71 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
fi

lt all

################## Frequency Relation##########

func EURel_1451
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=1451
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=1451
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1451
  5
 fi 
done
endfunc

func EURel_265
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=265
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=265
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=265
  6
 fi 
done
endfunc

func EURel_3666
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=3666
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3666
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3666
  4
 fi 
done
endfunc

func EURel_3678
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=3678
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=3678
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3678
  4
 fi 
done
endfunc

func EURel_40940
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,EUtranFreqRelation=40940
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,EUtranFreqRelation=40940
  ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
  7
 fi 
done
endfunc

func Gran_Rel_1
for $mo in $Par[$i]
 $mordn = rdn($mo)
 pr $mordn,GeranFreqGroupRelation=1
 if $nr_of_mos = 0
  cr ENodeBFunction=1,$mordn,GeranFreqGroupRelation=1
  ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
  1
 fi 
done
endfunc

for $i = 1 to 4
EURel_1451
EURel_265
EURel_3666
EURel_3678
EURel_40940
Gran_Rel_1
done


######################

##########################GNSS MO##############

cr Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
########################################


############################ Node Level Parameters #######################

########### ENodeBFunction ##################

set ENodeBFunction=1 alignTtiBundWUlTrigSinr 1
set ENodeBFunction=1 dscpLabel 48
set ENodeBFunction=1 rrcConnReestActive true
set ENodeBFunction=1$ tRelocOverall 20
set ENodeBFunction=1 tS1HoCancelTimer 3
set ENodeBFunction=1 enabledUlTrigMeas false
set ENodeBFunction=1 zzzTemporary52 -2000000000
set ENodeBFunction=1 x2GtpuEchoDscp 48
set ENodeBFunction=1 s1GtpuEchoDscp 48
set ENodeBFunction=1 x2SetupTwoWayRelations true
set ENodeBFunction=1 csfbMeasFromIdleMode true
set ENodeBFunction=1 dnsLookupOnTai 1
set ENodeBFunction=1$ zzzTemporary13 -2000000000
set ENodeBFunction=1 caAwareMfbiIntraCellHo false
set ENodeBFunction=1 mfbiSupportPolicy false
set ENodeBFunction=1 s1HODirDataPathAvail true
set ENodeBFunction=1 gtpuErrorIndicationDscp 48
set ENodeBFunction=1 timePhaseMaxDeviationIeNbCa 30
set ENodeBFunction=1 s1GtpuEchoEnable 0
set ENodeBFunction=1 checkEmergencySoftLock false
set ENodeBFunction=1 combCellSectorSelectThreshRx 300
set ENodeBFunction=1 combCellSectorSelectThreshTx 300
set ENodeBFunction=1 licConnectedUsersPercentileConf 90
set ENodeBFunction=1 tddVoipDrxProfileId -1
set ENodeBFunction=1 timePhaseMaxDeviation 100
set ENodeBFunction=1 timePhaseMaxDeviationEdrx 10
set ENodeBFunction=1 timePhaseMaxDeviationMbms 50
set ENodeBFunction=1 timePhaseMaxDeviationOtdoa 9
set ENodeBFunction=1 timePhaseMaxDeviationSib16 100
set ENodeBFunction=1 timePhaseMaxDeviationTdd 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd1 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd2 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd3 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd4 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd5 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd6 15
set ENodeBFunction=1 timePhaseMaxDeviationTdd7 15
set ENodeBFunction=1 timePhaseMaxDevIeNBUlComp 30
set ENodeBFunction=1 ulMaxWaitingTimeGlobal 0
set ENodeBFunction=1 ulSchedulerDynamicBWAllocationEnabled true
set ENodeBFunction=1 useBandPrioritiesInSCellEval false
set ENodeBFunction=1 x2GtpuEchoEnable 0
set ENodeBFunction=1 x2IpAddrViaS1Active true
set ENodeBFunction=1 x2retryTimerMaxAuto 1440
set ENodeBFunction=1 timeAndPhaseSynchAlignment true
set ENodeBFunction=1 timeAndPhaseSynchCritical true
set ENodeBFunction=1,SecurityHandling=1 securityHandlingId 1
set ENodeBFunction=1 csmMinHighHitThreshold 50
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1$ ulMaxHARQTx 4
set ENodeBFunction=1,AdmissionControl=1$ dlAdmDifferentiationThr 750
set ENodeBFunction=1,AdmissionControl=1$ ulAdmDifferentiationThr 750
set AutoCellCapEstFunction=1$ useEstimatedCellCap true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1$ anrStateGsm 1

################  QciProfilePredefined ########################

set QciTable=default,QciProfilePredefined=QCI1$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI2$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI5$ absPrioOverride 1
set QciTable=default,QciProfilePredefined=QCI1$ aqmMode 2
set QciTable=default,QciProfilePredefined=QCI2$ aqmMode 2
set QciTable=default,QciProfilePredefined=QCI5$ aqmMode 0
set QciTable=default,QciProfilePredefined=qci6$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci8$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci9$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci2$ counterActiveMode true
set QciTable=default,QciProfilePredefined=qci5$ counterActiveMode false
set QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI1$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI2$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=QCI5$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ dlMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=QCI2$ dlMinBitRate 384
set QciTable=default,QciProfilePredefined=QCI1$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI2$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI5$ dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=QCI6$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI8$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=QCI9$ dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1$ drxPriority 99
set QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
set QciTable=default,QciProfilePredefined=qci3$ drxPriority 0
set QciTable=default,QciProfilePredefined=qci5$ drxPriority 1
set QciTable=default,QciProfilePredefined=qci1$ drxProfileRef ENodeBFunction=1,DrxProfile=1
set QciTable=default,QciProfilePredefined=qci2$ drxProfileRef ENodeBFunction=1,DrxProfile=2
set QciTable=default,QciProfilePredefined=qci5$ drxProfileRef ENodeBFunction=1,DrxProfile=5
set QciTable=default,QciProfilePredefined=QCI6$ dscp 38
set QciTable=default,QciProfilePredefined=QCI7$ dscp 36
set QciTable=default,QciProfilePredefined=QCI8$ dscp 34
set QciTable=default,QciProfilePredefined=QCI9$ dscp 34
set QciTable=default,QciProfilePredefined=QCI1$ dscp 46
set QciTable=default,QciProfilePredefined=QCI2$ dscp 44
set QciTable=default,QciProfilePredefined=QCI5$ dscp 48
set QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
set QciTable=default,QciProfilePredefined=QCI1$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI2$ inactivityTimerOffset 30
set QciTable=default,QciProfilePredefined=QCI5$ inactivityTimerOffset 0
set QciTable=default,QciProfilePredefined=qci1$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci2$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=2
set QciTable=default,QciProfilePredefined=qci5$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=QCI1$ pdb 80
set QciTable=default,QciProfilePredefined=QCI2$ pdb 150
set QciTable=default,QciProfilePredefined=QCI5$ pdb 100
set QciTable=default,QciProfilePredefined=QCI1$ pdbOffset 50
set QciTable=default,QciProfilePredefined=QCI2$ pdbOffset 50
set QciTable=default,QciProfilePredefined=QCI5$ pdbOffset 0
set QciTable=default,QciProfilePredefined=QCI1$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI2$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI5$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=QCI1$ priority 2
set QciTable=default,QciProfilePredefined=QCI2$ priority 4
set QciTable=default,QciProfilePredefined=QCI5$ priority 1
set QciTable=default,QciProfilePredefined=qci1$ resourceType 1
set QciTable=default,QciProfilePredefined=qci2$ resourceType 1
set QciTable=default,QciProfilePredefined=qci5$ resourceType 0
set QciTable=default,QciProfilePredefined=QCI1$ rlcMode 1
set QciTable=default,QciProfilePredefined=QCI2$ rlcMode 1
set QciTable=default,QciProfilePredefined=QCI5$ rlcMode 0
set QciTable=default,QciProfilePredefined=QCI1$ rlcSNLength 5
set QciTable=default,QciProfilePredefined=QCI2$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI5$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=QCI1$ rlfPriority 1
set QciTable=default,QciProfilePredefined=QCI1$ rohcEnabled true
set QciTable=default,QciProfilePredefined=QCI2$ rohcEnabled false
set QciTable=default,QciProfilePredefined=QCI5$ rohcEnabled false
set QciTable=default,QciProfilePredefined=QCI1$ schedulingAlgorithm 6
set QciTable=default,QciProfilePredefined=QCI2$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI5$ schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=QCI6$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI7$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI8$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI9$ schedulingAlgorithm 3
set QciTable=default,QciProfilePredefined=QCI1$ serviceType 1
set QciTable=default,QciProfilePredefined=QCI2$ serviceType 0
set QciTable=default,QciProfilePredefined=QCI5$ serviceType 2
set QciTable=default,QciProfilePredefined=qci1$ tReorderingDl 75
set QciTable=default,QciProfilePredefined=qci1$ ulMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=QCI2$ ulMinBitRate 384
set QciTable=default,QciProfilePredefined=qci1$ tReorderingUl 75
set RadioBearerTable=default,SignalingRadioBearer=1 tReorderingUl 35
set QciTable=default,QciProfilePredefined=QCI6$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI7$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI8$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=QCI9$ absPrioOverride 0
set QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 20
set QciTable=default,QciProfilePredefined=qci2$ qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci5$ qciSubscriptionQuanta 1
set QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 200
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a1ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a2ThresholdRsrpPrimOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold1RsrpOffset=21
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams a5Threshold2RsrpOffset=2
set QciTable=default,QciProfilePredefined=qci1 measReportConfigParams b2Threshold1RsrpUtraOffset=2
set QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci8$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci9$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=default bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci1 bitRateRecommendationEnabled true
set QciTable=default,QciProfilePredefined=qci2 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci3 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci4 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci5 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci6$ bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci65 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci66 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci69 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci7$ bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci70 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci8 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=qci9 bitRateRecommendationEnabled false
set QciTable=default,QciProfilePredefined=default$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci2$ resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci3$ resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci4$ resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci3$ schedulingAlgorithm 0
set QciTable=default,QciProfilePredefined=qci4$ schedulingAlgorithm 0


################ SCTP ####################

set Transport=1,SctpProfile=1 assocMaxRtx 10
set Transport=1,SctpProfile=1 heartbeatInterval 30000
set Transport=1,SctpProfile=1 initRto 350
set Transport=1,SctpProfile=1 maxRto 500
set Transport=1,SctpProfile=1 maxInStreams 27
set Transport=1,SctpProfile=1 maxInitRt 8
set Transport=1,SctpProfile=1 maxOutStreams 27
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 minRto 300
set Transport=1,SctpProfile=1 pathMaxRtx 5
set Transport=1,SctpProfile=1 hbMaxBurst 0
set Transport=1,SctpProfile=1 maxSctpPduSize 1460

##########  DRX Profile ##############

lset ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=2$ drxInactivityTimer 6
lset ENodeBFunction=1,DrxProfile=0$ drxInactivityTimer 14
lset ENodeBFunction=1,DrxProfile=1$ drxRetransmissionTimer 1
lset ENodeBFunction=1,DrxProfile=2$ drxRetransmissionTimer 1
lset ENodeBFunction=1,DrxProfile=0$ drxRetransmissionTimer 4
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycle 3
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycle 9
lset ENodeBFunction=1,DrxProfile=1$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=2$ longDrxCycleOnly 3
lset ENodeBFunction=1,DrxProfile=0$ longDrxCycleOnly 9
lset ENodeBFunction=1,DrxProfile=1$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=2$ onDurationTimer 6
lset ENodeBFunction=1,DrxProfile=0$ onDurationTimer 7
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycle 7
lset ENodeBFunction=1,DrxProfile=1$ shortDrxCycleTimer 0
lset ENodeBFunction=1,DrxProfile=2$ shortDrxCycleTimer 0
lset ENodeBFunction=1,DrxProfile=0$ shortDrxCycleTimer 1
lset ENodeBFunction=1,DrxProfile=1$ drxState 1
set AnrPciConflictDrxProfile=1 anrPciConflictDrxInactivityTimer 8
set AnrPciConflictDrxProfile=1 anrPciConflictOnDurationTimer 4


###########  CarrierAggregationFunction ###################

set CarrierAggregationFunction=1 dynamicSCellSelectionMethod 3
set CarrierAggregationFunction=1 selectionPolicyUlWeighting 0
set CarrierAggregationFunction=1 fourLayerMimoPreferred false
set CarrierAggregationFunction=1 enhancedSelectionOfMimoAndCa true
set CarrierAggregationFunction=1 waitForAdditionalSCellOpportunity 2000
set CarrierAggregationFunction=1 sCellActProhibitTimer 10
set CarrierAggregationFunction=1 waitForBlindSelSCellRepLessTtt 600


##################   ANR Function ##################

set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrIntraFreqState 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 hoAllowedEutranPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 x2SetupPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMax 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesEUtraIntraFMin 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMax 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 anrUesThreshInterFMin 0
set ENodeBFunction=1,AnrFunction=1 maxNoPciReportsEvent 15
set ENodeBFunction=1,AnrFunction=1 removeNenbTime 1
set ENodeBFunction=1,AnrFunction=1 removeNrelTime 2
set ENodeBFunction=1,AnrFunction=1 probCellDetectMedHoSuccThres 60
set ENodeBFunction=1,AnrFunction=1 plmnWhiteListEnabled false
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 cellAddRsrpThresholdEutran -1080
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 anrStateUtran 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 hoAllowedUtranPolicy true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1 lbCellOffloadCapacityPolicy 1000
set ENodeBFunction=1,AnrFunction=1$ removeNcellTime 1
set ENodeBFunction=1,AnrFunction=1$ cellRelHoAttRateThreshold 30
set ENodeBFunction=1,AnrFunction=1$ problematicCellPolicy 1
set ENodeBFunction=1,AnrFunction=1$ probCellDetectLowHoSuccTime 2
set ENodeBFunction=1,AnrFunction=1$ probCellDetectMedHoSuccTime 2


######## Timer Profile ####################

set QciTable=default,QciProfilePredefined=qci1 rlfProfileRef ENodeBFunction=1,RlfProfile=1
set RlfProfile=1$ n310 20
set RlfProfile=1$ n311 1
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t310 2000
set RlfProfile=1$ t311 3000
set Rrc=1 t311 3000
set Rrc=1 tRrcConnReest 2
set Rrc=1 tWaitForRrcConnReest 9
seti . tRrcConnectionSetup 3
set Rrc=1 t301 400
set Rrc=1 t304 1000
set Rrc=1 tRrcConnectionReconfiguration 10
set Rcs=1 rlcDlDeliveryFailureAction 1
set Rcs=1 tInactivityTimer 10
set RlfProfile=0$ n310 20
set RlfProfile=10$ n310 20
set RlfProfile=11$ n310 20
set RlfProfile=12$ n310 20
set RlfProfile=13$ n310 20
set RlfProfile=14$ n310 20
set RlfProfile=15$ n310 20
set RlfProfile=16$ n310 20
set RlfProfile=17$ n310 20
set RlfProfile=18$ n310 20
set RlfProfile=19$ n310 20
set RlfProfile=2$ n310 20
set RlfProfile=20$ n310 20
set RlfProfile=21$ n310 20
set RlfProfile=22$ n310 20
set RlfProfile=3$ n310 20
set RlfProfile=4$ n310 20
set RlfProfile=5$ n310 20
set RlfProfile=6$ n310 20
set RlfProfile=7$ n310 20
set RlfProfile=8$ n310 20
set RlfProfile=9$ n310 20
set RlfProfile=0$ t301 2000
set RlfProfile=0$ t310 2000
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ ulMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ tPollRetransmitUl 120
set RlfProfile=5$ t301 1000

################   AdmissionControl #########################

set AdmissionControl=1 admNrRbDifferentiationThr 750
set AdmissionControl=1 admNrRrcDifferentiationThr 750
set AdmissionControl=1 arpBasedPreEmptionState 0
set AdmissionControl=1 ulAdmOverloadThr 950
set AdmissionControl=1 ulTransNwBandwidth 2000
set AdmissionControl=1 paArpOverride 7


################  MdtConfiguration  ######################

set MdtConfiguration=1 a2ThresholdRsrpMdt -140
set MdtConfiguration=1 a2ThresholdRsrqMdt -195
set MdtConfiguration=1 timeToTriggerA2Mdt 640
set MdtConfiguration=1 triggerQuantityA2Mdt 0

############### MACConfiguration ######################

set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 ulTtiBundlingMaxHARQTx 7
set ENodeBFunction=1,RadioBearerTable=default,MACConfiguration=1 dlMaxHARQTx 4

################# Signaling-DataRadioBearer-paging  ######################

set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 tPollRetransmitDl 120
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitUl 120
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 tPollRetransmitDl 120
set ENodeBFunction=1,Paging=1 pagingDiscardTimerDrxNb 6
set ENodeBFunction=1,Paging=1 maxNoOfPagingRecordsNb 3
set ENodeBFunction=1,Paging=1 noOfDefPagCyclPrim 8

################  Load Balancing Function #################

set LoadBalancingFunction=1 lbRateOffsetCoefficient 320
set LoadBalancingFunction=1 lbRateOffsetLoadThreshold 500
set LoadBalancingFunction=1 lbCeiling 300
set LoadBalancingFunction=1 lbCaThreshold 800
set LoadBalancingFunction=1 lbThreshold 30
set LoadBalancingFunction=1 lbHitRateEUtranAddThreshold 5
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeIntensity 10
set LoadBalancingFunction=1 lbHitRateEUtranMeasUeThreshold 10
set LoadBalancingFunction=1 lbHitRateEUtranRemoveThreshold 1
set LoadBalancingFunction=1 lbMeasScalingLimit 30


################  Common Cell Parameters TDD + FDD    ###########################

set ENodeBFunction=1,EUtranCell.DD=.* allocThrPucchFormat1 50
set ENodeBFunction=1,EUtranCell.DD=.* allocTimerPucchFormat1 50
set ENodeBFunction=1,EUtranCell.DD=.* deallocThrPucchFormat1 100
set ENodeBFunction=1,EUtranCell.DD=.* deallocTimerPucchFormat1 6000
set ENodeBFunction=1,EUtranCell.DD=.* dlBlerTargetEnabled true
set ENodeBFunction=1,EUtranCell.DD=.* drxActive true
set ENodeBFunction=1,EUtranCell.DD=.* enableServiceSpecificHARQ true
set ENodeBFunction=1,EUtranCell.DD=.* pdcchCovImproveDtx true
set ENodeBFunction=1,EUtranCell.DD=.* pdcchCovImproveSrb true
set ENodeBFunction=1,EUtranCell.DD=.* pdcchTargetBler 24
set ENodeBFunction=1,EUtranCell.DD=.* pdcchTargetBlerPCell 22
set ENodeBFunction=1,EUtranCell.DD=.* pMaxServingCell 1000
set ENodeBFunction=1,EUtranCell.DD=.* tReorderingAutoConfiguration true
set ENodeBFunction=1,EUtranCell.DD=.* tTimeAlignmentTimer 1920
set ENodeBFunction=1,EUtranCell.DD=.* ulBlerTargetEnabled true
set L2100 ulHarqVolteBlerTarget 2
set L1800 ulHarqVolteBlerTarget 2
set L900 ulHarqVolteBlerTarget 2
set TDD41 ulHarqVolteBlerTarget 3
set ENodeBFunction=1,EUtranCell.DD=.* adaptiveCfiHoProhibit 0
set ENodeBFunction=1,EUtranCell.DD=.* enableSinrUplinkClpc true
set ENodeBFunction=1,EUtranCell.DD=.* pdcchCovImproveQci1 true
set L2100 pdcchOuterLoopUpStepVolte 6
set L1800 pdcchOuterLoopUpStepVolte 6
set L900 pdcchOuterLoopUpStepVolte 6
set TDD41 pdcchOuterLoopUpStepVolte 9
set ENodeBFunction=1,EUtranCell.DD=.* pdcchTargetBlerVolte 6
set ENodeBFunction=1,EUtranCell.DD=.* alpha 10
set L2100 pZeroNominalPucch -108
set L1800 pZeroNominalPucch -108
set L900 pZeroNominalPucch -117
set TDD41 pZeroNominalPucch -117
set ENodeBFunction=1,EUtranCell.DD=.* cfraEnable true
set L2100 changeNotification changeNotificationSIB15=true
set L1800 changeNotification changeNotificationSIB15=true
set L900 changeNotification changeNotificationSIB15=true
set TDD41 changeNotification changeNotificationSIB15=false
set L2100 changeNotification changeNotificationSIB16=true
set L1800 changeNotification changeNotificationSIB16=true
set L900 changeNotification changeNotificationSIB16=true
set TDD41 changeNotification changeNotificationSIB16=false
set L2100 changeNotification changeNotificationSIB7=true
set L1800 changeNotification changeNotificationSIB7=true
set L900 changeNotification changeNotificationSIB7=true
set TDD41 changeNotification changeNotificationSIB7=false
set ENodeBFunction=1,EUtranCell.DD=.* changeNotification changeNotificationSIB2=true
set ENodeBFunction=1,EUtranCell.DD=.* changeNotification changeNotificationSIB3=true
set L2100 changeNotification changeNotificationSIB4=true
set L1800 changeNotification changeNotificationSIB4=true
set L900 changeNotification changeNotificationSIB4=true
set TDD41 changeNotification changeNotificationSIB4=false
set ENodeBFunction=1,EUtranCell.DD=.* changeNotification changeNotificationSIB1=true
set ENodeBFunction=1,EUtranCell.DD=.* changeNotification changeNotificationSIB6=true
set ENodeBFunction=1,EUtranCell.DD=.* changeNotification changeNotificationSIB5=true
set ENodeBFunction=1,EUtranCell.DD=.* changeNotification changeNotificationSIB13=true
set L2100 changeNotification changeNotificationSIB8=true
set L1800 changeNotification changeNotificationSIB8=true
set L900 changeNotification changeNotificationSIB8=true
set TDD41 changeNotification changeNotificationSIB8=false
set ENodeBFunction=1,EUtranCell.DD=.* mappingInfoCe mappingInfoSIB10=0
set ENodeBFunction=1,EUtranCell.DD=.* hoOptAdjThresholdAbs 5
set ENodeBFunction=1,EUtranCell.DD=.* hoOptAdjThresholdPerc 50
set ENodeBFunction=1,EUtranCell.DD=.* pdcchCfiMode 5
set ENodeBFunction=1,EUtranCell.DD=.* transmissionMode 4
set ENodeBFunction=1,EUtranCell.DD=.* ns05FullBandUsersInCellThres 10
set ENodeBFunction=1,EUtranCell.DD=.* puschNcpChannelEstWindowSize 0
set ENodeBFunction=1,EUtranCell.DD=.* mobCtrlAtPoorCovActive true
set ENodeBFunction=1,EUtranCell.DD=.* servOrPrioTriggeredIFHo 0
set ENodeBFunction=1,EUtranCell.DD=.* ul64qamEnabled true
set ENodeBFunction=1,EUtranCell.DD=.* dl256QamStatus 2
set ENodeBFunction=1,EUtranCell.DD=.* dl256QamEnabled true
set ENodeBFunction=1,EUtranCell.DD=[^,]+$ qRxLevMinCe -140
set ENodeBFunction=1,EUtranCell.DD=.* pdcchLaGinrMargin 30
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringForMmtelVideoPresence=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringForMmtelVoicePresence=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringPriorityMmtelVideo=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringPriorityMmtelVoice=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringForMoDataPresence=0
set ENodeBFunction=1,EUtranCell.DD=.* noOfEnhAdptReTxCand -1
set ENodeBFunction=1,EUtranCell.DD=.* dynUlResourceAllocEnabled false
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock6 tReselectionUtra=2
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock6 tReselectionUtraSfHigh=100
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock6 tReselectionUtraSfMedium=100
set ENodeBFunction=1,EUtranCell.DD=.* advCellSupAction 1
set ENodeBFunction=1,EUtranCell.DD=.* primaryPlmnReserved false
set ENodeBFunction=1,EUtranCell.DD=.* harqOffsetDl 3
set ENodeBFunction=1,EUtranCell.DD=.* harqOffsetUl 3
set ENodeBFunction=1,EUtranCell.DD=.* highSpeedUEActive false
set ENodeBFunction=1,EUtranCell.DD=.* initialBufferSizeDefault 86
set ENodeBFunction=1,EUtranCell.DD=.* prsTransmisScheme 0
set ENodeBFunction=1,EUtranCell.DD=.* puschPwrOffset64qam 0
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 tEvaluation=240
set ENodeBFunction=1,EUtranCell.DD=.* cellRange 15
set L2100 elcEnabled true
set L1800 elcEnabled true
set L900 elcEnabled false
set TDD41 elcEnabled true
set ENodeBFunction=1,EUtranCell.DD=.* preambleInitialReceivedTargetPower -110
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForCsfb acBarringFactor=95
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForCsfb acBarringTime=64
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForEmergency false
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForMoData acBarringFactor=95
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForMoData acBarringTime=64
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForMoSignalling acBarringFactor=95
set ENodeBFunction=1,EUtranCell.DD=.* acBarringForMoSignalling acBarringTime=64
set ENodeBFunction=1,EUtranCell.DD=.* acBarringInfoPresent false
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringForCsfbPresence=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringForMoSignPresence=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringPriorityCsfb=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringPriorityMoData=0
set ENodeBFunction=1,EUtranCell.DD=.* acBarringPresence acBarringPriorityMoSignaling=0
set ENodeBFunction=1,EUtranCell.DD=.* spifhoSetupBearerAtInitialCtxtSetup false
set ENodeBFunction=1,EUtranCell.DD=.* srDetectHighThres 70
set ENodeBFunction=1,EUtranCell.DD=.* srProcessingLevel 0
set ENodeBFunction=1,EUtranCell.DD=.* ssacBarringForMMTELVideo acBarringFactor=95
set ENodeBFunction=1,EUtranCell.DD=.* ssacBarringForMMTELVideo acBarringTime=64
set ENodeBFunction=1,EUtranCell.DD=.* ssacBarringForMMTELVoice acBarringFactor=95
set ENodeBFunction=1,EUtranCell.DD=.* ssacBarringForMMTELVoice acBarringTime=64
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 nCellChangeHigh=16
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 nCellChangeMedium=16
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 qHystSfHigh=0
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 qHystSfMedium=0
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 sIntraSearchQ=0
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 sNonIntraSearchv920Active=false
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 sIntraSearchv920Active=false
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 threshServingLowQ=1000
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock3 tHystNormal=240
set L2100 systemInformationBlock7 tReselectionGeran=2
set L1800 systemInformationBlock7 tReselectionGeran=2
set L900 systemInformationBlock7 tReselectionGeran=3
set TDD41 systemInformationBlock7 tReselectionGeran=2
set ENodeBFunction=1,EUtranCell.DD=.* systemInformationBlock7 tReselectionGeranSfHigh=100
set ENodeBFunction=1,EUtranCell.DD=.* tUeBlockingTimer 200
set ENodeBFunction=1,EUtranCell.DD=.* ulImprovedUeSchedLastEnabled true
set ENodeBFunction=1,EUtranCell.DD=.* ulSCellPriority 5
set ENodeBFunction=1,EUtranCell.DD=.* ulSchedCtrlForOocUesEnabled true
set ENodeBFunction=1,EUtranCell.DD=.* ulSrsEnable false
set ENodeBFunction=1,EUtranCell.DD=.* ulTxPsdDistrThr 40
set ENodeBFunction=1,EUtranCell.DD=.* uncertAltitude 0
set ENodeBFunction=1,EUtranCell.DD=.* uncertSemiMajor 0
set ENodeBFunction=1,EUtranCell.DD=.* uncertSemiMinor 0
set ENodeBFunction=1,EUtranCell.DD=.* covTriggerdBlindHoAllowed true
set ENodeBFunction=1,EUtranCell.DD=[^,]+$ qQualMin -34
set ENodeBFunction=1,EUtranCell.DD=[^,]+$ qRxLevMin -124
set ENodeBFunction=1,EUtranCell.DD=.* srvccDelayTimer 3000
set ENodeBFunction=1,EUtranCell.DD=.* dlInterferenceManagementActive true
set ENodeBFunction=1,EUtranCell.DD=.* ulInterferenceManagementActive true
set ENodeBFunction=1,EUtranCell.DD=.* dlFrequencyAllocationProportion 100
set ENodeBFunction=1,EUtranCell.DD=.* ulConfigurableFrequencyStart 0
set ENodeBFunction=1,EUtranCell.DD=.* ulFrequencyAllocationProportion 100
set ENodeBFunction=1,EUtranCell.DD=.* outOfCoverageSparseGrantingBsr 4
set ENodeBFunction=1,EUtranCell.DD=.* eUlFssSwitchThresh 100
set L2100 pdcchPowerBoostMax 3
set L1800 pdcchPowerBoostMax 3
set L900 pdcchPowerBoostMax 0
set TDD41 pdcchPowerBoostMax 3
set ENodeBFunction=1,EUtranCell.DD=.* dlMaxRetxRrcReleaseThr 2
set ENodeBFunction=1,EUtranCell.DD=.* sCellHandlingAtVolteCall 1


################  Common Cell Parameters FDD Technology   ###########################

set ENodeBFunction=1,EUtranCellFDD=.* pdcchOuterLoopUpStep 8
set ENodeBFunction=1,EUtranCellFDD=.* pdcchOuterLoopUpStepPCell 6
set ENodeBFunction=1,EUtranCellFDD=.* ttiBundlingAfterHo 1
set ENodeBFunction=1,EUtranCellFDD=.* ttiBundlingAfterReest 1
set ENodeBFunction=1,EUtranCellFDD=.* ttiBundlingSwitchThres 90
set ENodeBFunction=1,EUtranCellFDD=.* ttiBundlingSwitchThresHyst 20
set ENodeBFunction=1,EUtranCellFDD=.* cellDownlinkCaCapacity 0
set ENodeBFunction=1,EUtranCellFDD=.* mappingInfo mappingInfoSIB12=7
set ENodeBFunction=1,EUtranCellFDD=.* mappingInfo mappingInfoSIB5=3
set ENodeBFunction=1,EUtranCellFDD=.* servOrPrioTriggeredErabAction 3
set ENodeBFunction=1,EUtranCellFDD=.* dlInternalChannelBandwidth 0
set ENodeBFunction=1,EUtranCellFDD=.* ulInternalChannelBandwidth 0
set ENodeBFunction=1,EUtranCellFDD=.* commonSrPeriodicity 10
set ENodeBFunction=1,EUtranCellFDD=.* lbEUtranTriggerOffloadThreshold 100
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB1=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB2=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB3=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB4=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB5=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB6=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB7=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB13=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB15=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB16=true
set ENodeBFunction=1,EUtranCellFDD=.* changeNotification changeNotificationSIB8=true
set L2100 pZeroNominalPusch -100
set L1800 pZeroNominalPusch -100
set L900 pZeroNominalPusch -103
set ENodeBFunction=1,EUtranCellFDD=.* crsGain 0
set ENodeBFunction=1,EUtranCellFDD=.* ulTrigActive true
set ENodeBFunction=1,EUtranCellFDD=.* pdschTypeBGain 0
set ENodeBFunction=1,EUtranCellFDD=.* lbEUtranAcceptOffloadThreshold 50
set ENodeBFunction=1,EUtranCellFDD=.* systemInformationBlock3 sNonIntraSearch=10
set L2100 systemInformationBlock3 sNonIntraSearchP=12
set L1800 systemInformationBlock3 sNonIntraSearchP=10
set L900 systemInformationBlock3 sNonIntraSearchP=12


################  Common Cell Parameters TDD Technology   ###########################

set ENodeBFunction=1,EUtranCellTDD=.* hoOptStatTime 24
set ENodeBFunction=1,EUtranCellTDD=.* dlMaxMuMimoLayers 0
set ENodeBFunction=1,EUtranCellTDD=.* ulMaxMuMimoLayers 0
set ENodeBFunction=1,EUtranCellTDD=.* subframeAssignment 2
set ENodeBFunction=1,EUtranCellTDD=.* timePhaseMaxDeviationTddIndex 0
set ENodeBFunction=1,EUtranCellTDD=.* commonSrPeriodicity 20
set ENodeBFunction=1,EUtranCellTDD=.* mappingInfo mappingInfoSIB7=0
set ENodeBFunction=1,EUtranCellTDD=.* pZeroNominalPusch -100
set ENodeBFunction=1,EUtranCellTDD=.* crsGain 300
set ENodeBFunction=1,EUtranCellTDD=.* pdschTypeBGain 1
set ENodeBFunction=1,EUtranCellTDD=.* ulTrigActive true
set ENodeBFunction=1,EUtranCellTDD=.* cellRange 15
set ENodeBFunction=1,EUtranCellTDD=.* outOfCoverageSparseGrantingBsr 4
set ENodeBFunction=1,EUtranCellTDD=.* interferenceThresholdSinrClpc -105
set ENodeBFunction=1,EUtranCellTDD=.* rxSinrTargetClpc 25
set ENodeBFunction=1,EUtranCellTDD=.* lbEUtranAcceptOffloadThreshold 50
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 sNonIntraSearch=10
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 sNonIntraSearchQ=0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1$ inhibitB2RsrqConfig true
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 0
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1$ a3offsetAnrDelta 3
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5 480
set ENodeBFunction=1,EUtranCellTDD=.* alpha 10
set ENodeBFunction=1,EUtranCellTDD=.* cellCapMaxCellSubCap 36000
set ENodeBFunction=1,EUtranCellTDD=.* cellCapMinCellSubCap 12000
set ENodeBFunction=1,EUtranCellTDD=.* drxActive true
set ENodeBFunction=1,EUtranCellTDD=.* pdcchLaGinrMargin 30
set ENodeBFunction=1,EUtranCellTDD=.* pdcchOuterLoopUpStepVolte 9
set ENodeBFunction=1,EUtranCellTDD=.* pdcchPowerBoostMax 3
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1Search 480
set ENodeBFunction=1,EUtranCellTDD=.* ulBlerTargetEnabled true
set ENodeBFunction=1,EUtranCellTDD=.* enableServiceSpecificHARQ true
set ENodeBFunction=1,EUtranCellTDD=.* tReorderingAutoConfiguration true
set ENodeBFunction=1,EUtranCellTDD=.* srvccDelayTimer 3000
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ b2Threshold2Geran -101
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ hysteresisB2 20
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ timeToTriggerB2 480
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 320
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1,ReportConfigEUtraBestCellAnr=1$ timeToTriggerA3 480
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigEUtraIFBestCell=1$ timeToTriggerA3 40
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1$ ueMeasurementsActive true
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Search 480
set ENodeBFunction=1,EUtranCellTDD=.* advCellSupAction 1
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ timeToTriggerB2 640
set ENodeBFunction=1,EUtranCellTDD=.* dlBlerTargetEnabled true
set ENodeBFunction=1,EUtranCellTDD=.* pdcchCovImproveDtx true
set ENodeBFunction=1,EUtranCellTDD=.* ulHarqVolteBlerTarget 3
set ENodeBFunction=1,EUtranCellTDD=.* ns05FullBandUsersInCellThres 10
set ENodeBFunction=1,EUtranCellTDD=.* puschNcpChannelEstWindowSize 0
set ENodeBFunction=1,EUtranCellTDD=.* noOfEnhAdptReTxCand -1
set ENodeBFunction=1,EUtranCellTDD=.* dynUlResourceAllocEnabled false
set ENodeBFunction=1,EUtranCellTDD=.* acBarringInfoPresent false
set ENodeBFunction=1,EUtranCellTDD=.* eUlFssSwitchThresh 100
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrp -114
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold1Rsrq -30
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold2Rsrp -114
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1$ a5Threshold2Rsrq -195
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigB1GUtra=1$ b1ThresholdRsrq -435
set ENodeBFunction=1,EUtranCellTDD=.* cellSubscriptionCapacity 24000
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -110
set ENodeBFunction=1,EUtranCellTDD=.* pdcchTargetBlerVolte 6
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1$ excludeInterFreqAtCritical false
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5 20
set ENodeBFunction=1,EUtranCellTDD=.* enableSinrUplinkClpc true
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1UlSearch 40
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock6 tReselectionUtra=2
set ENodeBFunction=1,EUtranCellTDD=.* systemInformationBlock3 sIntraSearchQ=0
set ENodeBFunction=1,EUtranCellTDD=.* changeNotification changeNotificationSIB15=false
set ENodeBFunction=1,EUtranCellTDD=.* changeNotification changeNotificationSIB16=false


###############  Relation Parameters #################

set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=1451$ tReselectionEutra 1
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=265$ tReselectionEutra 1
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=3666$ tReselectionEutra 2
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=3678$ tReselectionEutra 2
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=40940$ tReselectionEutra 1
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ anrMeasOn true
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ anrMeasOn true
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*,EUtranCellRelation=.*$ isHoAllowed true
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ qRxLevMin -105
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ qRxLevMinCe -140
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ pMax 1000
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ tReselectionEutraSfHigh 100
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ tReselectionEutraSfMedium 100
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ qRxLevMin -124
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ mobilityAction 1
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ lbBnrPolicy 1
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=1451$ allowedMeasBandwidth 50
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=265$ allowedMeasBandwidth 75
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=3666$ allowedMeasBandwidth 15
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=3678$ allowedMeasBandwidth 25
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=40940$ allowedMeasBandwidth 100

########################  threshXHigh & threshXLow ####################


set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ threshXHigh 12


set ENodeBFunction=1,EUtranCellTDD=.*,GeranFreqGroupRelation=1$ threshXLow 0

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ threshXLow 12
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=.*$ threshXLow 12


for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ threshXLow 10
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ threshXLow 10
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ threshXLow 0
done

##################### UeMeasControl=1 ##############################
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigCsfbUtra=1$ hysteresis 10
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigCsfbGeran=1$ hysteresis 10
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSCellA6=1$ triggerQuantityA6 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1$ hysteresisA3 10
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5 20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ hysteresisB2 20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1Search 480
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1SearchRsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Critical 320
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2CriticalRsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Search 480
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2SearchRsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5 480
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5Rsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ timeToTriggerB2 640
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigEUtraBestCell=1$ triggerQuantityA3 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5=1$ triggerQuantityA5 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSCellA6=1$ timeToTriggerA6 40
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigElcA1A2=1$ hysteresisA1A2Rsrp 10
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1Geran=1$ hysteresisB1 10
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1Utra=1$ hysteresisB1 10
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigElcA1A2=1$ timeToTriggerA1 40
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSCellA1A2=1$ timeToTriggerA1 40
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSCellA1A2=1$ timeToTriggerA2 40
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigElcA1A2=1$ timeToTriggerA2 40
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2OutSearchRsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1Geran=1$ timeToTriggerB1 640
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ timeToTriggerB2Rsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ timeToTriggerB2Rsrq -1
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ hysteresisA5 20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThrQci1RsrpOffset -20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ filterCoefficientEUtraRsrp 4
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ ueMeasurementsActiveIF true
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ sMeasure -80
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ lowPrioMeasThresh 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ maxUtranCellsToMeasure 32
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ allowReleaseQci1 false
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ ulSinrOffset 30
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ ueMeasurementsActive true
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ a5B2MobilityTimer 0
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1$ ueMeasurementsActiveGERAN true
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1$ ueMeasurementsActiveGERAN true
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ excludeInterFreqAtCritical false
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ a3SuspendCsgTimer 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ ueMeasurementsActiveUTRAN true
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2UlCritical 40
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2UlCritical 40
set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2UlSearch 40
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2UlSearch 40
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5RsrqOffset 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ b2Threshold2Geran -101
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold1Rsrp -116
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThrQci1RsrqOffset -50
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ a1a2UlSearchThreshold -150
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2UlCritical 20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ csfbHoTargetSearchTimer 500
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ bothA5RsrpRsrqCheck false
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1$ inhibitB2RsrqConfig true
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ b2Threshold1Rsrp -122
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1Geran=1$ b1ThresholdGeran -110
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1$ reportIntervalB2 12
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ hysteresisB2 20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB2Geran=1$ b2Threshold1Rsrq -195


for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrp -122
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 10
 set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 320
 set $mordn,UeMeasControl=1$ zzzTemporary13 1
 set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1$ hysteresisA1A2RsrpBidirectional 10
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrp -122
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 10
 set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 320
 set $mordn,UeMeasControl=1$ zzzTemporary13 -2000000000
 set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1$ hysteresisA1A2RsrpBidirectional 10
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrp -123
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 10
 set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 256
 set $mordn,UeMeasControl=1$ zzzTemporary13 1
 set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1$ hysteresisA1A2RsrpBidirectional 20
done

for $mo in TDD41
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrp -122
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 0
 set $mordn,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 320
 set $mordn,UeMeasControl=1$ zzzTemporary13 -2000000000
 set $mordn,UeMeasControl=1,ReportConfigSCellA1A2=1$ hysteresisA1A2RsrpBidirectional 20
done

######################  AnrFunction=1 ############################

set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 cellAddEcNoThresholdUtranDelta 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionUtran=1 cellAddRscpThresholdUtranDelta 0
set ENodeBFunction=1,AnrFunction=1,AnrFunctionGeran=1 problematicCellPolicy 0
set ENodeBFunction=1,AnrFunction=1 zzzTemporary13 -2000000000


######## TWAMP setting #######################

get Router=LTEUP,RouteTableIPv4Static=2,Dst=UP_DEFAULT_ROUTE,NextHop= address$ > $UP-Nexthop

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_A_UP,AddressIPv4=TN_A_UP
responderType 1
udpPort 4001
userLabel 
end

get Router=LTEUP,RouteTableIPv4Static=2,Dst=UP_DEFAULT_ROUTE,NextHop= address$ > $UP-Nexthop

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_C_UP,AddressIPv4=TN_C_UP
responderType 1
udpPort 4001
userLabel 
end

get Router=LTEUP,RouteTableIPv4Static=2,Dst=UP_DEFAULT_ROUTE,NextHop= address$ > $UP-Nexthop

crn Transport=1,Router=LTEUP,TwampResponder=1
ipAddress Router=LTEUP,InterfaceIPv4=TN_E_UP,AddressIPv4=TN_E_UP
responderType 1
udpPort 4001
userLabel 
end

######## QOS setting #######################################

set ENodeBFunction=1 interEnbCaTunnelDscp 34
set ENodeBFunction=1 interEnbUlCompTunnelDscp 34

cr Transport=1,QosProfiles=1,DscpPcpMap=1

set QciTable=default,QciProfilePredefined=qci3 dscp 42
set QciTable=default,QciProfilePredefined=qci4 dscp 39

set SysM=1,OamTrafficClass=1 dscp 40

set EthernetPort=.* egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

set SctpProfile= dscp 48


lt all


set QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,4,5,6,7
set QosProfiles=1,DscpPcpMap=1 pcp1 8,9,10,11,12,13,14,15
set QosProfiles=1,DscpPcpMap=1 pcp2 16,17,18,19,20,21,22,23
set QosProfiles=1,DscpPcpMap=1 pcp3 24,25,26,27,28,29,30,31
set QosProfiles=1,DscpPcpMap=1 pcp4 32,33,34,35,36,37,38,39
set QosProfiles=1,DscpPcpMap=1 pcp5 40,41,42,43,44,45,46,47
set QosProfiles=1,DscpPcpMap=1 pcp6 48,49,50,51,52,53,54,55
set QosProfiles=1,DscpPcpMap=1 pcp7 56,57,58,59,60,61,62,63


set Router=OAM,DnsClient=1 dscp 40

set Router=.*,InterfaceIPv4= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Router=LTECP,InterfaceIPv4=.* egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Router=LTEUP,InterfaceIPv4=.* egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set Router=OAM,InterfaceIPv4=.* egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
set VlanPort= egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1


######## QOS setting #######################################

$date = `date +%y%m%d_%H%M`
cvms BEFORE_Baseline-twamp_$date


cr Transport=1,QosProfiles=1,DscpPcpMap=1


lt all


##Features_GPL

set CXC4011713 featureState 1
set CXC4012238 featureState 0
set CXC4012097 featureState 1
set CXC4011368 featureState 0
set CXC4012036 featureState 0
set CXC4010512 featureState 0
set CXC4010955 featureState 0
set CXC4010973 featureState 1
set CXC4011055 featureState 1
set CXC4011246 featureState 1
set CXC4011346 featureState 1
set CXC4011478 featureState 0
set cxc4011554 featureState 0
set CXC4011663 featureState 1
set CXC4011664 featureState 0
set CXC4011736 featureState 0
set CXC4011810 featureState 0
set cxc4011911 featureState 0
set cxc4011966 featureState 1
set CXC4011983 featureState 1
set CXC4011714 featureState 1
set CXC4010319 featureState 1
set CXC4010320 featureState 1
set CXC4010609 featureState 1
set CXC4010613 featureState 1
set CXC4010616 featureState 1
set CXC4010618 featureState 1
set CXC4010620 featureState 1
set CXC4010717 featureState 1
set CXC4010723 featureState 1
set CXC4010770 featureState 1
set CXC4010841 featureState 1
set CXC4010856 featureState 1
set CXC4010912 featureState 1
set CXC4010956 featureState 1
set CXC4010959 featureState 1
set CXC4010961 featureState 1
set CXC4010962 featureState 1
set CXC4010967 featureState 1
set CXC4010974 featureState 1
set CXC4010980 featureState 1
set CXC4010990 featureState 1
set CXC4011011 featureState 1
set CXC4011033 featureState 1
set CXC4011034 featureState 1
set CXC4011050 featureState 1
set CXC4011057 featureState 1
set CXC4011059 featureState 1
set CXC4011060 featureState 1
set CXC4011061 featureState 1
set CXC4011062 featureState 0
set CXC4011064 featureState 1
set CXC4011074 featureState 1
set CXC4011075 featureState 1
set CXC4011157 featureState 1
set CXC4011183 featureState 1
set CXC4011245 featureState 1
set CXC4011247 featureState 1
set CXC4011251 featureState 1
set CXC4011252 featureState 1
set CXC4011253 featureState 1
set CXC4011255 featureState 1
set CXC4011258 featureState 1
set CXC4011319 featureState 1
set CXC4011327 featureState 1
set CXC4011345 featureState 1
set CXC4011366 featureState 1
set CXC4011370 featureState 1
set CXC4011372 featureState 1
set CXC4011373 featureState 1
set CXC4011376 featureState 1
set CXC4011378 featureState 1
set CXC4011422 featureState 1
set CXC4011443 featureState 1
set CXC4011444 featureState 1
set CXC4011477 featureState 1
set CXC4011479 featureState 1
set CXC4011481 featureState 1
set CXC4011482 featureState 1
set CXC4011485 featureState 1
set CXC4011515 featureState 1
set CXC4011698 featureState 1
set CXC4011711 featureState 1
set CXC4011715 featureState 1
set CXC4011813 featureState 1
set CXC4011815 featureState 1
set CXC4011910 featureState 1
set CXC4011913 featureState 1
set CXC4011914 featureState 1
set CXC4011918 featureState 1
set CXC4011940 featureState 1
set CXC4011941 featureState 1
set CXC4011969 featureState 1
set CXC4012003 featureState 1
set CXC4012018 featureState 1
set CXC4012070 featureState 1
set CXC4012089 featureState 1
set CXC4011559 featureState 1
set CXC4011922 featureState 1
set CXC4011946 featureState 1
set CXC4012129 featureState 0
set CXC4012240 featureState 1
set CXC4011072 featureState 0
set CXC4011974 featureState 0

##20Q2 Features-

set CXC4012316 featureState 0
set CXC4012271 featureState 0
set CXC4012260 featureState 0
set CXC4012374 featureState 0
set CXC4012344 featureState 0
set CXC4012370 featureState 0
set CXC4012326 featureState 0
set CXC4012349 featureState 1
set CXC4012261 featureState 0


#FORTDDSITEONLY4x4Quad

set CXC4011667 featureState 1
set CXC4011056 featureState 1

#OLD Running Features

set CXC4010949 featureState 1
set CXC4010963 featureState 1
set CXC4010964 featureState 1
set CXC4011063 featureState 1
set CXC4011065 featureState 1
set CXC4011067 featureState 1
set CXC4011068 featureState 1
set CXC4011069 featureState 1
set CXC4011155 featureState 1
set CXC4011163 featureState 1
set CXC4011256 featureState 0
set CXC4011317 featureState 1
set CXC4011356 featureState 1
set CXC4011427 featureState 1
set CXC4011512 featureState 1
set CXC4011557 featureState 1
set CXC4011618 featureState 1
set CXC4011666 featureState 0
set CXC4011699 featureState 0
set CXC4011707 featureState 1
set CXC4011710 featureState 1
set CXC4011716 featureState 1
set CXC4011804 featureState 1
set CXC4011807 featureState 0
set CXC4011808 featureState 1
set CXC4011809 featureState 1
set CXC4011811 featureState 0
set CXC4011814 featureState 0
set CXC4011817 featureState 0
set CXC4011820 featureState 1
set CXC4011917 featureState 1
set CXC4011930 featureState 1
set CXC4011933 featureState 1
set CXC4011937 featureState 1
set CXC4011938 featureState 1
set CXC4011939 featureState 1
set CXC4011942 featureState 1
set CXC4011951 featureState 1
set CXC4011958 featureState 1
set CXC4011967 featureState 1
set CXC4011973 featureState 1
set CXC4011975 featureState 0
set CXC4011982 featureState 1
set CXC4011991 featureState 0
set CXC4012022 featureState 0
set CXC4040004 featureState 1
set CXC4040005 featureState 1
set CXC4040006 featureState 1
set CXC4040008 featureState 1
set CXC4040009 featureState 1
set CXC4040010 featureState 1
set CXC4040013 featureState 1
set CXC4040014 featureState 1
set CXC4012259 featureState 1

set CXC4011823 featureState 1

##Basic Intelligence

set CXC4012218 featureState 0

###############  PRB Muting Scripts 1800 Layer only #####################

set ENodeBFunction=1,EUtranCellFDD=.* dlFrequencyAllocationProportion 100
set ENodeBFunction=1,EUtranCellFDD=.* ulFrequencyAllocationProportion 100
set ENodeBFunction=1,EUtranCellFDD=.* dlConfigurableFrequencyStart 0
set ENodeBFunction=1,EUtranCellFDD=.* ulConfigurableFrequencyStart 0
set ENodeBFunction=1,EUtranCellFDD=.* dlInterferenceManagementActive true
set ENodeBFunction=1,EUtranCellFDD=.* ulInterferenceManagementActive true
set ENodeBFunction=1,EUtranCellFDD=.* ulSrsEnable false
set ENodeBFunction=1,EUtranCellFDD=.* pucchOverdimensioning 0
set ENodeBFunction=1,EUtranCellFDD=.* dlCchAndRefSigBlockActive false
set ENodeBFunction=1,EUtranCellFDD=.* dlCchAndRefSigBoost false


###############  GERAN CSFB/SRVCC Parameter ################

set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ csFallbackPrio 4
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ csFallbackPrioEC 4
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ pMaxGeran 23
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ qOffsetFreq 0
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ nccPermitted 11111111
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ mobilityAction 0


for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ mobilityActionCsfb 1
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ mobilityActionCsfb 1
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ mobilityActionCsfb 0
done

for $mo in TDD41
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ mobilityActionCsfb 1
done

##################  Power Savings Features ###########################

---------------  Mimo Sleep Function All Layers -------------

set ENodeBFunction=1,EUtranCell.DD=.*,MimoSleepFunction=1$ sleepStartTime 18:30

for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,MimoSleepFunction=1$ sleepMode 2
 set $mordn,MimoSleepFunction=1$ sleepEndTime 17:30
 set $mordn,MimoSleepFunction=1$ sleepPowerControl 0
 set $mordn,MimoSleepFunction=1$ switchDownMonitorDurTimer 30
 set $mordn,MimoSleepFunction=1$ switchDownPrbThreshold 10
 set $mordn,MimoSleepFunction=1$ switchDownRrcConnThreshold 5
 set $mordn,MimoSleepFunction=1$ switchUpMonitorDurTimer 10
 set $mordn,MimoSleepFunction=1$ switchUpPrbThreshold 20
 set $mordn,MimoSleepFunction=1$ switchUpRrcConnThreshold 10
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,MimoSleepFunction=1$ sleepMode 2
 set $mordn,MimoSleepFunction=1$ sleepEndTime 17:30
 set $mordn,MimoSleepFunction=1$ sleepPowerControl 0
 set $mordn,MimoSleepFunction=1$ switchDownMonitorDurTimer 30
 set $mordn,MimoSleepFunction=1$ switchDownPrbThreshold 10
 set $mordn,MimoSleepFunction=1$ switchDownRrcConnThreshold 5
 set $mordn,MimoSleepFunction=1$ switchUpMonitorDurTimer 10
 set $mordn,MimoSleepFunction=1$ switchUpPrbThreshold 20
 set $mordn,MimoSleepFunction=1$ switchUpRrcConnThreshold 10
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,MimoSleepFunction=1$ sleepMode 4
 set $mordn,MimoSleepFunction=1$ sleepEndTime 17:30
 set $mordn,MimoSleepFunction=1$ sleepPowerControl 1
 set $mordn,MimoSleepFunction=1$ switchDownMonitorDurTimer 30
 set $mordn,MimoSleepFunction=1$ switchDownPrbThreshold 10
 set $mordn,MimoSleepFunction=1$ switchDownRrcConnThreshold 5
 set $mordn,MimoSleepFunction=1$ switchUpMonitorDurTimer 10
 set $mordn,MimoSleepFunction=1$ switchUpPrbThreshold 20
 set $mordn,MimoSleepFunction=1$ switchUpRrcConnThreshold 10
done

for $mo in TDD41
 $mordn = rdn($mo)
 set $mordn,MimoSleepFunction=1$ sleepMode 6
 set $mordn,MimoSleepFunction=1$ sleepEndTime 00:30
 set $mordn,MimoSleepFunction=1$ sleepPowerControl 1
 set $mordn,MimoSleepFunction=1$ switchDownMonitorDurTimer 15
 set $mordn,MimoSleepFunction=1$ switchDownPrbThreshold 35
 set $mordn,MimoSleepFunction=1$ switchDownRrcConnThreshold 20
 set $mordn,MimoSleepFunction=1$ switchUpMonitorDurTimer 5
 set $mordn,MimoSleepFunction=1$ switchUpPrbThreshold 40
 set $mordn,MimoSleepFunction=1$ switchUpRrcConnThreshold 50
done

_______________ Cell Sleep Function ___________________________

#################### 2100  ############################

set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ sleepStartTime 18:30
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ sleepEndTime 00:30
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ capCellSleepMonitorDurTimer 15
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ capCellDlPrbSleepThreshold 10
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ capCellRrcConnSleepThreshold 5
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ covCellWakeUpMonitorDurTimer 15
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ covCellDlPrbWakeUpThreshold 25
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ covCellRrcConnWakeUpThreshold 30
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ coverageCellDiscovery true
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ capCellSleepProhibitInterval 0
set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ isAllowedMsmOnCovCell true

set ENodeBFunction=1,EUtranCellFDD=.*,CellSleepFunction=1$ capCellSleepProhibitInterval 0


for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,CellSleepFunction=1$ sleepMode 1
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,CellSleepFunction=1$ sleepMode 1
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,CellSleepFunction=1$ sleepMode 0
done

#################### TDD  ############################

set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ sleepMode 1
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ sleepStartTime 18:30
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ sleepEndTime 00:30
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ capCellSleepMonitorDurTimer 15
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ capCellDlPrbSleepThreshold 10
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ capCellRrcConnSleepThreshold 5
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ covCellWakeUpMonitorDurTimer 15
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ covCellDlPrbWakeUpThreshold 25
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ covCellRrcConnWakeUpThreshold 30
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1$ coverageCellDiscovery true

----------------  cellSleepCovCellMeasOn ---------------------------


set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ cellSleepCovCellMeasOn true


###############  AMS & CA Scripts ############################


set SystemFunctions=1,Lm=1,FeatureState=CXC4011476 featureState 1
set SystemFunctions=1,Lm=1,FeatureState=CXC4012123 featureState 0

set CXC4011958|CXC4011808|CXC4011803|CXC4011378 featureState 1

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ asmSCellDetection 3

set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=.*$ asmSCellDetection 3


set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ caTriggeredRedirectionActive true

set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ connectedModeMobilityPrio 1
set ENodeBFunction=1,EUtranCellTDD=.*,GeranFreqGroupRelation=1$ voicePrio -1


for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ voicePrio -1
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ voicePrio 0
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,GeranFreqGroupRelation=1$ voicePrio 0
done

#######################  22.Q2 Feature Massification #######################


##############  LTE PIM Detection in Baseband #################

set CXC4010955|CXC4011368|CXC4011842 featureState 0
set PreschedProfile=.* preschedulingDataSize 86
set PreschedProfile=.* preschedulingPeriod 5
set PreschedProfile=.* preschedulingDuration 200
set PreschedProfile=0 preschedulingSinrThreshold 20

##############  ASGH based Pre-Scheduling  ###################

set FeatureState=CXC4011715$ featureState 1
set FeatureState=CXC4012200$ featureState 0

############# Differential Uplink Power Contr ####################

set ENodeBFunction=1,EUtranCellTDD=.* ulPsdLoadThresholdSinrClpc 2
set ENodeBFunction=1,EUtranCellTDD=.* ulTxPsdDistrThr 40
set ENodeBFunction=1,EUtranCellTDD=.* p0ClpcExGoodEnabled false
set ENodeBFunction=1,EUtranCellTDD=.* p0ClpcExBadEnabled false
set ENodeBFunction=1,EUtranCellTDD=.* p0ClpcExBadSinrThr -10
set ENodeBFunction=1,EUtranCellTDD=.* p0ClpcExGoodSinrThr 21
set ENodeBFunction=1,EUtranCellTDD=.* p0ClpcExGoodSinrOffset64Qam 0
set ENodeBFunction=1,EUtranCellTDD=.* p0ClpcExGoodSinrOffset256Qam 0
set ENodeBFunction=1,EUtranCellTDD=.* assumedUePowerMsg3 1000

############### Increase number of GTP-U connec ######################


################  Atmospheric Duct Int Reduction  #########################

set ENodeBFunction=1,EUtranCellTDD=.* specialSubframePattern 7
set ENodeBFunction=1,EUtranCellTDD=.* ductIntOpMode 3
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntBgNoiseThr=-110
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqCorrPeakThr=20
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqPwrDiff=5
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntRedTriggerThr=8
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntRedRecovThr=2
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqPwrThr=-105
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntSlopePwrDiffThr=3
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectPeriod=10
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntSlopeDetectRatioThr=50
set ENodeBFunction=1,EUtranCellTDD=.* ductIntPerfTuning ductIntCharSeqTransThr=3
set ENodeBFunction=1 ductIntCharInfoScheme 0
set ENodeBFunction=1 ductIntFlexibleDetectionEnabled false
set CXC4012256 featureState 1

################# Dyn SCell Selection for CA ###########


###############


lt all
gs+
confbd+
st cell

### LMS WITHOUT LAYER FLIP  ####

set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=1451$ cellReselectionPriority 5
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=265$ cellReselectionPriority 6
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=3666$ cellReselectionPriority 4
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=3678$ cellReselectionPriority 4
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=40940$ cellReselectionPriority 7
set ENodeBFunction=1,EUtranCell.DD=.*,GeranFreqGroupRelation=1$ cellReselectionPriority 1

set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=1451$ connectedModeMobilityPrio 5
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=265$ connectedModeMobilityPrio 6
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=40940$ connectedModeMobilityPrio 7
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1451$ connectedModeMobilityPrio 5
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=265$ connectedModeMobilityPrio 6
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3666$ connectedModeMobilityPrio 4
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3678$ connectedModeMobilityPrio 4
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=40940$ connectedModeMobilityPrio 7
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1451$ connectedModeMobilityPrio 5
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=265$ connectedModeMobilityPrio 6
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3666$ connectedModeMobilityPrio -1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3678$ connectedModeMobilityPrio -1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=40940$ connectedModeMobilityPrio 7


set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1451$ voicePrio 6
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=265$ voicePrio 7
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3666$ voicePrio 5
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3678$ voicePrio 5
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=40940$ voicePrio -1
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1451$ voicePrio 6
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=265$ voicePrio 7
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3666$ voicePrio 3
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3678$ voicePrio 3
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=40940$ voicePrio 4


for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ connectedModeMobilityPrio 4
 set $mordn,EUtranFreqRelation=3678$ connectedModeMobilityPrio 4
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ connectedModeMobilityPrio 4
 set $mordn,EUtranFreqRelation=3678$ connectedModeMobilityPrio 4
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ connectedModeMobilityPrio 4
 set $mordn,EUtranFreqRelation=3678$ connectedModeMobilityPrio 4
done

for $mo in TDD41
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ connectedModeMobilityPrio -1
 set $mordn,EUtranFreqRelation=3678$ connectedModeMobilityPrio -1
done

### common ###

set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ interFreqMeasType 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA1A2SearchRsrp 20
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA1A2SearchRsrq 15
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ lbA5Thr1RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=.*$ qOffsetFreq 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=.*$ qOffsetFreq 0
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrq -195
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold2Rsrp -110
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold2Rsrq -195
set ENodeBFunction=1,EUtranCell.DD=.*,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrq 10

for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold1Rsrp -44
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold1Rsrp -44
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold1Rsrp -44
done

for $mo in TDD41
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold1Rsrp -110
done

### RSRP ###


set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrp -114
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrp -114

set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrp -114
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrp -114

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3666$ a5Thr1RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=3678$ a5Thr1RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=.*$ a5Thr1RsrpFreqOffset 0

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=1451$ a5Thr2RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=265$ a5Thr2RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=40940$ a5Thr2RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=1451$ a5Thr2RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=265$ a5Thr2RsrpFreqOffset 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3666$ a5Thr2RsrpFreqOffset 17
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=3678$ a5Thr2RsrpFreqOffset 17
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=40940$ a5Thr2RsrpFreqOffset 0

for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -110
 set $mordn,EUtranFreqRelation=1451$ a5Thr1RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=265$ a5Thr1RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=40940$ a5Thr1RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=3666$ a5Thr2RsrpFreqOffset 17
 set $mordn,EUtranFreqRelation=3678$ a5Thr2RsrpFreqOffset 17
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -110
 set $mordn,EUtranFreqRelation=1451$ a5Thr1RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=265$ a5Thr1RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=40940$ a5Thr1RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=3666$ a5Thr2RsrpFreqOffset 17
 set $mordn,EUtranFreqRelation=3678$ a5Thr2RsrpFreqOffset 17
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -105
 set $mordn,EUtranFreqRelation=1451$ a5Thr1RsrpFreqOffset 8
 set $mordn,EUtranFreqRelation=265$ a5Thr1RsrpFreqOffset 8
 set $mordn,EUtranFreqRelation=40940$ a5Thr1RsrpFreqOffset 8
 set $mordn,EUtranFreqRelation=3666$ a5Thr2RsrpFreqOffset 0
 set $mordn,EUtranFreqRelation=3678$ a5Thr2RsrpFreqOffset 0
done

### RSRQ ###

set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrq -165
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrq -165

set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrq -195
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrq -195

set ENodeBFunction=1,EUtranCellFDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrq -195
set ENodeBFunction=1,EUtranCellTDD=.*,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrq -195

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ a5Thr1RsrqFreqOffset 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=.*$ a5Thr1RsrqFreqOffset 0

set ENodeBFunction=1,EUtranCellFDD=.*,EUtranFreqRelation=.*$ a5Thr2RsrqFreqOffset 0
set ENodeBFunction=1,EUtranCellTDD=.*,EUtranFreqRelation=.*$ a5Thr2RsrqFreqOffset 0

############ IFLB ############

set L2100 cellCapMinCellSubCap 12740
set L1800 cellCapMinCellSubCap 8500
set L900 cellCapMinCellSubCap 4240
set L2100 cellCapMaxCellSubCap 38240
set L1800 cellCapMaxCellSubCap 25500
set L900 cellCapMaxCellSubCap 12740
set TDD41 cellCapMaxCellSubCap 36000
set L2100 cellCapMinMaxWriProt true
set L1800 cellCapMinMaxWriProt true
set L900 cellCapMinMaxWriProt true
set TDD41 cellCapMinMaxWriProt false


###################################


set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=1451$ voicePrio 6
set ENodeBFunction=1,EUtranCell.DD=.*,EUtranFreqRelation=265$ voicePrio 7

cvms pre_dotparameter

set ENodeBFunction=1,AdmissionControl=1 paArpOverrideHpa 0


cvms post_dotparameter


set CXC4012017 featureState 1
set CXC4012015 featureState 1
set CXC4012026 featureState 1
set CXC4011018 featureState 1


confb+


set . vswrSupervisionSensitivity 100
set RfPort=A$ vswrSupervisionActive true
set RfPort=C$ vswrSupervisionActive true
set RfPort=D$ vswrSupervisionActive true


########## Vi reference node active features (not in Airtel GPL list) ##########
$date = `date +%y%m%d_%H%M`
cvms Pre_Vi_Features_$date

set Lm=1,FeatureState=CXC4011567$ featureState 1    # SUPPLEMENTARY DL ONLY CELL
set Lm=1,FeatureState=CXC4011955$ featureState 1    # Dynamic Pucch
set Lm=1,FeatureState=CXC4011980$ featureState 1    # 4CC DL Carrier Aggregation Extension
set Lm=1,FeatureState=CXC4012016$ featureState 1    # Mixed Mode Baseband WCDMA
set Lm=1,FeatureState=CXC4012111$ featureState 1    # Global SCell Evaluation for Carrier Aggregation
set Lm=1,FeatureState=CXC4012157$ featureState 1    # High Power UE
set Lm=1,FeatureState=CXC4012199$ featureState 1    # ASGH Performance Package
set Lm=1,FeatureState=CXC4012453$ featureState 1    # VoLTE Inactivity Timer Extension
set Lm=1,FeatureState=CXC4012485$ featureState 1    # Optimized RRC Connection Release Control
set Lm=1,FeatureState=CXC4012533$ featureState 1    # LTE AI Powered MIMO Sleep Mode
set Lm=1,FeatureState=CXC4012603$ featureState 1    # Uplink-Triggered VoLTE Mobility
set Lm=1,FeatureState=CXC4020001$ featureState 1    # HSDPA Dynamic Code Allocation
set Lm=1,FeatureState=CXC4020002$ featureState 1    # 
set Lm=1,FeatureState=CXC4020003$ featureState 1    # HSDPA Flexible Scheduler
set Lm=1,FeatureState=CXC4020005$ featureState 1    # Enhanced Uplink Introduction Package
set Lm=1,FeatureState=CXC4020008$ featureState 1    # HSDPA Incremental Redundancy
set Lm=1,FeatureState=CXC4020010$ featureState 1    # RTT positioning
set Lm=1,FeatureState=CXC4020011$ featureState 1    # Enhanced Uplink, 2ms TTI
set Lm=1,FeatureState=CXC4020012$ featureState 1    # 
set Lm=1,FeatureState=CXC4020013$ featureState 1    # Enhanced Layer2
set Lm=1,FeatureState=CXC4020014$ featureState 1    # Support for 64 QAM
set Lm=1,FeatureState=CXC4020016$ featureState 1    # 
set Lm=1,FeatureState=CXC4020022$ featureState 1    # 
set Lm=1,FeatureState=CXC4020025$ featureState 1    # Fractional DPCH and SRB on HS
set Lm=1,FeatureState=CXC4020029$ featureState 1    # Multi Carrier
set Lm=1,FeatureState=CXC4020030$ featureState 1    # EUL single HARQ process scheduling
set Lm=1,FeatureState=CXC4020031$ featureState 1    # 
set Lm=1,FeatureState=CXC4020032$ featureState 1    # Multi Carrier Inactivity Control
set Lm=1,FeatureState=CXC4020035$ featureState 1    # 
set Lm=1,FeatureState=CXC4020036$ featureState 1    # Dual-Band HSDPA Multi-Carrier
set Lm=1,FeatureState=CXC4020040$ featureState 1    # 
set Lm=1,FeatureState=CXC4020041$ featureState 1    # 
set Lm=1,FeatureState=CXC4020042$ featureState 1    # 
set Lm=1,FeatureState=CXC4020043$ featureState 1    # High-speed downlink for FACH
set Lm=1,FeatureState=CXC4020051$ featureState 1    # Mixed Mode Radio WCDMA
set Lm=1,FeatureState=CXC4020054$ featureState 1    # EUL DCH Load Balancing
set Lm=1,FeatureState=CXC4020055$ featureState 1    # Battery efficiency for high-speed FACH
set Lm=1,FeatureState=CXC4020059$ featureState 1    # 
set Lm=1,FeatureState=CXC4020061$ featureState 1    # Interference Suppression
set Lm=1,FeatureState=CXC4020063$ featureState 1    # 
set Lm=1,FeatureState=CXC4020066$ featureState 1    # Uplink Fast Congestion Control
set Lm=1,FeatureState=CXC4020068$ featureState 1    # 
set Lm=1,FeatureState=CXC4020069$ featureState 1    # CE Extension for EUL
set Lm=1,FeatureState=CXC4020070$ featureState 1    # Interference Suppression for EUL 10 ms
set Lm=1,FeatureState=CXC4020072$ featureState 1    # 
set Lm=1,FeatureState=CXC4020073$ featureState 1    # 
set Lm=1,FeatureState=CXC4020075$ featureState 1    # Channel Element Efficiency for EUL
set Lm=1,FeatureState=CXC4020079$ featureState 1    # HSDPA Dynamic Power Sharing
set Lm=1,FeatureState=CXC4020081$ featureState 1    # Narrowband Interference Rejection
set Lm=1,FeatureState=CXC4020084$ featureState 1    # Increased Cell Carrier Support
set Lm=1,FeatureState=CXC4020086$ featureState 1    # Low Latency Pre-Scheduling for EUL
set Lm=1,FeatureState=CXC4020090$ featureState 1    # 
set Lm=1,FeatureState=CXC4020091$ featureState 1    # Uplink Coordinated Multi-Point Reception
set Lm=1,FeatureState=CXC4020102$ featureState 1    # HSDPA Mixed Mode Dynamic Power Sharing
set Lm=1,FeatureState=CXC4021014$ featureState 1    # Channel Element Capacity for EUL Smartphones
set Lm=1,FeatureState=CXC4030037$ featureState 1    # 
set Lm=1,FeatureState=CXC4040002$ featureState 1    # Ethernet Link Aggregation
set Lm=1,FeatureState=CXC4040003$ featureState 1    # 
set Lm=1,FeatureState=CXC4040007$ featureState 1    # PTP Slave for Frequency Synchronization
set Lm=1,FeatureState=CXC4040011$ featureState 1    # Synchronous Ethernet
set Lm=1,FeatureState=CXC4040016$ featureState 1    # Two-Way Active Measurement Protocol Initiator

$date = `date +%y%m%d_%H%M`
cvms Post_Vi_Features_$date

$date = `date +%y%m%d_%H%M`
cvms Baseline_Updated_$date

confbd-
gs-

for $mo in L2100
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ voicePrio 5
 set $mordn,EUtranFreqRelation=3678$ voicePrio 5
 set $mordn,EUtranFreqRelation=40940$ voicePrio -1
done

for $mo in L1800
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ voicePrio 5
 set $mordn,EUtranFreqRelation=3678$ voicePrio 5
 set $mordn,EUtranFreqRelation=40940$ voicePrio -1
done

for $mo in L900
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ voicePrio 5
 set $mordn,EUtranFreqRelation=3678$ voicePrio 5
 set $mordn,EUtranFreqRelation=40940$ voicePrio -1
done

for $mo in TDD41
 $mordn = rdn($mo)
 set $mordn,EUtranFreqRelation=3666$ voicePrio 3
 set $mordn,EUtranFreqRelation=3678$ voicePrio 3
 set $mordn,EUtranFreqRelation=40940$ voicePrio 4
done
"""


RJ_Vi_TN_RN_GPS_MME_SCRIPT = """
crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 4 5 6 7
pcp1 8 9 10 11 12 13 14 15
pcp2 16 17 18 19 20 21 22 23
pcp3 24 25 26 27 28 29 30 31
pcp4 32 33 34 35 36 37 38 39
pcp5 40 41 42 43 44 45 46 47
pcp6 48 49 50 51 52 53 54 55
pcp7 56 57 58 59 60 61 62 63
userLabel Traffic
end
#END Transport=1,QosProfiles=1,DscpPcpMap=1 --------------------

ld Transport=1,EthernetPort=TN_IDL_B
lset Transport=1,EthernetPort=TN_IDL_B$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_CP,InterfaceIPv6=LTE_CP
lset Transport=1,Router=LTE_CP,InterfaceIPv6=LTE_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP
lset Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_OM,InterfaceIPv6=LTE_OM
lset Transport=1,Router=LTE_OM,InterfaceIPv6=LTE_OM$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTE_UP,TwampResponder=1
ipAddress Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP,AddressIPv6=LTE_UP
udpPort 4001
userLabel User Plane
end
#END Transport=1,Router=LTE_UP,TwampResponder=1 --------------------

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 10
betaIndex 2
bundlingActivated true
bundlingTimer 10
cookieLife 60
dscp 48
hbMaxBurst 1
heartbeatInterval 30000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 350
maxActivateThr 65535
maxBurst 4
maxInitRt 8
maxInStreams 2
maxOutStreams 2
maxRto 500
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 300
pathMaxRtx 5
primaryPathMaxRtx 0
sackTimer 40
transmitBufferSize 64
userLabel SCTP
end
#END Transport=1,SctpProfile=1 --------------------

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTE_CP,InterfaceIPv6=LTE_CP,AddressIPv6=LTE_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end
#END Transport=1,SctpEndpoint=1 --------------------

#END Transport=1,Router=LTE_UP,TwampResponder=1 --------------------

ld Transport=1,Synchronization=1 #SystemCreated
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1


crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1 --------------------

crn Transport=1,Synchronization=1,TimeSyncIO=1
compensationDelay 0
encapsulation Equipment=1,FieldReplaceableUnit=BB-1,SyncPort=1
filterTime 12
end
#END Transport=1,Synchronization=1,TimeSyncIO=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Synchronization=1,TimeSyncIO=1
priority 1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=1 --------------------

crn Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2
adminQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
administrativeState 1
encapsulation Transport=1,Ptp=1,BoundaryOrdinaryClock=PTP1
priority 2
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2 --------------------

gs-
confb-

crn ENodeBFunction=1
eNodeBPlmnId mcc=404,mnc=60,mncLength=2
dscpLabel 48
eNBId {eNBId}
forcedSiTunnelingActive true
gtpuErrorIndicationDscp 48
interEnbCaTunnelDscp 34
interEnbUlCompTunnelDscp 34
maxNoCellsNaccCsfb 4
s1GtpuEchoDscp 48
sctpRef Transport=1,SctpEndpoint=1
upIpAddressRef Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP,AddressIPv6=LTE_UP
x2GtpuEchoDscp 48
end
#END ENodeBFunction=1 --------------------

# Paging: maxNoOfPagingRecords 7 before the cells (cell creation can fail above 7, e.g. L900 5 MHz)
set ENodeBFunction=1,Paging=1 maxNoOfPagingRecords 7



crn ENodeBFunction=1,GeraNetwork=1
end
#END ENodeBFunction=1,GeraNetwork=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
frequencyGroupId 1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=2
frequencyGroupId 2
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=57
arfcnValueGeranDl 57
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=58
arfcnValueGeranDl 58
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=59
arfcnValueGeranDl 59
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=60
arfcnValueGeranDl 60
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=61
arfcnValueGeranDl 61
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=62
arfcnValueGeranDl 62
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=72
arfcnValueGeranDl 72
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=73
arfcnValueGeranDl 73
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=74
arfcnValueGeranDl 74
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=75
arfcnValueGeranDl 75
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=76
arfcnValueGeranDl 76
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=77
arfcnValueGeranDl 77
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=78
arfcnValueGeranDl 78
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=79
arfcnValueGeranDl 79
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=80
arfcnValueGeranDl 80
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=81
arfcnValueGeranDl 81
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=82
arfcnValueGeranDl 82
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=83
arfcnValueGeranDl 83
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=84
arfcnValueGeranDl 84
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=default #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ aqmMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dscp 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ pdb 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ priority 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ bitRateRecommendationEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ counterActiveMode true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlMaxHARQTxQci 7
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ drxPriority 99
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ drxProfileRef ENodeBFunction=1,DrxProfile=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ endcProfileRef ENodeBFunction=1,EndcProfile=VOIP
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ inactivityTimerOffset 30
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ pdb 80
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ pdbOffset 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rlcMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ priority 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 20
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rlcSNLength 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rlfPriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rlfProfileRef ENodeBFunction=1,RlfProfile=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rohcEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ serviceType 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ schedulingAlgorithm 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ tReorderingDl 75
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ tReorderingUl 75
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ ulMaxHARQTxQci 7
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dlMinBitRate 384
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ drxProfileRef ENodeBFunction=1,DrxProfile=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dscp 44
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ inactivityTimerOffset 30
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdb 150
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdbOffset 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ rlcMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ priority 4
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMinBitRate 384
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dscp 42
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ pdb 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ priority 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dscp 39
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ priority 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ absPrioOverride 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ aqmMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ drxPriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dscp 48
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ endcProfileRef ENodeBFunction=1,EndcProfile=IMS_SIGNALING
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ pdb 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ priority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ serviceType 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ tReorderingDl 75
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ aqmMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dscp 38
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ endcProfileRef ENodeBFunction=1,EndcProfile=MBB
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ lessMaxDelayThreshold 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ priority 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 200
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ relativePriority 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rohcForUlDataEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdb 75
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdbOffset 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ priority 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ serviceType 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ pdb 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ pdbOffset 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ priority 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ serviceType 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ aqmMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dscp 38
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdb 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ priority 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ serviceType 4
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ aqmMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dscp 36
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ endcProfileRef ENodeBFunction=1,EndcProfile=MBB
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ lessMaxDelayThreshold 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdb 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ priority 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 200
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ relativePriority 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rohcForUlDataEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ tReorderingUl 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ aqmMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dscp 38
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ pdb 200
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ priority 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ priorityFraction 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ resourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ aqmMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ endcProfileRef ENodeBFunction=1,EndcProfile=MBB
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ lessMaxDelayThreshold 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ priority 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 200
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ relativePriority 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rohcForUlDataEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ tReorderingUl 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ aqmMode 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dlResourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ endcProfileRef ENodeBFunction=1,EndcProfile=MBB
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ lessMaxDelayThreshold 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ priority 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 200
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ relativePriority 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rohcForUlDataEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ tReorderingUl 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 #SystemCreated
lset ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ dlMaxRetxThreshold 16
lset ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ ulMaxRetxThreshold 32

ld ENodeBFunction=1,Rcs=1 #SystemCreated
lset ENodeBFunction=1,Rcs=1$ tInactivityTimer 10

ld ENodeBFunction=1,Rrc=1 #SystemCreated
lset ENodeBFunction=1,Rrc=1$ t300 1000
lset ENodeBFunction=1,Rrc=1$ t301 1000
lset ENodeBFunction=1,Rrc=1$ t311 10000

set 0 Userlabel {Phy_SiteID_Userlabel}

confb-
gs-

#######################DUAL STACK SCRIPT##############################

gs+

# IPv4 CP/UP (InterfaceIPv4, AddressIPv4, RouteTableIPv4Static 3/2) are created by the 01 SiteBasic
lset Transport=1,Router=LTE_CP,InterfaceIPv4=LTE_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
lset Transport=1,Router=LTE_UP,InterfaceIPv4=LTE_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1
gs-

{DUAL_STACK_SCTP}



#######################MME############################################

gs+

crn ENodeBFunction=1,TermPointToMme=INVIRJ18JPR1MMEX02ER
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 203.88.21.249
ipAddress2 203.88.21.250
ipv6Address1 2402:3a80:14fe::178
ipv6Address2 2402:3a80:14fe::179
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=INVIRJ18VKI1MMEX01ER
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 112.110.99.176
ipAddress2 112.110.99.177
ipv6Address1 2402:3a80:1072::2a
ipv6Address2 2402:3a80:1072::2b
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=RAJ-VKI-SGSN1
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 203.88.10.116
ipAddress2 203.88.10.117
ipv6Address1 2402:8100:001a:0:0:0:0:040e
ipv6Address2 2402:8100:001a:0:0:0:0:040f
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=RAJJPRESG03
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 203.88.10.165
ipAddress2 203.88.10.166
ipv6Address1 2402:3a80:14fe::74
ipv6Address2 2402:3a80:14fe::75
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=RJSGSN02
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 203.88.10.83
ipAddress2 203.88.10.84
ipv6Address1 2402:8100:001a:0:0:0:0:040c
ipv6Address2 2402:8100:001a:0:0:0:0:040d
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

gs-

####################################External Alarm Definition###########################



gs+

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=1
administrativeState 1
alarmInExternalMe false
alarmSlogan MAINS FAIL
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 2
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=2
administrativeState 1
alarmInExternalMe false
alarmSlogan SITE ON BATTERY
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 3
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=3
administrativeState 1
alarmInExternalMe false
alarmSlogan LOW BATTERY VOLTAGE
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 4
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=4
administrativeState 1
alarmInExternalMe false
alarmSlogan DG ON LOAD
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 3
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=5
administrativeState 1
alarmInExternalMe false
alarmSlogan DOOR OPEN
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 3
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=6
administrativeState 1
alarmInExternalMe false
alarmSlogan DG FAIL TO START
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 2
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=7
administrativeState 1
alarmInExternalMe false
alarmSlogan HIGH ROOM TEMPERATURE
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 2
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=8
administrativeState 1
alarmInExternalMe false
alarmSlogan FIRE AND SMOKE
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 2
userLabel
end

gs-
"""


# GSM on the L900 radios (02 Cell_Def), values as on LO01INRJ207062 (25.Q2, Radio 2271 B0C, 2 Trx per sector) and
# LMWUKES02. The Abis transport (Router=GSM_ABIS, IPv4) is made by the 01 SiteBasic.
# BSC broker per BSC, from the nodes' AbisIp bscBrokerIpAddress - add a BSC here once its broker is known
# (Site_Basic BSC_Broker_IP overrides it).
RJ_VI_BSC_BROKER = {
    "RBSBP01": "10.161.8.131",      # LO01INRJ207062
    "RBSGN01": "10.190.68.131",     # LMWUKES02
}
RJ_VI_GSM_FEATURES = ["CXC4012017", "CXC4012026"]       # Mixed Mode Baseband GSM, Mixed Mode Radio GSM for Baseband
RJ_VI_GSM_TRX_PER_SECTOR = 2
RJ_VI_GSM_ABIS_IP = {"dscpSectorControlUL": 48, "initialRetransmissionPeriod": 1, "keepAlivePeriod": 1,
                     "maxRetransmission": 5, "retransmissionCap": 4}
# Trx: no rfBranchRxRef / rfBranchTxRef, as on the node (the Trx takes the SectorEquipmentFunction's RfBranches)
RJ_VI_GSM_TRX = {"arfcnMax": 84, "arfcnMin": 51, "combinedCellType": 0, "configuredMaxTxPower": 20000,
                 "frequencyBand": 8, "noOfRxAntennas": 2, "noOfTxAntennas": 1}


# 02 Cell_Def, top: the EUtranFrequencies of the RJ_Vi GPL (the cells' and their frequency relations' targets), each
# created only when missing, so neither a re-run nor the 03 GPL tries to create an existing one
RJ_Vi_EUTRAN_FREQUENCY_AMOS = """
####################### EUtranFrequency creation (before the cells; was in the 03 GPL) #######################

lt all
confbd+
gs+

pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1451$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1451
1451
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1476$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1476
1476
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=265$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=265
265
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=290$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=290
290
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=315$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=315
315
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3666$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3666
3666
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3678$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3678
3678
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40140$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40140
40140
0
fi
pr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940$
if $nr_of_mos = 0
cr ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
40940
0
fi

gs-
confbd-

"""
