DEL_Vi_GPL_LMS_DST_SCRIPT = """
lt all

cvms Pre_integration_L1800

set . auportref
set . rfportref
rdel rilink
rdel sec
rdel rru
rdel rru
lt all

bl cell|sec|rru

rdel  FieldReplaceableUnit=BB-1,RiPort=G
rdel  FieldReplaceableUnit=BB-1,RiPort=H
rdel  FieldReplaceableUnit=BB-1,RiPort=J
rdel  FieldReplaceableUnit=BB-1,RiPort=K

gs+
Confbd+
gs+

cr Equipment=1,FieldReplaceableUnit=RRU-22

cr Equipment=1,AntennaUnitGroup=22

cr Equipment=1,AntennaUnitGroup=22,AntennaUnit=1

cr Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1
cr Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=1
cr Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=2
cr Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=3
cr Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=4

cr Equipment=1,AntennaUnitGroup=22,RfBranch=1
cr Equipment=1,AntennaUnitGroup=22,RfBranch=2
cr Equipment=1,AntennaUnitGroup=22,RfBranch=3
cr Equipment=1,AntennaUnitGroup=22,RfBranch=4

set Equipment=1,AntennaUnitGroup=22,RfBranch=1 auPortRef Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=1
set Equipment=1,AntennaUnitGroup=22,RfBranch=2 auPortRef Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=2
set Equipment=1,AntennaUnitGroup=22,RfBranch=3 auPortRef Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=3
set Equipment=1,AntennaUnitGroup=22,RfBranch=4 auPortRef Equipment=1,AntennaUnitGroup=22,AntennaUnit=1,AntennaSubunit=1,AuPort=4

cr Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=A
cr Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=B
cr Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=C
cr Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=D

set Equipment=1,AntennaUnitGroup=22,RfBranch=1 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=A
set Equipment=1,AntennaUnitGroup=22,RfBranch=2 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=B
set Equipment=1,AntennaUnitGroup=22,RfBranch=3 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=C
set Equipment=1,AntennaUnitGroup=22,RfBranch=4 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-22,RfPort=D


cr Equipment=1,FieldReplaceableUnit=RRU-22,RiPort=DATA_1
cr Equipment=1,FieldReplaceableUnit=RRU-22,RiPort=DATA_2

cr NodeSupport=1,SectorEquipmentFunction=S22
set  NodeSupport=1,SectorEquipmentFunction=S22 rfBranchRef Equipment=1,AntennaUnitGroup=22,RfBranch=1 Equipment=1,AntennaUnitGroup=22,RfBranch=2 Equipment=1,AntennaUnitGroup=22,RfBranch=3 Equipment=1,AntennaUnitGroup=22,RfBranch=4

cr Equipment=1,FieldReplaceableUnit=RRU-21

cr Equipment=1,AntennaUnitGroup=21

cr Equipment=1,AntennaUnitGroup=21,AntennaUnit=1

cr Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1
cr Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=1
cr Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=2
cr Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=3
cr Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=4


cr Equipment=1,AntennaUnitGroup=21,RfBranch=1
cr Equipment=1,AntennaUnitGroup=21,RfBranch=2
cr Equipment=1,AntennaUnitGroup=21,RfBranch=3
cr Equipment=1,AntennaUnitGroup=21,RfBranch=4

set Equipment=1,AntennaUnitGroup=21,RfBranch=1 auPortRef Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=1
set Equipment=1,AntennaUnitGroup=21,RfBranch=2 auPortRef Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=2
set Equipment=1,AntennaUnitGroup=21,RfBranch=3 auPortRef Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=3
set Equipment=1,AntennaUnitGroup=21,RfBranch=4 auPortRef Equipment=1,AntennaUnitGroup=21,AntennaUnit=1,AntennaSubunit=1,AuPort=4


cr Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=A
cr Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=B
cr Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=C
cr Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=D

set Equipment=1,AntennaUnitGroup=21,RfBranch=1 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=A
set Equipment=1,AntennaUnitGroup=21,RfBranch=2 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=B
set Equipment=1,AntennaUnitGroup=21,RfBranch=3 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=C
set Equipment=1,AntennaUnitGroup=21,RfBranch=4 rfPortRef Equipment=1,FieldReplaceableUnit=RRU-21,RfPort=D


cr Equipment=1,FieldReplaceableUnit=RRU-21,RiPort=DATA_1
cr Equipment=1,FieldReplaceableUnit=RRU-21,RiPort=DATA_2

cr NodeSupport=1,SectorEquipmentFunction=S21
set  NodeSupport=1,SectorEquipmentFunction=S21 rfBranchRef Equipment=1,AntennaUnitGroup=21,RfBranch=1 Equipment=1,AntennaUnitGroup=21,RfBranch=2 Equipment=1,AntennaUnitGroup=21,RfBranch=3 Equipment=1,AntennaUnitGroup=21,RfBranch=4


crn Equipment=1,FieldReplaceableUnit=BB-1,RiPort=A
administrativeState 1
preferredSfpProductNumber
end


crn Equipment=1,FieldReplaceableUnit=BB-1,RiPort=B
administrativeState 1
preferredSfpProductNumber
end

########rilink'###########################################################################


cr Equipment=1,RiLink=22
Equipment=1,FieldReplaceableUnit=BB-1,RiPort=B
Equipment=1,FieldReplaceableUnit=RRU-22,RiPort=DATA_1

cr Equipment=1,RiLink=21
Equipment=1,FieldReplaceableUnit=BB-1,RiPort=A
Equipment=1,FieldReplaceableUnit=RRU-21,RiPort=DATA_1


########rilink'###########################################################################


gs+

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=4
administrativeState 1
alarmInExternalMe false
alarmSlogan LOAD ON DG
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 2
userLabel
end

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=3
administrativeState 1
alarmInExternalMe false
alarmSlogan RECTIFIER FAIL
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 3
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

crn Equipment=1,FieldReplaceableUnit=BB-1,AlarmPort=1
administrativeState 1
alarmInExternalMe false
alarmSlogan MAINS FAIL
filterAlgorithm 0
filterDelay 60
filterTime 0
normallyOpen true
perceivedSeverity 4
userLabel
end
gs-
bl sec|cell|rru

lt all

##########--------------------#############################################################

$eNBId = readinput(Enter eNBId Ex: 123456 : )
$tac = readinput(Enter tac Ex: 123456 : )
$pci21 = readinput(Enter pci21 Ex: 123456 : )
$pci22 = readinput(Enter pci22 Ex: 123456 : )
$pci23 = readinput(Enter pci23 Ex: 123456 : )


###########################################################################---------------------------.###################################################################################

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
userLabel DSCP-PCP-Map
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
userLabel LTE_UP
end
#END Transport=1,Router=LTE_UP,TwampResponder=1 --------------------

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 10
betaIndex 2
bundlingActivated true
bundlingTimer 0
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
eNodeBPlmnId mcc=404,mnc=11,mncLength=2
dscpLabel 48
eNBId $eNBId
gtpuErrorIndicationDscp 48
interEnbCaTunnelDscp 34
interEnbUlCompTunnelDscp 34
rrcConnReestActive true
s1GtpuEchoDscp 48
sctpRef Transport=1,SctpEndpoint=1
timeAndPhaseSynchAlignment true
upIpAddressRef Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP,AddressIPv6=LTE_UP
x2GtpuEchoDscp 48
end
#END ENodeBFunction=1 --------------------

gs-
confb-

cvms Pre_L1800_cell


crn ENodeBFunction=1,SectorCarrier=21
configuredMaxTxPower 80000
noOfRxAntennas 2
noOfTxAntennas 2
rfBranchRxRef Equipment=1,AntennaUnitGroup=21,RfBranch=1 Equipment=1,AntennaUnitGroup=21,RfBranch=2 
rfBranchTxRef Equipment=1,AntennaUnitGroup=21,RfBranch=1 Equipment=1,AntennaUnitGroup=21,RfBranch=2 
sectorFunctionRef NodeSupport=1,SectorEquipmentFunction=S21
end
#END ENodeBFunction=1,SectorCarrier=21 --------------------

crn ENodeBFunction=1,EUtranCellFDD=$nodenameF21
acBarringForCsfb acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoData acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoSignalling acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringPresence acBarringForCsfbPresence=0,acBarringForMoDataPresence=0,acBarringForMoSignPresence=0
changeNotification changeNotificationSIB1=false,changeNotificationSIB13=true,changeNotificationSIB15=false,changeNotificationSIB16=false,changeNotificationSIB2=false,changeNotificationSIB3=false,changeNotificationSIB4=false,changeNotificationSIB5=true,changeNotificationSIB6=false,changeNotificationSIB7=false,changeNotificationSIB8=false
frameStartOffset subFrameOffset=0
mappingInfo mappingInfoSIB10=1,mappingInfoSIB11=0,mappingInfoSIB12=7,mappingInfoSIB15=0,mappingInfoSIB16=0,mappingInfoSIB3=6,mappingInfoSIB4=0,mappingInfoSIB5=3,mappingInfoSIB6=4,mappingInfoSIB7=0,mappingInfoSIB8=0
siPeriodicity siPeriodicitySI1=8,siPeriodicitySI10=64,siPeriodicitySI2=64,siPeriodicitySI3=64,siPeriodicitySI4=64,siPeriodicitySI5=64,siPeriodicitySI6=64,siPeriodicitySI7=64,siPeriodicitySI8=64,siPeriodicitySI9=64
ssacBarringForMMTELVideo acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
ssacBarringForMMTELVoice acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
systemInformationBlock3 nCellChangeHigh=16,nCellChangeMedium=16,qHyst=4,qHystSfHigh=0,qHystSfMedium=0,sIntraSearch=44,sIntraSearchP=44,sIntraSearchQ=0,sIntraSearchv920Active=false,sNonIntraSearch=10,sNonIntraSearchP=10,sNonIntraSearchQ=0,sNonIntraSearchv920Active=false,tEvaluation=240,threshServingLowQ=1000,tHystNormal=240
systemInformationBlock6 tReselectionUtra=2,tReselectionUtraSfHigh=100,tReselectionUtraSfMedium=100
systemInformationBlock7 tReselectionGeran=2,tReselectionGeranSfHigh=100,tReselectionGeranSfMedium=100
systemInformationBlock8 searchWindowSizeCdma=8,tReselectionCdma1xRtt=2,tReselectionCdma1xRttSfHigh=100,tReselectionCdma1xRttSfMedium=100,tReselectionCdmaHrpd=2,tReselectionCdmaHrpdSfHigh=100,tReselectionCdmaHrpdSfMedium=100
additionalPlmnAlarmSupprList false false false false false
additionalPlmnReservedList false false false false false
advCellSupAction 2
advCellSupSensitivity 25
alpha 10
cellId 21
cellRange 4
cfraEnable true
covTriggerdBlindHoAllowed true
crsGain 0
dlChannelBandwidth 10000
dlInterferenceManagementActive true
drxActive true
earfcndl 1421
earfcnul 19421
mobCtrlAtPoorCovActive true
noOfPucchCqiUsers 160
noOfPucchSrUsers 160
pdcchCfiMode 5
pdcchPowerBoostMax 0
pdschTypeBGain 0
physicalLayerCellIdGroup $pci21
physicalLayerSubCellId 0
preambleInitialReceivedTargetPower -110
pZeroNominalPucch -117
pZeroNominalPusch -103
qQualMin -34
qRxLevMin -124
rachRootSequence 748
sectorCarrierRef ENodeBFunction=1,SectorCarrier=21
tac 40014
threshServingLow 8
ulChannelBandwidth 10000
ulInterferenceManagementActive true
userLabel ZZ_$nodenameF21
end
#END ENodeBFunction=1,EUtranCellFDD=$nodenameF21 --------------------

crn ENodeBFunction=1,SectorCarrier=22
configuredMaxTxPower 80000
noOfRxAntennas 2
noOfTxAntennas 2
rfBranchRxRef Equipment=1,AntennaUnitGroup=21,RfBranch=3 Equipment=1,AntennaUnitGroup=21,RfBranch=4
rfBranchTxRef Equipment=1,AntennaUnitGroup=21,RfBranch=3 Equipment=1,AntennaUnitGroup=21,RfBranch=4
sectorFunctionRef NodeSupport=1,SectorEquipmentFunction=S21
end
#END ENodeBFunction=1,SectorCarrier=22 --------------------

crn ENodeBFunction=1,EUtranCellFDD=$nodenameF22
acBarringForCsfb acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoData acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoSignalling acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringPresence acBarringForCsfbPresence=0,acBarringForMoDataPresence=0,acBarringForMoSignPresence=0
changeNotification changeNotificationSIB1=false,changeNotificationSIB13=true,changeNotificationSIB15=false,changeNotificationSIB16=false,changeNotificationSIB2=false,changeNotificationSIB3=false,changeNotificationSIB4=false,changeNotificationSIB5=true,changeNotificationSIB6=false,changeNotificationSIB7=false,changeNotificationSIB8=false
frameStartOffset subFrameOffset=0
mappingInfo mappingInfoSIB10=1,mappingInfoSIB11=0,mappingInfoSIB12=7,mappingInfoSIB15=0,mappingInfoSIB16=0,mappingInfoSIB3=6,mappingInfoSIB4=0,mappingInfoSIB5=3,mappingInfoSIB6=4,mappingInfoSIB7=0,mappingInfoSIB8=0
siPeriodicity siPeriodicitySI1=8,siPeriodicitySI10=64,siPeriodicitySI2=64,siPeriodicitySI3=64,siPeriodicitySI4=64,siPeriodicitySI5=64,siPeriodicitySI6=64,siPeriodicitySI7=64,siPeriodicitySI8=64,siPeriodicitySI9=64
ssacBarringForMMTELVideo acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
ssacBarringForMMTELVoice acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
systemInformationBlock3 nCellChangeHigh=16,nCellChangeMedium=16,qHyst=4,qHystSfHigh=0,qHystSfMedium=0,sIntraSearch=44,sIntraSearchP=44,sIntraSearchQ=0,sIntraSearchv920Active=false,sNonIntraSearch=10,sNonIntraSearchP=10,sNonIntraSearchQ=0,sNonIntraSearchv920Active=false,tEvaluation=240,threshServingLowQ=1000,tHystNormal=240
systemInformationBlock6 tReselectionUtra=2,tReselectionUtraSfHigh=100,tReselectionUtraSfMedium=100
systemInformationBlock7 tReselectionGeran=2,tReselectionGeranSfHigh=100,tReselectionGeranSfMedium=100
systemInformationBlock8 searchWindowSizeCdma=8,tReselectionCdma1xRtt=2,tReselectionCdma1xRttSfHigh=100,tReselectionCdma1xRttSfMedium=100,tReselectionCdmaHrpd=2,tReselectionCdmaHrpdSfHigh=100,tReselectionCdmaHrpdSfMedium=100
additionalPlmnAlarmSupprList false false false false false
additionalPlmnReservedList false false false false false
advCellSupAction 2
advCellSupSensitivity 25
alpha 10
cellId 22
cellRange 4
cfraEnable true
covTriggerdBlindHoAllowed true
crsGain 0
dlChannelBandwidth 10000
dlInterferenceManagementActive true
drxActive true
earfcndl 1421
earfcnul 19421
mobCtrlAtPoorCovActive true
noOfPucchCqiUsers 160
noOfPucchSrUsers 160
pdcchCfiMode 5
pdcchPowerBoostMax 0
pdschTypeBGain 0
physicalLayerCellIdGroup $pci22
physicalLayerSubCellId 1
preambleInitialReceivedTargetPower -110
pZeroNominalPucch -117
pZeroNominalPusch -103
qQualMin -34
qRxLevMin -124
rachRootSequence 768
sectorCarrierRef ENodeBFunction=1,SectorCarrier=22
tac 40014
threshServingLow 8
ulChannelBandwidth 10000
ulInterferenceManagementActive true
userLabel ZZ_$nodenameF22
end
#END ENodeBFunction=1,EUtranCellFDD=$nodenameF22 --------------------

crn ENodeBFunction=1,SectorCarrier=23
configuredMaxTxPower 80000
noOfRxAntennas 4
noOfTxAntennas 4
rfBranchRxRef Equipment=1,AntennaUnitGroup=22,RfBranch=1 Equipment=1,AntennaUnitGroup=22,RfBranch=2 Equipment=1,AntennaUnitGroup=22,RfBranch=3 Equipment=1,AntennaUnitGroup=22,RfBranch=4
rfBranchTxRef Equipment=1,AntennaUnitGroup=22,RfBranch=1 Equipment=1,AntennaUnitGroup=22,RfBranch=2 Equipment=1,AntennaUnitGroup=22,RfBranch=3 Equipment=1,AntennaUnitGroup=22,RfBranch=4
sectorFunctionRef NodeSupport=1,SectorEquipmentFunction=S22
end
#END ENodeBFunction=1,SectorCarrier=23 --------------------

crn ENodeBFunction=1,EUtranCellFDD=$nodenameF23
acBarringForCsfb acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoData acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringForMoSignalling acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
acBarringPresence acBarringForCsfbPresence=0,acBarringForMoDataPresence=0,acBarringForMoSignPresence=0
changeNotification changeNotificationSIB1=false,changeNotificationSIB13=true,changeNotificationSIB15=false,changeNotificationSIB16=false,changeNotificationSIB2=false,changeNotificationSIB3=false,changeNotificationSIB4=false,changeNotificationSIB5=true,changeNotificationSIB6=false,changeNotificationSIB7=false,changeNotificationSIB8=false
frameStartOffset subFrameOffset=0
mappingInfo mappingInfoSIB10=1,mappingInfoSIB11=0,mappingInfoSIB12=7,mappingInfoSIB15=0,mappingInfoSIB16=0,mappingInfoSIB3=6,mappingInfoSIB4=0,mappingInfoSIB5=3,mappingInfoSIB6=4,mappingInfoSIB7=0,mappingInfoSIB8=0
siPeriodicity siPeriodicitySI1=8,siPeriodicitySI10=64,siPeriodicitySI2=64,siPeriodicitySI3=64,siPeriodicitySI4=64,siPeriodicitySI5=64,siPeriodicitySI6=64,siPeriodicitySI7=64,siPeriodicitySI8=64,siPeriodicitySI9=64
ssacBarringForMMTELVideo acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
ssacBarringForMMTELVoice acBarringFactor=95,acBarringForSpecialAC=false false false false false,acBarringTime=64
systemInformationBlock3 nCellChangeHigh=16,nCellChangeMedium=16,qHyst=4,qHystSfHigh=0,qHystSfMedium=0,sIntraSearch=44,sIntraSearchP=44,sIntraSearchQ=0,sIntraSearchv920Active=false,sNonIntraSearch=10,sNonIntraSearchP=10,sNonIntraSearchQ=0,sNonIntraSearchv920Active=false,tEvaluation=240,threshServingLowQ=1000,tHystNormal=240
systemInformationBlock6 tReselectionUtra=2,tReselectionUtraSfHigh=100,tReselectionUtraSfMedium=100
systemInformationBlock7 tReselectionGeran=2,tReselectionGeranSfHigh=100,tReselectionGeranSfMedium=100
systemInformationBlock8 searchWindowSizeCdma=8,tReselectionCdma1xRtt=2,tReselectionCdma1xRttSfHigh=100,tReselectionCdma1xRttSfMedium=100,tReselectionCdmaHrpd=2,tReselectionCdmaHrpdSfHigh=100,tReselectionCdmaHrpdSfMedium=100
additionalPlmnAlarmSupprList false false false false false
additionalPlmnReservedList false false false false false
advCellSupAction 2
advCellSupSensitivity 25
alpha 10
cellId 23
cellRange 4
cfraEnable true
covTriggerdBlindHoAllowed true
crsGain 0
dlChannelBandwidth 10000
dlInterferenceManagementActive true
drxActive true
earfcndl 1421
earfcnul 19421
mobCtrlAtPoorCovActive true
noOfPucchCqiUsers 160
noOfPucchSrUsers 160
pdcchCfiMode 5
pdcchPowerBoostMax 0
pdschTypeBGain 0
physicalLayerCellIdGroup 92
physicalLayerSubCellId 2
preambleInitialReceivedTargetPower -110
pZeroNominalPucch -117
pZeroNominalPusch -103
qQualMin -34
qRxLevMin -124
rachRootSequence 798
sectorCarrierRef ENodeBFunction=1,SectorCarrier=23
tac 40014
threshServingLow 8
ulChannelBandwidth 10000
ulInterferenceManagementActive true
userLabel ZZ_$nodenameF23
end
#END ENodeBFunction=1,EUtranCellFDD=$nodenameF23 --------------------

confb+
gs+

cvms post_L1800_CELL

crn ENodeBFunction=1,GeraNetwork=1
end
#END ENodeBFunction=1,GeraNetwork=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
frequencyGroupId 1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=597
arfcnValueGeranDl 597
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=597 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=598
arfcnValueGeranDl 598
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=598 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=599
arfcnValueGeranDl 599
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=599 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=644
arfcnValueGeranDl 644
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=644 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=645
arfcnValueGeranDl 645
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=645 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=646
arfcnValueGeranDl 646
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=646 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=647
arfcnValueGeranDl 647
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=647 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=648
arfcnValueGeranDl 648
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=648 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=649
arfcnValueGeranDl 649
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=649 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=643
arfcnValueGeranDl 643
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=643 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=601
arfcnValueGeranDl 601
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=601 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=640
arfcnValueGeranDl 640
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=640 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=639
arfcnValueGeranDl 639
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=639 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=603
arfcnValueGeranDl 603
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=603 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=605
arfcnValueGeranDl 605
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=605 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=638
arfcnValueGeranDl 638
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=638 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=600
arfcnValueGeranDl 600
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=600 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=641
arfcnValueGeranDl 641
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=641 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=602
arfcnValueGeranDl 602
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=602 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=604
arfcnValueGeranDl 604
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=604 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=606
arfcnValueGeranDl 606
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=606 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=607
arfcnValueGeranDl 607
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=607 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=636
arfcnValueGeranDl 636
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=636 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=637
arfcnValueGeranDl 637
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=637 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=642
arfcnValueGeranDl 642
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=642 --------------------

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=default #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ aqmMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dscp 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ pdb 300
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ drxPriority 98
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ drxProfileRef ENodeBFunction=1,DrxProfile=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ inactivityTimerOffset 20
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rlcSNLength 10
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dscp 44
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdb 150
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdbOffset 0
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dscp 42
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dscp 39
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ drxProfileRef ENodeBFunction=1,DrxProfile=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dscp 48
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=2
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ serviceType 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ tReorderingDl 35
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dscp 38
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ priority 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ relativePriority 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rohcForUlDataEnabled false
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdb 75
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdbOffset 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ priority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ priorityFraction 7
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdb 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ priority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ priorityFraction 5
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dscp 36
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdb 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ priority 7
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ relativePriority 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ tReorderingUl 35
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ priority 8
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ relativePriority 20
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ tReorderingUl 35
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ priority 9
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ relativePriority 20
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ tReorderingUl 35
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
lset ENodeBFunction=1,Rrc=1$ t301 400
lset ENodeBFunction=1,Rrc=1$ t311 3000

gs+

crn ENodeBFunction=1,TermPointToMme=INVIDL13NOD1MMEX02NK
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 0.0.0.0
ipAddress2 0.0.0.0
ipv6Address1 2402:8100:17:19c::32
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=INVIDL13NOD1MMEX01NK
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 0.0.0.0
ipAddress2 0.0.0.0
ipv6Address1 2402:8100:17:18c::32
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=INVIDL13GUR1MMEX02NK
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 112.110.107.23
ipAddress2 0.0.0.0
ipv6Address1 2402:8100:17:175c::32
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end

crn ENodeBFunction=1,TermPointToMme=INVIDL13GUR1MMEX01NK
additionalCnRef
administrativeState 1
dcnType 0
domainName
ipAddress1 112.110.107.17
ipAddress2 0.0.0.0
ipv6Address1 2402:8100:17:174c::32
ipv6Address2 ::
mmeSupportLegacyLte true
mmeSupportNbIoT false
pwsRestartHandling 1
end
gs-




crn ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=415
allowedMeasBandwidth 25
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 5
connectedModeMobilityPrio 5
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=415
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio 6
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=415 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=40940
allowedMeasBandwidth 25
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 7
connectedModeMobilityPrio 7
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio -1
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=40940 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=3601
allowedMeasBandwidth 50
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 3
connectedModeMobilityPrio 4
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio 5
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=3601 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=1421
allowedMeasBandwidth 50
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 4
connectedModeMobilityPrio 4
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio 7
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=1421 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=415
allowedMeasBandwidth 25
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 5
connectedModeMobilityPrio 5
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=415
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio 6
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=415 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=40940
allowedMeasBandwidth 25
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 7
connectedModeMobilityPrio 7
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio -1
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=40940 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=3601
allowedMeasBandwidth 50
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 3
connectedModeMobilityPrio 4
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio 5
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=3601 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=1421
allowedMeasBandwidth 50
anrMeasOn true
caTriggeredRedirectionActive true
cellReselectionPriority 4
connectedModeMobilityPrio 4
eutranFrequencyRef ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
presenceAntennaPort1 true
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 12
threshXHighQ 0
threshXLow 12
threshXLowQ 0
tReselectionEutra 2
voicePrio 7
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=1421 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT21,GeranFreqGroupRelation=1
anrMeasOn true
cellReselectionPriority 0
connectedModeMobilityPrio 0
csFallbackPrio 0
csFallbackPrioEC 0
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
mobilityAction 0
mobilityActionCsfb 0
pMaxGeran 23
qRxLevMin -115
threshXHigh 0
threshXLow 6
userLabel SIB7
voicePrio 0
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT21,GeranFreqGroupRelation=1 --------------------

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT22,GeranFreqGroupRelation=1
anrMeasOn true
cellReselectionPriority 0
connectedModeMobilityPrio 0
csFallbackPrio 0
csFallbackPrioEC 0
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
mobilityAction 0
mobilityActionCsfb 0
pMaxGeran 23
qRxLevMin -115
threshXHigh 0
threshXLow 6
userLabel SIB7
voicePrio 0
end
#END ENodeBFunction=1,EUtranCellTDD=$nodenameT22,GeranFreqGroupRelation=1 --------------------

gs-
confb-



ld ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ a5B2MobilityTimer 0
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ measQuantityUtraFDD 1
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ sMeasure 0
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ ueMeasurementsActive true
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ ueMeasurementsActiveGERAN true
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ ueMeasurementsActiveIF true
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1$ ueMeasurementsActiveUTRAN true

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrp -114
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrp -114
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5 480
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigA5=1$ triggerQuantityA5 0

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold1Rsrp -116
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold1Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold2EcNoUtra -160
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold2RscpUtra -109
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ hysteresisB2 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ timeToTriggerB2 640
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1$ triggerQuantityB2 0

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraBestCell=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraBestCell=1$ a3offset 30
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraBestCell=1$ hysteresisA3 10
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 40
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraBestCell=1$ triggerQuantityA3 0

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold1Rsrp -44
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold2Rsrp -106
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold2Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ hysteresisA5 10

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -114
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrq -165
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrp -118
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA1A2SearchRsrp 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA1A2SearchRsrq 15
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrq 10
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1Search 480
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Critical 480
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Search 480

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ a5B2MobilityTimer 0
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ measQuantityUtraFDD 1
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ sMeasure 0
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ ueMeasurementsActive true
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ ueMeasurementsActiveGERAN true
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ ueMeasurementsActiveIF true
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1$ ueMeasurementsActiveUTRAN true

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrp -114
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ a5Threshold1Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrp -114
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ a5Threshold2Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ hysteresisA5 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ timeToTriggerA5 480
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigA5=1$ triggerQuantityA5 0

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold1Rsrp -116
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold1Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold2EcNoUtra -160
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ b2Threshold2RscpUtra -109
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ hysteresisB2 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ timeToTriggerB2 640
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1$ triggerQuantityB2 0

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraBestCell=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraBestCell=1$ a3offset 30
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraBestCell=1$ hysteresisA3 10
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraBestCell=1$ timeToTriggerA3 40
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraBestCell=1$ triggerQuantityA3 0

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold1Rsrp -44
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold2Rsrp -106
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ a5Threshold2Rsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1$ hysteresisA5 10

ld ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1 #SystemCreated
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrp -114
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ a1a2SearchThresholdRsrq -165
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrp -118
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ a2CriticalThresholdRsrq -195
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA1A2SearchRsrp 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA1A2SearchRsrq 15
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrp 20
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ hysteresisA2CriticalRsrq 10
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA1Search 480
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Critical 480
lset ENodeBFunction=1,EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigSearch=1$ timeToTriggerA2Search 480

lt all
rbs
rbs
$date = `date +%y%m%d_%H%M`
cvms Pre_Baseline_$date

###################################################################################       Cell Lock   ----  Cells_Unlocked_Original

get 0 ^managedElementid$ > $nodename14
st cell
ma Cells_Unlocked_Original EUtranCell(FDD|TDD) administrativeState 1
ma Cells_Locked_Original EUtranCell(FDD|TDD) administrativeState 0
bl cell

##################################################################################        Featurestate   - 120 features 

get NodeBFunction=1 NodeBFunctionId > $NodeBFunctionId
#if $NodeBFunctionId = 1

set CXC4011183 featurestate 1
set CXC4011942 featurestate 1
set CXC4011443 featurestate 1
set CXC4010980 featurestate 1
set CXC4010990 featurestate 1
set CXC4011346 featurestate 1
set CXC4011247 featurestate 1
set CXC4011253 featurestate 1
set CXC4011914 featurestate 1
set CXC4010961 featurestate 1
set CXC4011064 featurestate 1
set CXC4011376 featurestate 1
set CXC4011059 featurestate 1
set CXC4010955 featurestate 0
set CXC4011664 featurestate 0
set CXC4011262 featurestate 0
set CXC4011370 featurestate 1
set CXC4011955 featurestate 0
set CXC4012271 featurestate 1
set CXC4011427 featurestate 1
set CXC4011667 featurestate 1
set CXC4011319 featurestate 1
set CXC4011476 featurestate 1
set CXC4011559 featurestate 1
set CXC4011666 featurestate 1
set CXC4011714 featurestate 1
set CXC4011922 featurestate 1
set CXC4012018 featurestate 1
set CXC4011980 featurestate 1
set CXC4011062 featurestate 1
set CXC4011074 featurestate 1
set CXC4011264 featurestate 0
set CXC4012240 featurestate 1
set CXC4011663 featurestate 0
set CXC4012259 featurestate 1
set CXC4011061 featurestate 1
set CXC4011918 featurestate 1
set CXC4011060 featurestate 1
set CXC4011345 featurestate 1
set CXC4011366 featurestate 1
set CXC4010959 featurestate 1
set CXC4011327 featurestate 1
set CXC4010723 featurestate 1
set CXC4011815 featurestate 1
set CXC4010618 featurestate 1
set CXC4011011 featurestate 1
set CXC4010616 featurestate 1
set CXC4010912 featurestate 1
set CXC4012563 featurestate 1
set CXC4012199 featurestate 1
set CXC4012505 featurestate 1
set CXC4012603 featurestate 1
set CXC4011814 featurestate 1
set CXC4012454 featurestate 1
set CXC4011969 featurestate 1
set CXC4012123 featurestate 1
set CXC4011983 featurestate 1
set CXC4012089 featurestate 1
set CXC4012485 featurestate 1
set CXC4010949 featurestate 1
set CXC4010319 featurestate 1
set CXC4010613 featurestate 1
set CXC4011255 featurestate 1
set CXC4011075 featurestate 1
set CXC4011163 featurestate 1
set CXC4011478 featurestate 1
set CXC4011055 featurestate 1
set CXC4011479 featurestate 1
set CXC4011477 featurestate 1
set CXC4011256 featurestate 1
set CXC4011246 featurestate 1
set CXC4011910 featurestate 1
set CXC4010967 featurestate 1
set CXC4011515 featurestate 1
set CXC4011713 featurestate 1
set CXC4011940 featurestate 1
set CXC4011444 featurestate 1
set CXC4011736 featurestate 0
set CXC4010974 featurestate 1
set CXC4010770 featurestate 1
set CXC4011482 featurestate 1
set CXC4010620 featurestate 1
set CXC4010956 featurestate 1
set CXC4011373 featurestate 1
set CXC4012070 featurestate 1
set CXC4010320 featurestate 1
set CXC4010609 featurestate 1
set CXC4010962 featurestate 1
set CXC4010963 featurestate 1
set CXC4010964 featurestate 1
set CXC4011050 featurestate 1
set CXC4011067 featurestate 1
set CXC4011068 featurestate 1
set CXC4011069 featurestate 1
set CXC4011072 featurestate 0
set CXC4011157 featurestate 1
set CXC4011372 featurestate 1
set CXC4011422 featurestate 1
set CXC4011481 featurestate 1
set CXC4011804 featurestate 1
set CXC4011913 featurestate 1
set CXC4011930 featurestate 1
set CXC4011937 featurestate 1
set CXC4011946 featurestate 1
set CXC4011981 featurestate 1
set CXC4012157 featurestate 1
set CXC4012297 featurestate 1
set CXC4012308 featurestate 0
set CXC4012316 featurestate 1
set CXC4012326 featurestate 1
set CXC4012344 featurestate 1
set CXC4012345 featurestate 1
set CXC4012346 featurestate 1
set CXC4012349 featurestate 1
set CXC4012352 featurestate 1
set CXC4012397 featurestate 1
set CXC4011372 FeatureState 1
set CXC4011481 FeatureState 1
set CXC4011973 featurestate 0
set CXC4011252 featurestate 1

# PTP
set CXC4040007 featurestate 1
set CXC4040008 featurestate 1
set CXC4040009 featurestate 1
set CXC4040019 featurestate 1

############################################################################     vswrSupervision


SET FieldReplaceableUnit=RRU-[123],RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-1[345],RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-[789],RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-1[012],RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-19,RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-20,RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-21,RfPort=[ABCD] vswrSupervisionActive true
SET FieldReplaceableUnit=RRU-[123],RfPort=[ABCD] vswrSupervisionSensitivity 100
SET FieldReplaceableUnit=RRU-1[345],RfPort=[ABCD] vswrSupervisionSensitivity 100
SET FieldReplaceableUnit=RRU-[789],RfPort=[ABCD] vswrSupervisionSensitivity 100
SET FieldReplaceableUnit=RRU-1[012],RfPort=[ABCD] vswrSupervisionSensitivity 100
SET FieldReplaceableUnit=RRU-19,RfPort=[ABCD] vswrSupervisionSensitivity 100
SET FieldReplaceableUnit=RRU-20,RfPort=[ABCD] vswrSupervisionSensitivity 100
SET FieldReplaceableUnit=RRU-21,RfPort=[ABCD] vswrSupervisionSensitivity 100

############################################################################    EutranFrequency


crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
arfcnValueEUtranDl 1421
caOffloadingEnabled false
excludeAdditionalFreqBandList 
extEndcAllowedPlmnListPolicy 
mfbiFreqBandIndPrio false
prioAdditionalFreqBandList 
userLabel    LTE-FDD-1800-B3
end

crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
arfcnValueEUtranDl 3601
caOffloadingEnabled false
excludeAdditionalFreqBandList 
extEndcAllowedPlmnListPolicy 
mfbiFreqBandIndPrio false
prioAdditionalFreqBandList 
userLabel    LTE-FDD-900-B0
end 

crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
arfcnValueEUtranDl 40940
caOffloadingEnabled false
excludeAdditionalFreqBandList 
extEndcAllowedPlmnListPolicy 
mfbiFreqBandIndPrio false
prioAdditionalFreqBandList 
userLabel    LTE-TDD-2500-B41
end

crn ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=39400
arfcnValueEUtranDl 39400
caOffloadingEnabled false
excludeAdditionalFreqBandList 
extEndcAllowedPlmnListPolicy 
mfbiFreqBandIndPrio false
prioAdditionalFreqBandList 
userLabel    LTE-TDD-2300-B40
end

########################################      EUtranFreqRelation -    40940 with All other

get 0 ^managedElementid$ > $nodename
get ENodeBFunction=1 eNBId > $nodeid

cr ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT23,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7

cr ENodeBFunction=1,EUtranCellTDD=$nodenameT24,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT25,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT26,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT27,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF21,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF22,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF23,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF11,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF12,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF13,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF31,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF32,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF33,EUtranFreqRelation=40940
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=40940
7



####################################      EUtranFreqRelation -    3601 with All other

cr ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT23,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4

cr ENodeBFunction=1,EUtranCellTDD=$nodenameT24,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT25,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT26,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT27,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF21,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF22,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF23,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF11,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF12,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF13,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF31,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF32,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF33,EUtranFreqRelation=3601
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=3601
4


########################################      EUtranFreqRelation -    1421 with All other

cr ENodeBFunction=1,EUtranCellTDD=$nodenameT21,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT22,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT23,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6

cr ENodeBFunction=1,EUtranCellTDD=$nodenameT24,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT25,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT26,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellTDD=$nodenameT27,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF21,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF22,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF23,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF11,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF12,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF13,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6

cr ENodeBFunction=1,EUtranCellFDD=$nodenameF31,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF32,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6
cr ENodeBFunction=1,EUtranCellFDD=$nodenameF33,EUtranFreqRelation=1421
ENodeBFunction=1,EUtraNetwork=1,EUtranFrequency=1421
6




################################################    GERAN Frequency Relation

cr ENodeBFunction=1,GeraNetwork=1
cr ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
1
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=597
597
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=598
598
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=599
599
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=643
643
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=644
644
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=645
645
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=646
646
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=647
647
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=648
648
0
cr ENodeBFunction=1,GeraNetwork=1,GeranFrequency=649
649
0

wait 1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=597 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=598 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=599 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=643 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=644 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=645 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=646 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=647 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=648 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
set ENodeBFunction=1,GeraNetwork=1,GeranFrequency=649 geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1


crn ENodeBFunction=1,EUtranCellFDD=$nodenameF11,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellFDD=$nodenameF12,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellFDD=$nodenameF13,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellFDD=$nodenameF21,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellFDD=$nodenameF22,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellFDD=$nodenameF23,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end

crn ENodeBFunction=1,EUtranCellTDD=$nodenameT21,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellTDD=$nodenameT22,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellTDD=$nodenameT23,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end
crn ENodeBFunction=1,EUtranCellTDD=$nodenameT24,GeranFreqGroupRelation=1
cellReselectionPriority 0
connectedModeMobilityPrio 0
geranFreqGroupRef GeraNetwork=1,GeranFreqGroup=1
end

#####################################################################################################   BASIC Setting

ENodeBFunction=1     srsPeriodicityTdd 20
set EUtranCellFDD=.* transmissionMode  4
set EUtranCellTDD=.* transmissionMode  4

set QciTable=default,QciProfilePredefined=qci1              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci2              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci3              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci4              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci5              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci6              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci65             dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci66             dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci69             dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci7              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci70             dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci8              dataFwdPerQciEnabled true
set QciTable=default,QciProfilePredefined=qci9              dataFwdPerQciEnabled true


cr ENodeBFunction=1,PmFlexCounterFilter=1
cr ENodeBFunction=1,PmFlexCounterFilter=2
cr ENodeBFunction=1,PmFlexCounterFilter=3
set PmFlexCounterFilter=1                                    qciFilterEnabled  true
set PmFlexCounterFilter=1                                    qciFilterMax      1
set PmFlexCounterFilter=1                                    qciFilterMin      1
set PmFlexCounterFilter=1                                    uePowerClassFilterEnabled false
set PmFlexCounterFilter=2                                    uePowerClassFilterEnabled true
wait 10
set PmFlexCounterFilter=3                                    uePowerClassFilterEnabled true
set PmFlexCounterFilter=1                                    uePowerClassFilterMax 1
set PmFlexCounterFilter=2                                    uePowerClassFilterMax 2
set PmFlexCounterFilter=3                                    uePowerClassFilterMax 3
set PmFlexCounterFilter=1                                    uePowerClassFilterMin 1
set PmFlexCounterFilter=2                                    uePowerClassFilterMin 2
set PmFlexCounterFilter=3                                    uePowerClassFilterMin 3
set PmFlexCounterFilter=3                                    uePowerClassFilterEnabled true


set EUtranCell.*DD=.* primaryPlmnReserved false

#################################################################################  ANR

set AnrFunction=1,AnrFunctionEUtran=1 anrInterFreqState 1
Set ENodeBFunction=1,AnrFunction=1,AnrFunctionEUtran=1      anrIntraFreqState 1
Set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          anrStateNR        1

################################################################################  lbceling

set LoadBalancingFunction=1 lbCeiling 300
set LoadBalancingFunction=1 lbThreshold 30
set QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 100
set QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 100
set QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 100
set QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 100
set AutoCellCapEstFunction=1 useEstimatedCellCap FALSE

wait 10 

lt all

wait 5
set QciTable=default,QciProfilePredefined=qci1 serviceType 1
set QciTable=default,QciProfilePredefined=qci2 serviceType 0
set QciTable=default,QciProfilePredefined=qci5 serviceType 2
set QciTable=default,QciProfilePredefined=qci1$ rlcMode 1
set QciTable=default,QciProfilePredefined=qci2$ rlcMode 1
set QciTable=default,QciProfilePredefined=qci5$ rlcMode 0
set QciTable=default,QciProfilePredefined=qci1              aqmMode           2
set QciTable=default,QciProfilePredefined=qci2              aqmMode           2
set QciTable=default,QciProfilePredefined=qci5              aqmMode           0
set QciTable=default,QciProfilePredefined=qci1$              counterActiveMode true
set QciTable=default,QciProfilePredefined=qci2$              counterActiveMode true
set QciTable=default,QciProfilePredefined=qci5$              counterActiveMode false
set QciTable=default,QciProfilePredefined=qci1              drxPriority 98
set QciTable=default,QciProfilePredefined=qci2              drxPriority 100
set QciTable=default,QciProfilePredefined=qci5              drxPriority 1
set QciTable=default,QciProfilePredefined=qci1 pdb 80
set QciTable=default,QciProfilePredefined=qci2 pdb 150
set QciTable=default,QciProfilePredefined=qci5 pdb 100
set QciTable=default,QciProfilePredefined=qci1              pdbOffset         50
set QciTable=default,QciProfilePredefined=qci2              pdbOffset         0
set QciTable=default,QciProfilePredefined=qci5              pdbOffset         0
set QciTable=default,QciProfilePredefined=qci1$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci2$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci5$ pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci1$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=qci2$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=qci5$ rlcSNLength 10
set QciTable=default,QciProfilePredefined=qci1$              rlfPriority 1
set QciTable=default,QciProfilePredefined=qci2$              rlfPriority 0
set QciTable=default,QciProfilePredefined=qci5$              rlfPriority 0
set EUtranCellFDD=.* dlFrequencyAllocationProportion 100
set EUtranCellFDD=.* ulFrequencyAllocationProportion 100
set EUtranCellFDD=.* dlConfigurableFrequencyStart 0
set EUtranCellFDD=.* ulConfigurableFrequencyStart 0
set EUtranCellFDD=.* dlInterferenceManagementActive true
set EUtranCellFDD=.* ulInterferenceManagementActive true
set EUtranCellFDD=.* ttiBundlingSwitchThres 100
set EUtranCellFDD=.* ttiBundlingSwitchThresHyst 20
set EUtranCell.* sCellActDeactDataThres 20
set EUtranCell.* dl256QamEnabled true
set EUtranCell.* pdcchCovImproveQci1 true
set EUtranCell.* ul64qamEnabled true
set EUtranCell.* pdcchCovImproveDtx true
set EUtranCell.* pdcchCovImprovesrb true
set EUtranCell.* Pdcchtargetblervolte 6
set QciTable=default,QciProfilePredefined=qci1              rlfProfileRef     RlfProfile=1 
set CarrierAggregationFunction=1                            sCellActDeactDataThresHyst 40
set CarrierAggregationFunction=1 sCellActProhibitTimer 10
set CarrierAggregationFunction=1 sCellDeactProhibitTimer 400
set CarrierAggregationFunction=1 sCellScheduleSinrThres -25
set CarrierAggregationFunction=1 caRateAdjustCoeff 3
set . pdcchTargetBlerPCell 18
set . pdcchTargetBler 18
set QciTable=default,QciProfilePredefined=qci1              tReorderingul  75
set QciTable=default,QciProfilePredefined=qci1              tReorderingdl  75

set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ tPollRetransmitDl 120
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1$ tPollRetransmitUl 120
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ tPollRetransmitUl 120
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1$ tPollRetransmitDl 120

wait 20

lt all

set AnrFunction=1                                           problematicCellPolicy 1
set AnrFunction=1                                           probCellDetectMedHoSuccTime 2
set AnrFunction=1                                           probCellDetectMedHoSuccThres 60
set AnrFunction=1                                           probCellDetectLowHoSuccTime 2
set AnrFunction=1                                           probCellDetectLowHoSuccThres 40
set AnrFunction=1                                           pciConflictMobilityEcgiMeas 1
set AnrFunction=1                                           pciConflictDetectionEcgiMeas 1
set AnrFunction=1                                           cellRelHoAttRateThreshold 15
set AnrFunction=1,AnrFunctionGeran=1$	 rimIntegrationEnabled  TRUE
set ENodeBFunction=1 tRelocOverall 20

################################----------------------- Paging ----------------------------------                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

set ENodeBFunction=1,Paging=1$ defaultPagingCycle 128
set ENodeBFunction=1,Paging=1$ nB 2
set ENodeBFunction=1,Paging=1$ pagingDiscardTimerDrx 3

###############################--------------------- RRC Timers----------------------------------                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

set ENodeBFunction=1,Rrc=1$ t300 1000
set ENodeBFunction=1,Rrc=1$ t301 400
set ENodeBFunction=1,Rrc=1$ t311 3000
set ENodeBFunction=1,Rrc=1$ t320 30
set ENodeBFunction=1,Rcs=1$ tInactivityTimer 10


set QciProfilePredefined=qci1$ rohcEnabled true
set QciTable=default,QciProfilePredefined=default           rohcEnabled       False
set QciProfilePredefined=qci2$ rohcEnabled False
set QciProfilePredefined=qci3$ rohcEnabled False
set QciProfilePredefined=qci4$ rohcEnabled False
set QciProfilePredefined=qci5$ rohcEnabled False
set QciProfilePredefined=qci6$ rohcEnabled False
set QciProfilePredefined=qci7$ rohcEnabled False
set QciProfilePredefined=qci8$ rohcEnabled False
set QciProfilePredefined=qci9$ rohcEnabled False
set QciProfilePredefined=qci65$ rohcEnabled False
set QciProfilePredefined=qci66$ rohcEnabled False
set QciProfilePredefined=qci69$ rohcEnabled False
set QciProfilePredefined=qci70$ rohcEnabled False
set QciTable=default,QciProfilePredefined=qci6$ rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci7$ rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci8$ rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci9$ rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci1              absPrioOverride   0
set QciTable=default,QciProfilePredefined=qci2$              absPrioOverride   0
set QciTable=default,QciProfilePredefined=qci5$              absPrioOverride   1
set QciTable=default,QciProfilePredefined=qci1$ dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci2$ dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci5$ dataFwdPerQciEnabled 1
set QciProfilePredefined=qci1 dlMinBitRate 0
set QciProfilePredefined=qci2 dlMinBitRate 384
set QciProfilePredefined=qci5 dlMinBitRate 0
set  QciProfilePredefined=qci1$ UlMinBitRate 0
set  QciProfilePredefined=qci5$ UlMinBitRate 0
set QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci2$ resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1$              dscp              46
set QciTable=default,QciProfilePredefined=qci2$              dscp              46
set QciTable=default,QciProfilePredefined=qci5$              dscp              48
set QciTable=default,QciProfilePredefined=qci3$              dscp              32
set QciTable=default,QciProfilePredefined=qci4$              dscp              24
set QciTable=default,QciProfilePredefined=qci6$              dscp              24
set QciTable=default,QciProfilePredefined=qci7$              dscp              20
set QciTable=default,QciProfilePredefined=qci8$              dscp              20
set QciTable=default,QciProfilePredefined=qci9$              dscp              20
set SctpProfile=1                                           dscp  48
set QciTable=default,QciProfilePredefined=qci1 priority 2
set QciTable=default,QciProfilePredefined=qci2 priority 4
set QciTable=default,QciProfilePredefined=qci5 priority 1
set  QciTable=default,QciProfilePredefined=qci1$ schedulingAlgorithm 6
set  QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 3
set  QciTable=default,QciProfilePredefined=qci5$ schedulingAlgorithm 0
set  QciTable=default,QciProfilePredefined=qci6$ schedulingAlgorithm 3
set  QciTable=default,QciProfilePredefined=qci7$ schedulingAlgorithm 3
set  QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 3
set  QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 3
set EUtranCellFDD=.*  ttiBundlingAfterReest 1
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 ulMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1  ulMaxRetxThreshold 32
set . tRrcConnectionReconfiguration 10

set QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
set QciTable=default,QciProfilePredefined=qci1$ ulMaxHARQTxQci 7
set QciTable=default,QciProfilePredefined=qci1$ dlMaxHARQTxQci 7
set . enableServiceSpecificHARQ true
set . tReorderingAutoConfiguration true
set MACConfiguration ulTtiBundlingMaxHARQTx 7
set ENodeBFunction=1,RlfProfile=1$ t311 3000
set ENodeBFunction=1,RlfProfile=1$ t310 2000
set ENodeBFunction=1,RlfProfile=1$ t301 1000

set . sCellHandlingAtVolteCall 1
set . srvccDelayTimer 3000
set . removeNenbTime 7
set ENodeBFunction=1,AnrFunction=1                          removeNrelTime 1
set CarrierAggregationFunction=1                            waitForAdditionalSCellOpportunity 2000
set CarrierAggregationFunction=1 waitForAdditionalScellOpportunity  2000
set CarrierAggregationFunction=1 sCellSelectionMode 2
set ReportConfigB2Utra=1 b2Threshold2EcNoUtra -150
set UeMeasControl=1 measQuantityUtraFDD 1
set . rlcDlDeliveryFailureAction 1
set EUtranCellFDD=.* pZeroNominalPucch -117
set EUtranCellFDD=.* pZeroNominalPusch -103
set . amoAllowed true
set GeranFreqGroupRelation=1$                   anrMeasOn                         TRUE
set ,EUtranFreqRelation=.*                                anrMeasOn                                     TRUE
set ,EUtranFreqRelation=.*                                caTriggeredRedirectionActive                  TRUE
set ,EUtranFreqRelation=.*                                lbActivationThreshold                         0
set ,EUtranFreqRelation=.*                                lbBnrPolicy                                   1
#########################---------------------- Configure VoLTE Settings ----------------------------------                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
Set . ueMeasurementsActive true
Set . ueMeasurementsActiveUTRAN true
Set . ueMeasurementsActiveIF true
Set . ueMeasurementsActiveGERAN true
Set . ueMeasurementsActiveCDMA2000 False
gs-
setm EUtranCell.DD=.* ulBlerTargetEnabled true dlBlerTargetEnabled true
gs+

###################################----------------------Configure RLC Mode-------------------------------------                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
Set QciTable=default,QciProfilePredefined=qci1 rlcMode 1
Set QciTable=default,QciProfilePredefined=qci2 rlcMode 1
Set QciTable=default,QciProfilePredefined=qci5 rlcMode 0

#########################---------------------Configure PDCP --------------------------------------------
Set QciTable=default,QciProfilePredefined=qci1 pdcpSNLength 12
Set QciTable=default,QciProfilePredefined=qci2 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci1 rlcSNLength 10
set QciTable=default,QciProfilePredefined=qci2 rlcSNLength 10
Set QciTable=default,QciProfilePredefined=qci5 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci5 rlcSNLength 10
set QciProfilePredefined=qci1 pdb 80
set QciProfilePredefined=qci5 pdb 100
set QciProfilePredefined=qci2 pdb 150

set QciTable=default,QciProfilePredefined=qci1              rlfPriority 1
set QciTable=default,QciProfilePredefined=qci2              rlfPriority 0
set QciTable=default,QciProfilePredefined=qci5              rlfPriority 0

#########################--------------------------Relative Priority-------------------------------------------
set  QciTable=default,QciProfilePredefined=qci6$ relativePriority  60
set  QciTable=default,QciProfilePredefined=qci7$ relativePriority  40
set  QciTable=default,QciProfilePredefined=qci8$ relativePriority  20
set  QciTable=default,QciProfilePredefined=qci9$ relativePriority  20

#########################--------------------------Enable ROHC-------------------------------------------
set QciProfilePredefined=qci1 rohcEnabled true

#########################-------------------------- Enable TTI bundling ---------------------------------
set . alignTtiBundWUlTrigSinr 1
set . ttiBundlingAfterHo 1
set . ttiBundlingAfterReest 2
set . ttiBundlingSwitchThres 55
Set . ttiBundlingSwitchThresHyst 25


#########################-------------------------- Configure SRVCC to GSM -------------------------------------

set . anrStateGsm 1
Set externalUtranCellFDD= srvccCapability 1
set ExternalGeranCell dtmSupport 1
set GeranFreqGroupRelation= mobilityAction 0
set ,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -114
set ,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set ,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -94
set ,GeranFreqGroupRelation= b2Thr2GeranFreqOffset 1

#########################-------------------------- Configure DRX ---------------------------------------


Set EUtranCellFDD= drxActive TRUE
set DrxProfile=1$ onDurationTimer 7
set DrxProfile=1$ drxInactivityTimer 6
set DrxProfile=1$ drxRetransmissionTimer 1
set DrxProfile=1$ longDrxCycle 3  
set DrxProfile=1$ longDrxCycleOnly 3
set DrxProfile=1$ shortDrxCycle 7
set DrxProfile=1$ shortDrxCycletimer 0
set DrxProfile=2$ onDurationTimer 4
set DrxProfile=2$ drxInactivityTimer 6
set DrxProfile=2$ drxRetransmissionTimer 2
set DrxProfile=2$ longDrxCycle 3
set DrxProfile=2$ longDrxCycleOnly 3



#########################---------------------- Abnormal Call Release Settings ----------------------------------
set QciProfilePredefined=qci6|QciProfilePredefined=qci8|QciProfilePredefined=qci9 dataFwdPerQciEnabled true
set . dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1              dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1 pdbOffset 50
set QciTable=default,QciProfilePredefined=qci1 pdb 80
set QciTable=default,QciProfilePredefined=qci1 servicetype 1
set . forcedSiTunnelingActive true
set . gtpuErrorIndicationDscp 48
set . s1HODirDataPathAvail false
set . rrcConnReestActive True
set . servOrPrioTriggeredErabAction 2
set QciTable=default,QciProfilePredefined=default pdb 300
set QciTable=default,QciProfilePredefined=qci2 pdb 150
set QciTable=default,QciProfilePredefined=qci1 serviceType 1
set QciTable=default,QciProfilePredefined=qci2 serviceType 0
set QciTable=default,QciProfilePredefined=qci5 serviceType 2


#########################---------------------- Default Parameter setting ----------------------------------


set QciTable=default,QciProfilePredefined=qci1 dlMinBitRate 0
set QciTable=default,QciProfilePredefined=qci2 dlMinBitRate 384
set QciTable=default,QciProfilePredefined=qci5 dlMinBitRate 0

set QciTable=default,QciProfilePredefined=qci1 inactivityTimerOffset 10
set QciTable=default,QciProfilePredefined=qci2 inactivityTimerOffset 10
set QciTable=default,QciProfilePredefined=qci5 inactivityTimerOffset 0


set QciTable=default,QciProfilePredefined=qci1 absPrioOverride 0
set QciTable=default,QciProfilePredefined=qci2 absPrioOverride 0
set QciTable=default,QciProfilePredefined=qci5 absPrioOverride 1
set QciTable=default,QciProfilePredefined=qci1 aqmMode 2
set QciTable=default,QciProfilePredefined=qci2 aqmMode 2
set QciTable=default,QciProfilePredefined=qci5 aqmMode 0
set QciTable=default,QciProfilePredefined=qci1 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci2 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci5 dataFwdPerQciEnabled 1
set QciTable=default,QciProfilePredefined=qci1 drxPriority 98
set QciTable=default,QciProfilePredefined=qci2 drxPriority 100
set QciTable=default,QciProfilePredefined=qci5 drxPriority 1




set QciTable=default,QciProfilePredefined=default logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciTable=default,QciProfilePredefined=qci1 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci2 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=2
set QciTable=default,QciProfilePredefined=qci3 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci4 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci5 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=1
set QciTable=default,QciProfilePredefined=qci6 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci7 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci8 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3
set QciTable=default,QciProfilePredefined=qci9 logicalChannelGroupRef QciTable=default,LogicalChannelGroup=3

set QciTable=default,QciProfilePredefined=qci5 pdbOffset 0
set QciTable=default,QciProfilePredefined=qci2 pdbOffset 0
set QciTable=default,QciProfilePredefined=qci1 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci5 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci2 pdcpSNLength 12
set QciTable=default,QciProfilePredefined=qci1 priority 2
set QciTable=default,QciProfilePredefined=qci2 priority 4
set QciTable=default,QciProfilePredefined=qci5 priority 1
set QciTable=default,QciProfilePredefined=qci1 rlcMode 1
set QciTable=default,QciProfilePredefined=qci5 rlcMode 0
set QciTable=default,QciProfilePredefined=qci2 rlcMode 1

set QciTable=default,QciProfilePredefined=qci1 resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci2 resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci5 resourceAllocationStrategy 0



set QciTable=default,QciProfilePredefined=qci1$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci2$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci3$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci4$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci5$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci6$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci65$ priorityFraction 7
set QciTable=default,QciProfilePredefined=qci66$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci69$ priorityFraction 5
set QciTable=default,QciProfilePredefined=qci7$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci70$ priorityFraction 5
set QciTable=default,QciProfilePredefined=qci8$ priorityFraction 0
set QciTable=default,QciProfilePredefined=qci9$ priorityFraction 0
set EthernetPort=TN egressQosMarking QosProfiles=1,DscpPcpMap=1
set AbisIp=1 dscpSectorControlUL 48
scw 4486:0
scw L4885:1

set  QciTable=default,QciProfilePredefined=qci1$ bitRateRecommendationEnabled  true
set  QciTable=default,QciProfilePredefined=qci2$ bitRateRecommendationEnabled  false
set  QciTable=default,QciProfilePredefined=qci5$ bitRateRecommendationEnabled  false
set  QciTable=default,QciProfilePredefined=qci6$ bitRateRecommendationEnabled  false
set  QciTable=default,QciProfilePredefined=qci7$ bitRateRecommendationEnabled  false
set  QciTable=default,QciProfilePredefined=qci8$ bitRateRecommendationEnabled  false
set  QciTable=default,QciProfilePredefined=qci9$ bitRateRecommendationEnabled  false


#########################---------------------- Additional Setting ----------------------------------
set ENodeBFunction=1 rrcConnReestActive true
set . inhibitA2SearchConfig 1
set QciTable=default,QciProfilePredefined=qci5$ tReorderingDl 35
set QciTable=default,QciProfilePredefined=qci5$ tReorderingUl 35

set QciTable=default,QciProfilePredefined=.* rohcEnabled 0
set QciTable=default,QciProfilePredefined=qci1$ rohcEnabled 1


#######################################################################################################################   LMS Common


set ,eutranFreqRelation=1421 voicePrio 6
set ,eutranFreqRelation=40940 voicePrio -1
set ,eutranFreqRelation=3601 voicePrio 7
set ,eutranFreqRelation=3601 cellReselectionPriority 5
set ,eutranFreqRelation=3601 connectedModeMobilityPrio 5
set ,eutranFreqRelation=1421 cellReselectionPriority 6
set ,eutranFreqRelation=1421 connectedModeMobilityPrio 6
set ,eutranFreqRelation=40940 cellReselectionPriority 7
set ,eutranFreqRelation=40940 connectedModeMobilityPrio 7
set ENodeBFunction=1,EUtranCell.*=.*,GeranFreqGroupRelation=1 cellReselectionPriority 0
set ENodeBFunction=1,EUtranCell.*=.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio 0
set ENodeBFunction=1,EUtranCellFDD=.*,GeranFreqGroupRelation=1 voicePrio 0
set ENodeBFunction=1,EUtranCellTDD=.*.,GeranFreqGroupRelation=1 voicePrio -1
lset Eutrancell.*=.*GeranFreqGroupRelation=1 csFallbackPrio 3
set EUtranCell.*=.* mobCtrlAtPoorCovActive TRUE
set EUtranCell.*=.*,EUtranFreqRelation=.* mobilityAction 1
set EUtranFreqRelation=.*. a5Thr1RsrpFreqOffset 0
set EUtranFreqRelation=.*.   a5Thr2RsrpFreqOffset 0 
set EUtranFreqRelation=.*.   anrMeasOn TRUE
set EUtranFreqRelation=.*.   qRxLevMin -124
set EUtranFreqRelation=.*.   threshXHigh 12
set EUtranFreqRelation=.*.   threshXLow 12
set EUtranFreqRelation=.*.   tReselectionEutra 3
set ENodeBFunction=1,EUtranCell qRxLevMin -124
set ENodeBFunction=1,EUtranCell systemInformationBlock3 sNonIntraSearch=10
set ENodeBFunction=1,EUtranCell threshServingLow 8
set ,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -115
set ,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA1Search 480
set ,UeMeasControl=1,ReportConfigSearch=1 timeToTriggerA2Search 480
set ,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 10
set ,UeMeasControl=1,ReportConfigA5=1 a5Threshold1Rsrp  -115
set ,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -115
set ,UeMeasControl=1,ReportConfigA5=1 hysteresisA5 10
set ,UeMeasControl=1,ReportConfigA5=1 timeToTriggerA5   480

lset EUtranCellFDD=.*F2(1|2|3),UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellFDD=.*F1(1|2|3),UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=72,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=72,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellFDD=.*F2(1|2|3),EUtranFreqRelation= eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellFDD=.*F1(1|2|3),EUtranFreqRelation=.* eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellTDD=.*,EUtranFreqRelation= eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=72,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCell.*=.*,GeranFreqGroupRelation=*.* qRxLevMin -105
set EUtranCell.*=.*,GeranFreqGroupRelation=*.* threshXLow 10
set EUtranCell.*=.*,GeranFreqGroupRelation=*.* threshXHigh 0
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -123
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 10
set EUtranCell.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThrQci1RsrpOffset 0
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp -116
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2 20
set EUtranCell.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -105
set EUtranCell.*=.*,GeranFreqGroupRelation= qciB2ThrOffsets b2Thr1RsrpGeranFreqQciOffset=4,b2Thr1RsrqGeranFreqQciOffset=0,b2Thr2GeranFreqQciOffset=8,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCellFDD=.*,GeranFreqGroupRelation=*.* voicePrio 0
set EUtranCellTDD=.*,GeranFreqGroupRelation=*.* voicePrio -1
set UeMeasControl=1  sMeasure -80
set EUtranFreqRelation=.* allowedMeasBandwidth 6
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 cellCapMaxCellSubCap 30000
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 cellCapMinCellSubCap 10000
set EUtranCellFDD=.*[FFF][222][123]$                                 cellCapMaxCellSubCap 7000
set EUtranCellFDD=.*[FFF][222][123]$                                   cellCapMinCellSubCap 500
set EUtranCellFDD=.*[FFF][111][123]$                               cellCapMaxCellSubCap 10000
set EUtranCellFDD=.*[FFF][111][123]$                                  cellCapMinCellSubCap 500

lset EUtranCellFDD=.*[FFF][222][123]$ cellSubscriptionCapacity 5000
lset EUtranCellFDD=.*[FFF][111][123]$ cellSubscriptionCapacity 5000
lset EUtranCellTDD=.*[TTTTTT][222][123567]$ cellSubscriptionCapacity 22000

gs-
setm EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellTDD=.*[T2][123346],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -110 a5Threshold2Rsrp -95
gs+
set EUtranCell.*=.*,GeranFreqGroupRelation=*.* b2Thr2GeranFreqOffset 0
set EUtranCell.*=.*,GeranFreqGroupRelation=*.* mobilityActionCsfb 0
set EUtranCell.*=.*,UeMeasControl=1,ReportConfigB2Geran=1 timeToTriggerB2   640
set EUtranCell.*=.*,UeMeasControl=1                  inhibitB2RsrqConfig   false





############################################################ ---Automatic Scell Management------------

set . sCellCandidate 2
set . asmSCellDlOnlyAllowed 1
set . asmHitRateAddThreshold 15
set . asmHitRateRemoveThreshold 5
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportDecr 1        
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportIncr 10        
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportMax 100        
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     asmInterFMeasReportMin 20        
set CarrierAggregationFunction=1,AutoSCellMgmFunction=1     sCellCandidateLimit 50        
set CarrierAggregationFunction=1$    caPreference   0  
set CarrierAggregationFunction=1$    caRateAdjustCoeff     3
set CarrierAggregationFunction=1$    caUsageLimit   65535  
set CarrierAggregationFunction=1$    effectiveBwImpactDl2Layer   180  
set CarrierAggregationFunction=1$    effectiveBwImpactDl4Layer   150  
set CarrierAggregationFunction=1$    fourLayerMimoPreferred      FALSE
set CarrierAggregationFunction=1$    sCellActDeactDataThres     20
set CarrierAggregationFunction=1$    sCellActDeactDataThresHyst  40     
set CarrierAggregationFunction=1$    sCellActProhibitTimer  10     
set CarrierAggregationFunction=1$    sCellDeactDelayTimer  50     
set CarrierAggregationFunction=1$    sCellDeactOutOfCoverageTimer   100     
set CarrierAggregationFunction=1$    sCellDeactProhibitTimer  400     
set CarrierAggregationFunction=1$    sCellEvaluationLevel  EFFECTIVE     
set CarrierAggregationFunction=1$    sCellPdcchOuterLoopMargin   100     
set CarrierAggregationFunction=1$    sCellScheduleSinrThres   -25  
set CarrierAggregationFunction=1$    sCellSelectionMode   2  
set CarrierAggregationFunction=1$    useAbsolutePrioForCspEffBw   FALSE     
set CarrierAggregationFunction=1$    waitForAdditionalSCellOpportunity   2000  
set CarrierAggregationFunction=1$    caPreemptionThreshold   70
set CarrierAggregationFunction=1$    enhancedSelectionOfMimoAndCa    true
set CarrierAggregationFunction=1$    sCellActDeactUlDataThresh    20
set CarrierAggregationFunction=1$    sCellActDeactUlDataThreshHyst    40
set CarrierAggregationFunction=1$    selectionPolicyUlWeighting    0
set CarrierAggregationFunction=1$    caPCellOnlyInitialSetup 1
set CarrierAggregationFunction=1$     waitForCaOpportunity 2000



################################################                LBDR

crn ENodeBFunction=1,LoadBalancingFunction=1,IdleModePrioAtRelease=1
end
set LoadBalancingFunction=1,IdleModePrioAtRelease=1 highLoadThreshold 800
set LoadBalancingFunction=1,IdleModePrioAtRelease=1 mediumLoadThreshold 600
set LoadBalancingFunction=1,IdleModePrioAtRelease=1 mediumHighLoadThreshold 600
set LoadBalancingFunction=1,IdleModePrioAtRelease=1 lowMediumLoadThreshold 600
set LoadBalancingFunction=1,IdleModePrioAtRelease=1 lowLoadThreshold 400
set LoadBalancingFunction=1 coverageAwareLbdar true
set LoadBalancingFunction=1 targetLoadAwareLbdar true

################################################             Timer Profile   

del ENodeBFunction=1,TimerProfile=0

crn ENodeBFunction=1,TimerProfile=0
tRelocOverall 20
tRrcConnReest 2
tRrcConnectionReconfiguration 9
tWaitForRrcConnReest 9
end
gs-
set ENodeBFunction=1,TimerProfile=0 tWaitForRrcConnReest 9
set ENodeBFunction=1,TimerProfile=0 tRrcConnectionReconfiguration 9
set ENodeBFunction=1,TimerProfile=0 tRrcConnReest 2
set ENodeBFunction=1,TimerProfile=0 tRelocOverall 20
set ENodeBFunction=1,Rrc=1 tWaitForRrcConnReest 10
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1,Rrc=1 tRrcConnReest 2
set EUtranCellFDD= ulHarqVolteBlerTarget 2
set EUtranCellTDD= ulHarqVolteBlerTarget 2

###########################################################################################################################    L900   

# ----------------------- Configure VoLTE Settings ----------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$  mobCtrlAtPoorCovActive TRUE
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActive true        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActiveUTRAN true        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActiveIF true        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActiveGERAN true        
# ----------------------------------Instant 256 Downlink-----------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$                                instantDl256QamMode 2        


set EUtranCellFDD=.*[FFF][111][123]$                                 prachSfn          -1        
#--------------------------------Uplink Triggered Volte------------------------------   
    
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold1Rsrp  -44        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold1Rsrq  -160        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 hysteresisA5      10        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 timeToTriggerA5   40        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 triggerQuantityA5 0         
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrp  -114        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrq  -160        
set EUtranCellFDD=.*[FFF][111][123]$                                ulVolteCovMobDetect 1        
set EUtranCellFDD=.*[FFF][111][123]$                                ulVolteCovMobThr  5        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  a5TimerUlVolteCovMob 2000        
#-------------------------------------Differential Uplink Power control---------------------------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$                                 enableSinrUplinkClpc true        
set EUtranCellFDD=.*[FFF][111][123]$                                 rxSinrTargetClpc  15        
set EUtranCellFDD=.*[FFF][111][123]$                                 interferenceThresholdSinrClpc -108        
set EUtranCellFDD=.*[FFF][111][123]$                                 ulPsdLoadThresholdSinrClpc 2        
set EUtranCellFDD=.*[FFF][111][123]$                                 ulTxPsdDistrThr   40        
set EUtranCellFDD=.*[FFF][111][123]$                                 p0ClpcExGoodEnabled true        
set EUtranCellFDD=.*[FFF][111][123]$                                 p0ClpcExBadEnabled true        
set EUtranCellFDD=.*[FFF][111][123]$                                 p0ClpcExBadSinrThr -10        
set EUtranCellFDD=.*[FFF][111][123]$                                 p0ClpcExGoodSinrThr 18        
set EUtranCellFDD=.*[FFF][111][123]$                                 p0ClpcExGoodSinrOffset64Qam 0        
set EUtranCellFDD=.*[FFF][111][123]$                                 p0ClpcExGoodSinrOffset256Qam 0        
#------------------------------------Optimized PUCCH---------------------------------------------------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$                                pdcchFlexibleBlerEnabled true        
set EUtranCellFDD=.*[FFF][111][123]$                                optimizedPdcchCongestThres 30        
set EUtranCellFDD=.*[FFF][111][123]$                                optimizedPdcchDlPrbThres 100        
set EUtranCellFDD=.*[FFF][111][123]$                                optimizedPdcchMaxTargetBler 200        
#------------------------------------------Optimized RRC-----------------------------------------------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$                                dlMaxRetxRrcReleaseThr 2        
set EUtranCellFDD=.*[FFF][111][123]$                                tPollRetxRrcReleaseDl 300        
        
#--------------------------------------------------Radio Bearer-----------------------------------------------------------------        
#--------------------------------------------------GPL-----------------------------------------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$    adaptiveCfiHoProhibit     0
set EUtranCellFDD=.*[FFF][111][123]$    alpha     10
set EUtranCellFDD=.*[FFF][111][123]$    cellCapMinMaxWriProt                      FALSE
set EUtranCellFDD=.*[FFF][111][123]$    cfraEnable                              TRUE
set EUtranCellFDD=.*[FFF][111][123]$    dl256QamEnabled                      TRUE
set EUtranCellFDD=.*[FFF][111][123]$    dlInterferenceManagementActive            TRUE  
set EUtranCellFDD=.*[FFF][111][123]$    drxActive                              TRUE
set EUtranCellFDD=.*[FFF][111][123]$    enableUeAssistedSigReduction              TRUE
set EUtranCellFDD=.*[FFF][111][123]$    lbdarCoverageThreshold     15
set EUtranCellFDD=.*[FFF][111][123]$    mobCtrlAtPoorCovActive              TRUE
set EUtranCellFDD=.*[FFF][111][123]$    pdcchCfiMode     5
set EUtranCellFDD=.*[FFF][111][123]$    enableServiceSpecificHARQ              TRUE
set EUtranCellFDD=.*[FFF][111][123]$    adaptiveCfiHoProhibit     0
set EUtranCellFDD=.*[FFF][111][123]$    pdcchTargetBlerVolte     6
set EUtranCellFDD=.*[FFF][111][123]$    pdschMaxNrOfPrbsPerUe     100
set EUtranCellFDD=.*[FFF][111][123]$    srvccDelayTimer     3000
set EUtranCellFDD=.*[FFF][111][123]$    sCellHandlingAtVolteCall                      1     
set EUtranCellFDD=.*[FFF][111][123]$    alpha     10
set EUtranCellFDD=.*[FFF][111][123]$    tReorderingAutoConfiguration              TRUE
set EUtranCellFDD=.*[FFF][111][123]$    ul64qamEnabled                 TRUE
set EUtranCellFDD=.*[FFF][111][123]$    ulImprovedUeSchedLastEnabled       TRUE  
set EUtranCellFDD=.*[FFF][111][123]$    ulInterferenceManagementActive      TRUE  
set EUtranCellFDD=.*[FFF][111][123]$    ulTrigActive             TRUE
set EUtranCellFDD=.*[FFF][111][123]$    cfraEnable                 TRUE
set EUtranCellFDD=.*[FFF][111][123]$    covTrigMobErabSetupConfig   DISABLED     
set EUtranCellFDD=.*[FFF][111][123]$    dl256QamEnabled    TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    dlInterferenceManagementActive     TRUE  
set EUtranCellFDD=.*[FFF][111][123]$    drxActive    TRUE  
set EUtranCellFDD=.*[FFF][111][123]$    enableServiceSpecificHARQ  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    enableUeAssistedSigReduction  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    lbdarCoverageThreshold  15     
set EUtranCellFDD=.*[FFF][111][123]$    mobCtrlAtPoorCovActive  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    pdcchCfiMode  5     
set EUtranCellFDD=.*[FFF][111][123]$    pdcchCovImproveDtx  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    pdcchCovImproveQci1  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    pdcchTargetBlerVolte  6     
set EUtranCellFDD=.*[FFF][111][123]$    pdschMaxNrOfPrbsPerUe  100     
set EUtranCellFDD=.*[FFF][111][123]$    qRxLevMin  -124     
set EUtranCellFDD=.*[FFF][111][123]$    sCellHandlingAtVolteCall   1  
set EUtranCellFDD=.*[FFF][111][123]$    srvccDelayTimer  3000     
set EUtranCellFDD=.*[FFF][111][123]$    transmissionMode  4     
set EUtranCellFDD=.*[FFF][111][123]$    tReorderingAutoConfiguration  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ttiBundlingAfterHo  1     
set EUtranCellFDD=.*[FFF][111][123]$    ttiBundlingAfterReest  1     
set EUtranCellFDD=.*[FFF][111][123]$    ul64qamEnabled  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ulImprovedUeSchedLastEnabled  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ulInterferenceManagementActive  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ulSchedCtrlForOocUesEnabled  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ulSchedCtrlForOocUesEnabled  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ulTrigActive  TRUE     
set EUtranCellFDD=.*[FFF][111][123]$    ulHarqVolteBlerTarget  2    


# ----------------------- Load balancing ----------------------------------        
set LoadBalancingFunction=1$                      lbCaCapHysteresis     20
set LoadBalancingFunction=1$                      lbCaThreshold     800
set LoadBalancingFunction=1$                      lbCeiling     300
set LoadBalancingFunction=1$                      lbDiffCaOffset     100
set LoadBalancingFunction=1$                      lbHitRateEUtranRemoveThreshold     2
set LoadBalancingFunction=1$                      lbThreshold     30
gs-
setm EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -110 a5Threshold2Rsrp -95
gs+
set AutoCellCapEstFunction=1$                      useEstimatedCellCap                      FALSE
set EUtranCellFDD=.*[FFF][111][123]$                               cellCapMaxCellSubCap 10000
set EUtranCellFDD=.*[FFF][111][123]$                                  cellCapMinCellSubCap 500
lset EUtranCellFDD=.*[FFF][222][123]$ cellSubscriptionCapacity 5000
lset EUtranCellFDD=.*[FFF][111][123]$ cellSubscriptionCapacity 5000
lset EUtranCellTDD=.*[TTTTTT][222222][123567]$  cellSubscriptionCapacity 22000
set EUtranCellFDD=.*[FFF][111][123]$ dlInterferenceManagementActive true
set EUtranCellFDD=.*[FFF][111][123]$  ulInterferenceManagementActive true
set EUtranCellFDD=.*[FFF][111][123]$  ttiBundlingSwitchThres 100
set EUtranCellFDD=.*[FFF][111][123]$  ttiBundlingSwitchThresHyst 20
set ENodeBFunction=1 tRelocOverall 20
set EUtranCellFDD=.*[FFF][111][123]$   ttiBundlingAfterReest 1
set EUtranCellFDD=.*[FFF][111][123]$  transmissionMode 4
gs-
setm EUtranCellFDD=.*[FFF][111][123]$ noOfPucchCqiUsers 160 noOfPucchSrUsers 160
gs+
set ENodeBFunction=1                                        prachConfigEnabled true        


#############################################################################################################################    L1800

#----------------------- Configure VoLTE Settings ----------------------------------        
set EUtranCellFDD=.*[FFF][111][123]$  mobCtrlAtPoorCovActive TRUE
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActive true        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActiveUTRAN true        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActiveIF true        
set EUtranCellFDD=.*[F1][123],UeMeasControl=1  ueMeasurementsActiveGERAN true        
#----------------------------------Instant 256 Downlink-----------------------------------        
set EUtranCellFDD=.*[FFF][222][123]$                                instantDl256QamMode 2        

set EUtranCellFDD=.*[FFF][222][123]$                                 prachSfn          -1        
#--------------------------------Uplink Triggered Volte------------------------------        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold1Rsrp  -44        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold1Rsrq  -160        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 hysteresisA5      10        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 timeToTriggerA5   40        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 triggerQuantityA5 0         
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrp  -114        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrq  -160        
set EUtranCellFDD=.*[F2][123]                                ulVolteCovMobDetect 1        
set EUtranCellFDD=.*[F2][123]                                ulVolteCovMobThr  5        
set EUtranCellFDD=.*[F2][123],UeMeasControl=1  a5TimerUlVolteCovMob 2000        
#-------------------------------------Differential Uplink Power control---------------------------------------------------        
set EUtranCellFDD=.*[FFF][222][123]$                                 enableSinrUplinkClpc true        
set EUtranCellFDD=.*[FFF][222][123]$                                 rxSinrTargetClpc  15        
set EUtranCellFDD=.*[FFF][222][123]$                                 interferenceThresholdSinrClpc -108        
set EUtranCellFDD=.*[FFF][222][123]$                                 ulPsdLoadThresholdSinrClpc 2        
set EUtranCellFDD=.*[FFF][222][123]$                                 ulTxPsdDistrThr   40        
set EUtranCellFDD=.*[FFF][222][123]$                                 p0ClpcExGoodEnabled true        
set EUtranCellFDD=.*[FFF][222][123]$                                 p0ClpcExBadEnabled true        
set EUtranCellFDD=.*[FFF][222][123]$                                 p0ClpcExBadSinrThr -10        
set EUtranCellFDD=.*[FFF][222][123]$                                 p0ClpcExGoodSinrThr 18        
set EUtranCellFDD=.*[FFF][222][123]$                                 p0ClpcExGoodSinrOffset64Qam 0        
set EUtranCellFDD=.*[FFF][222][123]$                                 p0ClpcExGoodSinrOffset256Qam 0        
#------------------------------------Optimized PUCCH---------------------------------------------------------------------------        
set EUtranCellFDD=.*[FFF][222][123]$                                pdcchFlexibleBlerEnabled true        
set EUtranCellFDD=.*[FFF][222][123]$                                optimizedPdcchCongestThres 30        
set EUtranCellFDD=.*[FFF][222][123]$                                optimizedPdcchDlPrbThres 100        
set EUtranCellFDD=.*[FFF][222][123]$                                optimizedPdcchMaxTargetBler 200        
#------------------------------------------Optimized RRC-----------------------------------------------------------------------        
set EUtranCellFDD=.*[FFF][222][123]$                                dlMaxRetxRrcReleaseThr 2        
set EUtranCellFDD=.*[FFF][222][123]$                                tPollRetxRrcReleaseDl 300        
        
#--------------------------------------------------Radio Bearer-----------------------------------------------------------------        
#--------------------------------------------------GPL-----------------------------------------------------------------        
set EUtranCellFDD=.*[FFF][222][123]$    adaptiveCfiHoProhibit     0
set EUtranCellFDD=.*[FFF][222][123]$    alpha     10
set EUtranCellFDD=.*[FFF][222][123]$    cellCapMinMaxWriProt                      FALSE
set EUtranCellFDD=.*[FFF][222][123]$    cfraEnable                              TRUE
set EUtranCellFDD=.*[FFF][222][123]$    dl256QamEnabled                      TRUE
set EUtranCellFDD=.*[FFF][222][123]$    dlInterferenceManagementActive           true
set EUtranCellFDD=.*[FFF][222][123]$    ulInterferenceManagementActive      true
set EUtranCellFDD=.*[FFF][222][123]$    drxActive                              TRUE
set EUtranCellFDD=.*[FFF][222][123]$    enableUeAssistedSigReduction              TRUE
set EUtranCellFDD=.*[FFF][222][123]$    lbdarCoverageThreshold     15
set EUtranCellFDD=.*[FFF][222][123]$    mobCtrlAtPoorCovActive              TRUE
set EUtranCellFDD=.*[FFF][222][123]$    pdcchCfiMode     5
set EUtranCellFDD=.*[FFF][222][123]$    enableServiceSpecificHARQ              TRUE
set EUtranCellFDD=.*[FFF][222][123]$    adaptiveCfiHoProhibit     0
set EUtranCellFDD=.*[FFF][222][123]$    pdcchTargetBlerVolte     6
set EUtranCellFDD=.*[FFF][222][123]$    pdschMaxNrOfPrbsPerUe     100
set EUtranCellFDD=.*[FFF][222][123]$    srvccDelayTimer     3000
set EUtranCellFDD=.*[FFF][222][123]$    sCellHandlingAtVolteCall                      1     
set EUtranCellFDD=.*[FFF][222][123]$    alpha     10
set EUtranCellFDD=.*[FFF][222][123]$    tReorderingAutoConfiguration              TRUE
set EUtranCellFDD=.*[FFF][222][123]$    ul64qamEnabled                 TRUE
set EUtranCellFDD=.*[FFF][222][123]$    ulImprovedUeSchedLastEnabled       TRUE  
set EUtranCellFDD=.*[FFF][222][123]$    ulTrigActive             TRUE
set EUtranCellFDD=.*[FFF][222][123]$    cfraEnable                 TRUE
set EUtranCellFDD=.*[FFF][222][123]$    covTrigMobErabSetupConfig   DISABLED     
set EUtranCellFDD=.*[FFF][222][123]$      dl256QamEnabled    TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    drxActive    TRUE  
set EUtranCellFDD=.*[FFF][222][123]$    enableServiceSpecificHARQ  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    enableUeAssistedSigReduction  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    lbdarCoverageThreshold  15     
set EUtranCellFDD=.*[FFF][222][123]$    mobCtrlAtPoorCovActive  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    pdcchCfiMode  5     
set EUtranCellFDD=.*[FFF][222][123]$    pdcchCovImproveDtx  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    pdcchCovImproveQci1  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    pdcchTargetBlerVolte  6     
set EUtranCellFDD=.*[FFF][222][123]$    pdschMaxNrOfPrbsPerUe  100     
set EUtranCellFDD=.*[FFF][222][123]$    qRxLevMin  -124     
set EUtranCellFDD=.*[FFF][222][123]$    sCellHandlingAtVolteCall   1  
set EUtranCellFDD=.*[FFF][222][123]$    srvccDelayTimer  3000     
set EUtranCellFDD=.*[FFF][222][123]$    transmissionMode  4     
set EUtranCellFDD=.*[FFF][222][123]$    tReorderingAutoConfiguration  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    ttiBundlingAfterHo  1     
set EUtranCellFDD=.*[FFF][222][123]$    ttiBundlingAfterReest  1     
set EUtranCellFDD=.*[FFF][222][123]$    ul64qamEnabled  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    ulImprovedUeSchedLastEnabled  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    ulSchedCtrlForOocUesEnabled  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    ulSchedCtrlForOocUesEnabled  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    ulTrigActive  TRUE     
set EUtranCellFDD=.*[FFF][222][123]$    ulHarqVolteBlerTarget  2

#----------------------- Load balancing ----------------------------------        
set LoadBalancingFunction=1$                      lbCaCapHysteresis     20
set LoadBalancingFunction=1$                      lbCaThreshold     800
set LoadBalancingFunction=1$                      lbCeiling     300
set LoadBalancingFunction=1$                      lbDiffCaOffset     100
set LoadBalancingFunction=1$                      lbHitRateEUtranRemoveThreshold     2
set LoadBalancingFunction=1$                      lbThreshold     30
gs-
setm EUtranCellFDD=.*[F1][123],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellFDD=.*[F2][123],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -110 a5Threshold2Rsrp -95
gs+
set AutoCellCapEstFunction=1$                      useEstimatedCellCap                      FALSE
set EUtranCellFDD=.*[FFF][222][123]$                                 cellCapMinCellSubCap 500
set EUtranCellFDD=.*[FFF][222][123]$                                 cellCapMaxCellSubCap 7000
lset EUtranCellFDD=.*[FFF][222][123]$ cellSubscriptionCapacity 5000
lset EUtranCellFDD=.*[FFF][111][123]$ cellSubscriptionCapacity 5000
lset EUtranCellTDD=.*[TTTTTT][222222][123567]$  cellSubscriptionCapacity 22000
set EUtranCellFDD=.*[FFF][222][123]$  ttiBundlingSwitchThres 100
set EUtranCellFDD=.*[FFF][222][123]$  ttiBundlingSwitchThresHyst 20
set ENodeBFunction=1 tRelocOverall 20
set EUtranCellFDD=.*[FFF][222][123]$   ttiBundlingAfterReest 1
set EUtranCellFDD=.*[FFF][222][123]$  transmissionMode 4
gs-
setm EUtranCellFDD=.*[FFF][222][123]$ noOfPucchCqiUsers 320 noOfPucchSrUsers 320
gs+
set ENodeBFunction=1                                        prachConfigEnabled true        


##########################################################################################################       L2500

#########################---------------------- Configure VoLTE Settings ----------------------------------        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  mobCtrlAtPoorCovActive TRUE
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1  ueMeasurementsActive true        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1  ueMeasurementsActiveUTRAN true        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1  ueMeasurementsActiveIF true        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1  ueMeasurementsActiveGERAN true        
----------------------------------Instant 256 Downlink-----------------------------------        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                instantDl256QamMode 2        

set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 prachSfn          -1        
#########################-------------------------------Uplink Triggered Volte------------------------------ 
   
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold1Rsrp  -44 
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold1Rsrq  -160        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 hysteresisA5      10        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 timeToTriggerA5   40        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 triggerQuantityA5 0         
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrp  -114        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrq  -160        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                               ulVolteCovMobDetect 1        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                ulVolteCovMobThr  5        
set EUtranCellTDD=.*[T2][123567],UeMeasControl=1  a5TimerUlVolteCovMob 2000        
#########################------------------------------------Differential Uplink Power control---------------------------------------------------        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 enableSinrUplinkClpc true        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 rxSinrTargetClpc  15        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 interferenceThresholdSinrClpc -108        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 ulPsdLoadThresholdSinrClpc 2        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 ulTxPsdDistrThr   40        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 p0ClpcExGoodEnabled true        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 p0ClpcExBadEnabled true        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 p0ClpcExBadSinrThr -10        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 p0ClpcExGoodSinrThr 18        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 p0ClpcExGoodSinrOffset64Qam 0        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 p0ClpcExGoodSinrOffset256Qam 0        
#########################-----------------------------------Optimized PUCCH---------------------------------------------------------------------------        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                pdcchFlexibleBlerEnabled true        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                optimizedPdcchCongestThres 30        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                optimizedPdcchDlPrbThres 100        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                optimizedPdcchMaxTargetBler 200        
#########################-----------------------------------------Optimized RRC-----------------------------------------------------------------------        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                dlMaxRetxRrcReleaseThr 2        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                tPollRetxRrcReleaseDl 300        
        
#########################-------------------------------------------------Radio Bearer-----------------------------------------------------------------        
#########################-------------------------------------------------GPL-----------------------------------------------------------------        
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    adaptiveCfiHoProhibit     0
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    alpha     10
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    cellCapMinMaxWriProt                      FALSE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    cfraEnable                              TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    dl256QamEnabled                      TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    dlInterferenceManagementActive            TRUE  
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    drxActive                              TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    enableUeAssistedSigReduction              TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    lbdarCoverageThreshold     15
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    mobCtrlAtPoorCovActive              TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdcchCfiMode     5
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    enableServiceSpecificHARQ              TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    adaptiveCfiHoProhibit     0
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdcchTargetBlerVolte     6
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdschMaxNrOfPrbsPerUe     100
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    srvccDelayTimer     3000
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    sCellHandlingAtVolteCall                      1     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    alpha     10
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    tReorderingAutoConfiguration              TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ul64qamEnabled                 TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulImprovedUeSchedLastEnabled       TRUE  
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulInterferenceManagementActive      TRUE  
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulTrigActive             TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    cfraEnable                 TRUE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    covTrigMobErabSetupConfig   DISABLED     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$      dl256QamEnabled    TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    dlInterferenceManagementActive     TRUE  
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    drxActive    TRUE  
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    enableServiceSpecificHARQ  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    enableUeAssistedSigReduction  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    lbdarCoverageThreshold  15     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    mobCtrlAtPoorCovActive  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdcchCfiMode  5     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdcchCovImproveDtx  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdcchCovImproveQci1  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdcchTargetBlerVolte  6     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    pdschMaxNrOfPrbsPerUe  100     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    qRxLevMin  -124     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    sCellHandlingAtVolteCall   1  
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    srvccDelayTimer  3000     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    transmissionMode  4     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    tReorderingAutoConfiguration  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ul64qamEnabled  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulImprovedUeSchedLastEnabled  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulInterferenceManagementActive  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulSchedCtrlForOocUesEnabled  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulSchedCtrlForOocUesEnabled  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulTrigActive  TRUE     
set EUtranCellTDD=.*[TTTTTT][222222][123567]$    ulHarqVolteBlerTarget  2     


#########################---------------------- Load balancing ----------------------------------        
set LoadBalancingFunction=1$                      lbCaCapHysteresis     20
set LoadBalancingFunction=1$                      lbCaThreshold     800
set LoadBalancingFunction=1$                      lbCeiling     300
set LoadBalancingFunction=1$                      lbDiffCaOffset     100
set LoadBalancingFunction=1$                      lbHitRateEUtranRemoveThreshold     2
set LoadBalancingFunction=1$                      lbThreshold     30
gs-
setm EUtranCellFDD=.*[F1][123567],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellFDD=.*[F2][123567],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -44 a5Threshold2Rsrp -112
setm EUtranCellTDD=.*[T2][123567],UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold1Rsrp  -110 a5Threshold2Rsrp -95
gs+
set AutoCellCapEstFunction=1$                      useEstimatedCellCap                      FALSE
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 cellCapMaxCellSubCap 30000
set EUtranCellTDD=.*[TTTTTT][222222][123567]$                                 cellCapMinCellSubCap 10000
lset EUtranCellFDD=.*[FFF][222][123]$ cellSubscriptionCapacity 5000
lset EUtranCellFDD=.*[FFF][111][123]$ cellSubscriptionCapacity 5000
lset EUtranCellTDD=.*[TTT][222][123567]$ cellSubscriptionCapacity 22000
set EUtranCellTDD=.*[TTT][222][123567]$ dlInterferenceManagementActive true
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  ulInterferenceManagementActive true
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  ttiBundlingSwitchThres 100
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  ttiBundlingSwitchThresHyst 20
set ENodeBFunction=1 tRelocOverall 20
set EUtranCellTDD=.*[TTTTTT][222222][123567]$   ttiBundlingAfterReest 1
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  transmissionMode 4
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  crsgain 300
set EUtranCellTDD=.*[TTTTTT][222222][123567]$  pdschTypeBGain 1
gs-
setm EUtranCellTDD=.*[TTT][222][123]$ noOfPucchCqiUsers 320 noOfPucchSrUsers 320
gs+
set ENodeBFunction=1                                        prachConfigEnabled true        


######################################################################################################   GASC for 1800

st trx
if $nr_of_mos >=0
set CXC4011365 featureState 0
set CXC4011984 featureState 1
fi

set EUtranCellFDD=.*(F21|F22|F23) pucchOverdimensioning 10
set EUtranCellFDD=.*(F21|F22|F23) dlConfigurableFrequencyStart 13
set EUtranCellFDD=.*(F21|F22|F23) ulConfigurableFrequencyStart 13
set EUtranCellFDD=.*(F21|F22|F23) dlFrequencyAllocationProportion 72
set EUtranCellFDD=.*(F21|F22|F23) ulFrequencyAllocationProportion 72
set EUtranCellFDD=.*(F21|F22|F23) dlInterferenceManagementActive false
set EUtranCellFDD=..*(F21|F22|F23) ulInterferenceManagementActive false


######################################################################################################      Time & Phase -  ( All Delhi sites are Non PTP )

lt all
st tdd
if $nr_of_mos ~ ^0 
    set ENodeBFunction=1      timeAndPhaseSynchAlignment true 
    set ENodeBFunction=1       timeAndPhaseSynchCritical false
else if $nr_of_mos > 1
    set ENodeBFunction=1      timeAndPhaseSynchAlignment true 
    set ENodeBFunction=1       timeAndPhaseSynchCritical true
fi 



#####################################################################################################   Cells Unlock
# Below 7 lines Added on 3rd Jan 2025
set QciTable=default,QciProfilePredefined=qci1$ inactivityTimerOffset 10
set QciTable=default,QciProfilePredefined=qci2$ inactivityTimerOffset 10
set ENodeBFunction=1,DrxProfile=1$ drxInactivityTimer 6
Set EUtranCellTDD= drxActive TRUE
set EUtranCell.*=.*,UeMeasControl=1   measQuantityUtraFDD 1
set CXC4011183 featurestate 1
set CXC4011317 featurestate 1
######################
lset EUtranCellFDD=.*F2(1|2|3),UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellFDD=.*F1(1|2|3),UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellFDD=.*F2(1|2|3),EUtranFreqRelation= eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellFDD=.*F1(1|2|3),EUtranFreqRelation=.* eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellTDD=.*,EUtranFreqRelation= eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellFDD=.*F2(1|2|3),GeranFreqGroupRelation= qciB2ThrOffsets b2Thr1RsrpGeranFreqQciOffset=0,b2Thr1RsrqGeranFreqQciOffset=0,b2Thr2GeranFreqQciOffset=8,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellFDD=.*F.*,GeranFreqGroupRelation= qciB2ThrOffsets b2Thr1RsrpGeranFreqQciOffset=4,b2Thr1RsrqGeranFreqQciOffset=0,b2Thr2GeranFreqQciOffset=8,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
Set EUtranCell.*=.*,GeranFreqGroupRelation=.* b2Thr1RsrpGeranFreqOffset 0
set ,eutranFreqRelation=1421 voicePrio 7
set ,eutranFreqRelation=3601 voicePrio 6
set ,eutranFreqRelation=40940 voicePrio 1
set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set RlfProfile=0$ t301 1000
set RlfProfile=1$ t301 1000
set RlfProfile=1$ t311 10000
set RlfProfile=0$ t311 10000
set ENodeBFunction=1,Rrc=1 t301 1000
set ENodeBFunction=1,Rrc=1 t311 10000



set CUUP5qiTable=1,CUUP5qi=5qi69   dscp  40
set CUUP5qiTable=1,CUUP5qi=5qi79   dscp  38
set CUUP5qiTable=1,CUUP5qi=5qi80   dscp  38
set CUUP5qiTable=1,CUUP5qi=5qi82   dscp  44
 
set  DU5qiTable=1,DU5qi=69    dscp  40
set  DU5qiTable=1,DU5qi=79    dscp  38
set  DU5qiTable=1,DU5qi=80    dscp  38
set  DU5qiTable=1,DU5qi=82    dscp  44
 
set  QciTable=default,QciProfilePredefined=qci2    dscp  44
set  QciTable=default,QciProfilePredefined=qci3    dscp  42
set  QciTable=default,QciProfilePredefined=qci4    dscp  39
set  QciTable=default,QciProfilePredefined=qci6    dscp  38
set  QciTable=default,QciProfilePredefined=qci65    dscp  44
set  QciTable=default,QciProfilePredefined=qci66    dscp  44
set  QciTable=default,QciProfilePredefined=qci69    dscp  40
set  QciTable=default,QciProfilePredefined=qci7    dscp  36
set  QciTable=default,QciProfilePredefined=qci70    dscp  36
set  QciTable=default,QciProfilePredefined=qci8    dscp  34
set  QciTable=default,QciProfilePredefined=qci9    dscp  34
rdel Transport=1,Synchronization=1,RadioEquipmentClock=1,RadioEquipmentClockReference=2
rdel Transport=1,Ptp=1,BoundaryOrdinaryClock=PTP1,PtpBcOcPort=1
set ManagedElement=$nodename                           userLabel         ZZ_$nodename
set    ENodeBFunction=1  timeAndPhaseSynchAlignment  true                       
set ENodeBFunction=1   timeAndPhaseSynchCritical      true   

set EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Cdma2000=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2NR=1 b2Threshold1Rsrp  -120
set EUtranCellTDD=$nodenameT21,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Cdma2000=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2NR=1 b2Threshold1Rsrp  -120
set EUtranCellTDD=$nodenameT22,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -116


set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -115
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 10
set EUtranCellFDD=$nodenameT.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA1A2SearchRsrp 10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigSearch=1 a1a2SearchThresholdRsrp -115


set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -115
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 a5Threshold2RsrpAnrDelta 1
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold2Rsrp  -112
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5InterFreqHigherPrio=1 a5Threshold2Rsrp  -140
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5SoftLock=1 a5Threshold2Rsrp  -140
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5Spifho=1 a5Threshold2Rsrp  -110
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5UlTraffic=1 a5Threshold2Rsrp  -140
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrp  -140
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrp  -114
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp  -112

set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5RsrqOffset 0
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5InterFreqHigherPrio=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5Spifho=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5UlTraffic=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5UlTrig=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5UlVolte=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigCsg=1 hysteresisA5AltCsg 10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5      10
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigEUtraInterFreqMbms=1 hysteresisA5      10

set QciTable=default,QciProfilePredefined=qci1              dlResourceAllocationStrategy 1


set QciTable=default,QciProfilePredefined=qci1              inactivityTimerOffset 10
set QciTable=default,QciProfilePredefined=qci2              inactivityTimerOffset 10
set QciTable=default,QciProfilePredefined=qci2              schedulingAlgorithm 3

set QciTable=default,QciProfilePredefined=default           rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci1              rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci2              rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci3              rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci4              rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci5              rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci6              rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci65             rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci66             rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci69             rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci7              rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci70             rohcForUlDataEnabled false
set QciTable=default,QciProfilePredefined=qci8              rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci9              rohcForUlDataEnabled true
set QciTable=default,QciProfilePredefined=qci1    counterActiveMode  true
set QciTable=default,QciProfilePredefined=qci2    counterActiveMode true
set EUtranCellTDD=$nodenameT.*  crsgain 300
set ManagedElement=$nodename                           userLabel         $nodename
set EthernetPort=TN_IDL_B                                   egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort=TN_E          egressQosMarking  QosProfiles=1,DscpPcpMap=1
set EthernetPort=TN_ IDL_B       egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=GSM_ABIS,InterfaceIPv4=GSM_ABIS                  egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTE_CP,InterfaceIPv4=LTE_X2                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTE_CP,InterfaceIPv6=LTE_CP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTE_OM,InterfaceIPv6=LTE_OM                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set Router=LTE_UP,InterfaceIPv6=LTE_UP                      egressQosMarking  QosProfiles=1,DscpPcpMap=1
set QciTable=default,QciProfilePredefined=default           dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=default           resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1              dlResourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci1              resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci2              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci2              resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci3              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci3              resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci4              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci4              resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci5              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci5              resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci6              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci6              resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci65             dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci65             resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci66             dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci66             resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci69             dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci69             resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci7              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci7              resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci70             dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci70             resourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci8              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci8              resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci9              dlResourceAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci9              resourceAllocationStrategy 1
set QciTable=default,QciProfilePredefined=default           srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1              srsAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci2              srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci3              srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci4              srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci5              srsAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci6              srsAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci65             srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci66             srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci69             srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci7              srsAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci70             srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci8              srsAllocationStrategy 1
set QciTable=default,QciProfilePredefined=qci9              srsAllocationStrategy 1
set QciTable=default,SciProfile=default                     srsAllocationStrategy 0
set QciTable=default,SciProfile=sci1                        srsAllocationStrategy 0
set QciTable=default,QciProfilePredefined=qci1              counterActiveMode true
set QciTable=default,QciProfilePredefined=qci2              counterActiveMode true
del ENodeBFunction=1,TimerProfile=0

confb+
gs+

crn ENodeBFunction=1,TimerProfile=0
tRelocOverall 20
tRrcConnReest 2
tRrcConnectionReconfiguration 9
tWaitForRrcConnReest 9
end
gs-

set ENodeBFunction=1,TimerProfile=0 tWaitForRrcConnReest 9
set ENodeBFunction=1,TimerProfile=0 tRrcConnectionReconfiguration 9
set ENodeBFunction=1,TimerProfile=0 tRrcConnReest 2
set ENodeBFunction=1,TimerProfile=0 tRelocOverall 20
set ENodeBFunction=1,Rrc=1 tWaitForRrcConnReest 10
set ENodeBFunction=1 tRelocOverall 20
set ENodeBFunction=1,Rrc=1 tRrcConnReest 2
set EUtranCellFDD= ulHarqVolteBlerTarget 2
set EUtranCellTDD= ulHarqVolteBlerTarget 2
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=1421 endcHoFreqPriority 5
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=3601 endcHoFreqPriority 4
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=40940 endcHoFreqPriority 3
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=415  endcHoFreqPriority 7
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 endcHoFreqPriority 5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 endcHoFreqPriority 4
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 endcHoFreqPriority 3
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=415  endcHoFreqPriority 7

set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma2000=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 b2Threshold1Rsrp  -120
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma2000=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 b2Threshold1Rsrp  -120
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -116
set ENodeBFunction=1                                        prachConfigEnabled true
set EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,Qci                                       ProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2


set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp  -115
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 a5Threshold2RsrpAnrDelta 1
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5EndcHo=1 a5Threshold2Rsrp  -112
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5InterFreqHigherPrio=1 a5Threshold2Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5SoftLock=1 a5Threshold2Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5Spifho=1 a5Threshold2Rsrp  -110
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5UlTraffic=1 a5Threshold2Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5UlTrig=1 a5Threshold2Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5UlVolte=1 a5Threshold2Rsrp  -114
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 a5Threshold2Rsrp  -95

set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5=1 hysteresisA5RsrqOffset 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5=1,ReportConfigA5Anr=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5InterFreqHigherPrio=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5Spifho=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5UlTraffic=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5UlTrig=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5UlVolte=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigCsg=1 hysteresisA5AltCsg 10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigEUtraInterFreqLb=1 hysteresisA5      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigEUtraInterFreqMbms=1 hysteresisA5      10


set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma2000=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 b2Threshold1Rsrp  -140
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold1Rsrp  -116
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 b2Threshold1Rsrp  -120
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Utra=1 b2Threshold1Rsrp  -116

set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma2000=1 hysteresisB2      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma2000=1 hysteresisB2RsrqOffset 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 hysteresisB2      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 hysteresisB2RsrqOffset 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2      20
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Geran=1 hysteresisB2RsrqOffset 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 hysteresisB2      10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 hysteresisB2      2
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 hysteresisB2RsrqOffset 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2      20
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Utra=1 hysteresisB2RsrqOffset 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2UtraUlTrig=1 hysteresisB2      10


set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma2000=1 triggerQuantityB2 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Cdma20001xRtt=1 triggerQuantityB2 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Geran=1 triggerQuantityB2 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 triggerQuantityB2 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2NR=1 triggerQuantityB2NR 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB2Utra=1 triggerQuantityB2 0
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1         measQuantityUtraFDD 1
set EUtranCellTDD=$nodenameT.*,GeranFreqGroupRelation=1 b2Thr1RsrpGeranFreqOffset 0
lset EUtranCellTDD=.*,EUtranFreqRelation= eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCellTDD=$nodename.*,UeMeasControl=1,ReportConfigB2Geran=1 b2Threshold2Geran -105
set EUtranCellTDD=$nodename.*,UeMeasControl=1,ReportConfigB2GeranUlTrig=1 b2Threshold2Geran -110
set EUtranCell.*=.*,GeranFreqGroupRelation= qciB2ThrOffsets b2Thr1RsrpGeranFreqQciOffset=4,b2Thr1RsrqGeranFreqQciOffset=0,b2Thr2GeranFreqQciOffset=8,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellFDD=.*F1(1|2|3|4|5),GeranFreqGroupRelation= qciB2ThrOffsets b2Thr1RsrpGeranFreqQciOffset=-4,b2Thr1RsrqGeranFreqQciOffset=0,b2Thr2GeranFreqQciOffset=8,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
set EUtranCellTDD=$nodenameT.*                         qRxLevMin         -124
set EUtranCellTDD=$nodenameT.*                         qRxLevMinCe       -140
set EUtranCellTDD=$nodenameT.*                         qRxLevMinOffset   1000
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 qRxLevMin         -124
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 qRxLevMinCe       -140
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 qRxLevMin         -124
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 qRxLevMinCe       -140
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 qRxLevMin         -124
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 qRxLevMinCe       -140
set EUtranCellTDD=$nodenameT.*                         threshServingLow  8
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 threshXLow        12
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 threshXLowQ       0
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 threshXLow        12
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 threshXLowQ       0
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 threshXLow        12
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 threshXLowQ       0
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=415  threshXLow        12
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=415  threshXLowQ       0
set EUtranCellTDD=$nodenameT.*,GeranFreqGroupRelation=1 threshXLow        10
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigSearch=1 a2CriticalThresholdRsrp -123
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigSearch=1 hysteresisA2CriticalRsrp 10

set RlfProfile=0                                            t311              10000
set RlfProfile=1                                            t311              10000
set RlfProfile=10                                           t311              3000
set RlfProfile=11                                           t311              3000
set RlfProfile=12                                           t311              3000
set RlfProfile=13                                           t311              3000
set RlfProfile=14                                           t311              3000
set RlfProfile=15                                           t311              3000
set RlfProfile=16                                           t311              3000
set RlfProfile=17                                           t311              3000
set RlfProfile=18                                           t311              3000
set RlfProfile=19                                           t311              3000
set RlfProfile=2                                            t311              3000
set RlfProfile=20                                           t311              3000
set RlfProfile=21                                           t311              3000
set RlfProfile=22                                           t311              3000
set RlfProfile=3                                            t311              3000
set RlfProfile=4                                            t311              3000
set RlfProfile=5                                            t311              3000
set RlfProfile=6                                            t311              3000
set RlfProfile=7                                            t311              3000
set RlfProfile=8                                            t311              3000
set RlfProfile=9                                            t311              3000
set ENodeBFunction=1,Rrc=1                                  t311              10000
set ENodeBFunction=1,Rrc=1                                  t311Nb            5000
set RlfProfile=0                                            t301              1000
set RlfProfile=1                                            t301              1000
set RlfProfile=10                                           t301              1000
set RlfProfile=11                                           t301              1000
set RlfProfile=12                                           t301              1000
set RlfProfile=13                                           t301              1000
set RlfProfile=14                                           t301              1000
set RlfProfile=15                                           t301              1000
set RlfProfile=15                                           t301              1000
set RlfProfile=16                                           t301              1000
set RlfProfile=17                                           t301              1000
set RlfProfile=18                                           t301              1000
set RlfProfile=19                                           t301              1000
set RlfProfile=2                                            t301              1000
set RlfProfile=20                                           t301              1000
set RlfProfile=21                                           t301              1000
set RlfProfile=22                                           t301              1000
set RlfProfile=3                                            t301              1000
set RlfProfile=4                                            t301              1000
set RlfProfile=5                                            t301              1000
set RlfProfile=6                                            t301              1000
set RlfProfile=7                                            t301              1000
set RlfProfile=8                                            t301              1000
set RlfProfile=9                                            t301              1000
set ENodeBFunction=1,Rrc=1                                  t301              400
set ENodeBFunction=1,Rrc=1                                  t301Br            0
set ENodeBFunction=1,Rrc=1                                  t301Nb            10000

######################################################################################################      Time & Phase -  ( All Delhi sites are Non PTP )


lt all
st tdd
if $nr_of_mos ~ ^0
    set ENodeBFunction=1      timeAndPhaseSynchAlignment true
    set ENodeBFunction=1       timeAndPhaseSynchCritical false
else if $nr_of_mos > 1
    set ENodeBFunction=1      timeAndPhaseSynchAlignment true
    set ENodeBFunction=1       timeAndPhaseSynchCritical true
fi

set ENodeBFunction=1                                        x2GtpuEchoDscp  48
set ENodeBFunction=1                                        interEnbCaTunnelDscp 34
set ENodeBFunction=1                                        s1GtpuEchoDscp   48
set ENodeBFunction=1                                        interEnbUlCompTunnelDscp 34



lt all

set  QciTable=default,QciProfilePredefined=qci1              dscp 46
set  QciTable=default,QciProfilePredefined=qci2              dscp 44
set  QciTable=default,QciProfilePredefined=qci3              dscp 42
set  QciTable=default,QciProfilePredefined=qci4              dscp 39
set  QciTable=default,QciProfilePredefined=qci5              dscp 48
set  QciTable=default,QciProfilePredefined=qci6              dscp 38
set  QciTable=default,QciProfilePredefined=qci65             dscp 46
set  QciTable=default,QciProfilePredefined=qci66             dscp 46
set  QciTable=default,QciProfilePredefined=qci69             dscp 38
set  QciTable=default,QciProfilePredefined=qci7              dscp 36
set  QciTable=default,QciProfilePredefined=qci70             dscp 38
set  QciTable=default,QciProfilePredefined=qci8              dscp 34
set  QciTable=default,QciProfilePredefined=qci9              dscp 34


set  QciTable=default,QciProfilePredefined=qci65             priority 2
set  QciTable=default,QciProfilePredefined=qci66             priority 2
set  QciTable=default,QciProfilePredefined=qci69             priority 6


set  QciTable=default,QciProfilePredefined=qci65            priorityFraction 0
set  QciTable=default,QciProfilePredefined=qci66            priorityFraction 0
set  QciTable=default,QciProfilePredefined=qci69            priorityFraction 0
set  QciTable=default,QciProfilePredefined=qci70          priorityFraction  5
set . enableSinrUplinkClpc true
set EUtranCellTDD=$nodenameT.* pdschTypeBGain 1
set EUtranCellFDD=$nodenameF21   physicalLayerSubCellId 0
set EUtranCellFDD=$nodenameF22   physicalLayerSubCellId  1
set EUtranCellFDD=$nodenameF23   physicalLayerSubCellId 2
set ENodeBFunction=1                                        srsPeriodicityTdd 20
set ENodeBFunction=1                                        srsPeriodicityFdd 40

set . hysteresisA1A2SearchRsrp 10
set EUtranCellTDD=$nodenameT.*,GeranFreqGroupRelation=1 qRxLevMin         -105

lt all

confb+
gs+

set AntennaUnitGroup=1,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameT21
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameF21
set AntennaUnitGroup=2,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameT22
set AntennaUnitGroup=2,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameF22
set AntennaUnitGroup=1,AntennaNearUnit=1,RetSubUnit=Y1  userLabel $nodenameT21
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=Y2  userLabel $nodenameF21
set AntennaUnitGroup=21,AntennaNearUnit=1,RetSubUnit=Y1 userLabel  $nodenameT22
set AntennaUnitGroup=21,AntennaNearUnit=2,RetSubUnit=Y2userLabel  $nodenameF22

set AntennaUnitGroup=1,AntennaNearUnit=1,RetSubUnit=1  userLabel $nodenameT21
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=2  userLabel $nodenameF21
set AntennaUnitGroup=21,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameT22
set AntennaUnitGroup=21,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameF22




set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -110
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1   480

set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -110
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1   480

set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 32
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set ENodeBFunction=1,Rrc=1                                  t301              400
set ENodeBFunction=1,Rrc=1                                  t301Br            0
set ENodeBFunction=1,Rrc=1                                  t301Nb            10000

set . egressQosMarking  QosProfiles=1,DscpPcpMap=1
set .dscpSectorControlUL 48


confb+
gs+

lt all

$date = `date +%y%m%d_%H%M`
cvms PRE

st cell


set  featurestate=CXC4012218   featurestate   1
set  featurestate=CXC4012371   featurestate   1
set  featurestate=CXC4012504   featurestate   1
set  featurestate=CXC4012381   featurestate   1


cr ENodeBFunction=1,GUtraNetwork=1

crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=624096-30
arfcn 624096
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
userLabel
end

#lset   GUtranSyncSignalFrequency=624096-30  bandList   77,78

ma L18_ACell ^eutrancellFDD= FreqBand 3
for $mo in L18_ACell
$cell1 = rdn($mo)
pr $cell1$


crn $cell1,GUtranFreqRelation=624096
allowedPlmnList
anrMeasOn true
b1ThrRsrpFreqOffset 0
b1ThrRsrqFreqOffset 0
cellReselectionPriority -1
connectedModeMobilityPrio 1
deriveSsbIndexFromCell false
endcB1MeasPriority 5
gUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency=624096-30
pMaxNR 26
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 4
threshXHighQ 0
threshXLow 0
threshXLowQ 0
end
done

mr L18_ACell

ma L9_ACell ^eutrancellFDD= FreqBand 8
for $mo in L9_ACell
$cell2 = rdn($mo)
pr $cell2$

crn $cell2,GUtranFreqRelation=624096
allowedPlmnList
anrMeasOn true
b1ThrRsrpFreqOffset 0
b1ThrRsrqFreqOffset 0
cellReselectionPriority -1
connectedModeMobilityPrio 1
deriveSsbIndexFromCell false
endcB1MeasPriority 5
gUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency=624096-30
pMaxNR 26
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 4
threshXHighQ 0
threshXLow 0
threshXLowQ 0
end
done

mr L9_ACell

ma T41_ACell ^eutrancellTDD= FreqBand 41
for $mo in T41_ACell
$cell3 = rdn($mo)
pr $cell3$


crn $cell3,GUtranFreqRelation=624096
allowedPlmnList
anrMeasOn true
b1ThrRsrpFreqOffset 0
b1ThrRsrqFreqOffset 0
cellReselectionPriority -1
connectedModeMobilityPrio 1
deriveSsbIndexFromCell false
endcB1MeasPriority 5
gUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency=624096-30
pMaxNR 26
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 4
threshXHighQ 0
threshXLow 0
threshXLowQ 0
end
done

mr T41_ACell

ma T40_ACell ^eutrancellTDD= FreqBand 40
for $mo in T40_ACell
$cell4 = rdn($mo)
pr $cell4

gs+
crn $cell4,GUtranFreqRelation=624096
allowedPlmnList
anrMeasOn true
b1ThrRsrpFreqOffset 0
b1ThrRsrqFreqOffset 0
cellReselectionPriority -1
connectedModeMobilityPrio 1
deriveSsbIndexFromCell false
endcB1MeasPriority 5
gUtranSyncSignalFrequencyRef GUtraNetwork=1,GUtranSyncSignalFrequency=624096-30
pMaxNR 26
qOffsetFreq 0
qQualMin 0
qRxLevMin -124
threshXHigh 4
threshXHighQ 0
threshXLow 0
threshXLowQ 0
end
done

mr T40_ACell

set   GUtranFreqRelation=624096   cellReselectionPriority   -1
set   GUtranFreqRelation=624096   connectedModeMobilityPrio   -1
set   GUtranFreqRelation=624096   pMaxNR   26
set   GUtranFreqRelation=624096   qRxLevMin   -124
set   GUtranFreqRelation=624096   anrMeasOn  true

set   ^EutranCellFDD|^EutranCellTDD   endcAllowedPlmnList   mcc=404,mnc=11,mnclength=2
set   ^EutranCellFDD|^EutranCellTDD   primaryUpperLayerInd   0
set   ^EutranCellFDD|^EutranCellTDD  upperLayerAutoConfEnabled   false

set   ENodeBFunction   endcAllowed   TRUE
set   ENodeBFunction   endcDataUsageReportEnabled   TRUE
set   ^EutranCellFDD|^EutranCellTDD   endcB1MeasGapConfig   1
set   ReportConfigB1GUtra   b1ThresholdRsrp   -110
set   UeMeasControl   maxMeasB1Endc   3
set   UeMeasControl   endcMeasTime   2000
set   UeMeasControl   endcMeasRestartTime   -1
set   UeMeasControl   endcB1MeasWindow   40
set   ReportConfigB1GUtra   triggerQuantityB1   0
set   ReportConfigB1GUtra   hysteresisB1   0
set   ReportConfigB1GUtra   timeToTriggerB1   480
set   ENodeBFunction   endcSplitAllowedNonDynPwrShUe   FALSE
set   ENodeBFunction=1     endcSplitAllowedMoVoice false
set   ^EutranCellFDD|^EutranCellTDD   lbActionForEndcUe   0
set   ^EutranCellFDD|^EutranCellTDD   loopingEndcProtectionEnabled   TRUE
set   ^EutranCellFDD|^EutranCellTDD   loopingEndcShortScgSessTime   200
set   ^EutranCellFDD|^EutranCellTDD   loopingEndcConsecFailThr   3
set   ^EutranCellFDD|^EutranCellTDD   loopingEndcBackoffDuration   1500
set   ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          cellAddRsrpThresholdNR   -116
set   ^EutranCellFDD|^EutranCellTDD   endcSetupDlPktVolThr   0
set   ^EutranCellFDD|^EutranCellTDD   endcSetupDlPktAgeThr   0
set   GUtranFreqRelation=624096   endcB1MeasPriority   5
set   EUtranFreqRelation=3601   endcHoFreqPriority   4
set   EUtranFreqRelation=1421   endcHoFreqPriority   5
set   EUtranFreqRelation=40940   endcHoFreqPriority   3
set   ReportConfigA5EndcHo   triggerQuantityA5   0
set   ReportConfigA5EndcHo   a5Threshold1Rsrp   -44
set   ReportConfigA5EndcHo   a5Threshold2Rsrp   -112
set   ReportConfigA5EndcHo   reportAmountA5   0
set   ReportConfigA5EndcHo   reportIntervalA5   2
set   ReportConfigA5EndcHo   timeToTriggerA5   100
set   ReportConfigA5EndcHo   hysteresisA5   10

##  Create New MO UePolicyOptimization

cr ENodeBFunction=1,UePolicyOptimization=1
set   UePolicyOptimization=1   endcAwareImc   1
set   UePolicyOptimization=1   coverageAwareImc   FALSE
set   UePolicyOptimization=1   loadAwareImc   TRUE
set   EutranCellFDD|TDD   subscriptionRatioHighThresh   600
set   UePolicyOptimization=1   t320   30
set   EUtranFreqRelation=3601   endcAwareIdleModePriority   4
set   EUtranFreqRelation=1421   endcAwareIdleModePriority   5
set   EUtranFreqRelation=40940   endcAwareIdleModePriority   3

set   ENodeBFunction   zzzTemporary81   1

cr   ENodeBFunction=1,EndcProfile=IMS_SIGNALING
cr   ENodeBFunction=1,EndcProfile=VOIP
cr   ENodeBFunction=1,EndcProfile=MBB
set   EndcProfile=IMS_SIGNALING   meNbS1TermReqArpLev   15
set   EndcProfile=IMS_SIGNALING   splitNotAllowedUeArpLev   0
set   EndcProfile=VOIP   meNbS1TermReqArpLev   15
set   EndcProfile=VOIP   splitNotAllowedUeArpLev   15
set   EndcProfile=MBB   meNbS1TermReqArpLev   0
set   EndcProfile=MBB   splitNotAllowedUeArpLev   0
set   QciTable=default,QciProfilePredefined=qci5$   endcProfileRef   ENodeBFunction=1,EndcProfile=IMS_SIGNALING
set   QciTable=default,QciProfilePredefined=qci1$   endcProfileRef   ENodeBFunction=1,EndcProfile=VOIP
set   QciTable=default,QciProfilePredefined=qci6$   endcProfileRef   ENodeBFunction=1,EndcProfile=MBB
set   QciTable=default,QciProfilePredefined=qci7$   endcProfileRef   ENodeBFunction=1,EndcProfile=MBB
set   QciTable=default,QciProfilePredefined=qci8$   endcProfileRef   ENodeBFunction=1,EndcProfile=MBB
set   QciTable=default,QciProfilePredefined=qci9$   endcProfileRef   ENodeBFunction=1,EndcProfile=MBB

set   ANRFunctionNR   anrStateNR   1
set   ENodeBFunction   endcX2IpAddrViaS1Active   TRUE
set   ENodeBFunction   zzzTemporary74   1
set   AnrFunction   removeNrelTime   7
set   AnrFunction   removeNcellTime   30
set   AnrFunction   removeNgnbTime   7
set   Rcs=1 tInactivityTimer   10

cr ENodeBFunction=1,PmFlexCounterFilter=5
cr ENodeBFunction=1,PmFlexCounterFilter=6
cr ENodeBFunction=1,PmFlexCounterFilter=7

lset ENodeBFunction=1,PmFlexCounterFilter=5 endcFilterEnabled true
lset ENodeBFunction=1,PmFlexCounterFilter=5 endcFilterMin 0
lset ENodeBFunction=1,PmFlexCounterFilter=5 uePowerClassFilterEnabled false
wait 4
lset ENodeBFunction=1,PmFlexCounterFilter=6 endcFilterEnabled true
lset ENodeBFunction=1,PmFlexCounterFilter=6 endcFilterMin 1
lset ENodeBFunction=1,PmFlexCounterFilter=6 uePowerClassFilterEnabled false
wait 4
lset ENodeBFunction=1,PmFlexCounterFilter=7 endcFilterEnabled true
lset ENodeBFunction=1,PmFlexCounterFilter=7 endcFilterMin 2
lset ENodeBFunction=1,PmFlexCounterFilter=7 uePowerClassFilterEnabled false

confb-
gs-
set   PmFlexCounterFilter=6   endcFilterEnabled   true
y
set   PmFlexCounterFilter=7   endcFilterEnabled   true
y
set . endcB1MeasGapConfig 0
set . lbActionForEndcUe 1
set . endcSetupDlPktVolThr 100
set EndcProfile=IMS_SIGNALING                               meNbS1TermReqArpLev 15
set . smtcDuration  1
set . smtcOffset  0
set . smtcPeriodicity  20
set . smtcScs  30
set . upperLayerAutoConfEnabled  1
set . primaryUpperLayerInd  1
set . endcAllowed  TRUE
set . endcB1MeasGapConfig  0
set . triggerQuantityB1  0
set . maxMeasB1Endc  3
set . endcMeasTime  2000
set . endcMeasRestartTime  -1
set . endcB1MeasWindow  40
set . endcSplitAllowedNonDynPwrShUe  FALSE
set . endcSplitAllowedMoVoice  FALSE
set . lbActionForEndcUe  1
set . endcSetupDlPktVolThr  100
set . endcSetupDlPktAgeThr  0
set . t320  30
set . meNbS1TermReqArpLev  15EndcProfile=IMS_SIGNALING                               meNbS1TermReqArpLev 15
set . anrStateNR  1
set . endcX2IpAddrViaS1Active  TRUE
set . removeNrelTime  7
set . removeNcellTime  30
set . removeNgnbTime  7
set . tInactivityTimer  10
set . loopingEndcProtectionEnabled  TRUE
set . loopingEndcShortScgSessTime  1500
set . loopingEndcConsecFailThr  3
set . loopingEndcBackoffDuration  200
set . cellAddRsrpThresholdNR  -114
set . anrMeasOn  TRUE
set . pMaxNR  26
set . endcB1MeasPriority  5
set . loadAwareImc  TRUE
set . anrMeasOn   TRUE
set . endcDataUsageReportEnabled  1


set CXC4012218|CXC4012504|CXC4012381|CXC4010620   featurestate 1
set . pdcchCfiMode 5
set . pdcchFlexibleBlerEnabled true

set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 endcAwareIdleModePriority 7
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 endcAwareIdleModePriority 6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 endcAwareIdleModePriority 5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601  voicePrio 5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421  voicePrio 6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 voicePrio 7

set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421   cellReselectionPriority 6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601   cellReselectionPriority 5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 cellReselectionPriority 7

set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421  connectedModeMobilityPrio  6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 connectedModeMobilityPrio  5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940  connectedModeMobilityPrio  7




get CXC4012218|CXC4012371|CXC4012504|CXC4012381







set . vswrSupervisionSensitivity 100
set . vswrSupervisionActive true
deb rfport
    

deb cell


st cell


confb+
gs+

set AntennaUnitGroup=1,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameT21
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameF21
set AntennaUnitGroup=2,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameT22
set AntennaUnitGroup=2,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameF22
set AntennaUnitGroup=1,AntennaNearUnit=1,RetSubUnit=Y1  userLabel $nodenameT21
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=Y2  userLabel $nodenameF21
set AntennaUnitGroup=21,AntennaNearUnit=1,RetSubUnit=Y1 userLabel  $nodenameT22
set AntennaUnitGroup=21,AntennaNearUnit=2,RetSubUnit=Y2userLabel  $nodenameF22

set AntennaUnitGroup=1,AntennaNearUnit=1,RetSubUnit=1  userLabel $nodenameT21
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=2  userLabel $nodenameF21
set AntennaUnitGroup=21,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameT22
set AntennaUnitGroup=21,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameF22


 set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=Y1 userLabel $nodenameF21
 set AntennaUnitGroup=11,AntennaNearUnit=2,RetSubUnit=Y2 userLabel $nodenameF21
 set AntennaUnitGroup=11,AntennaNearUnit=3,RetSubUnit=R1 userLabel $nodenameF11
 set AntennaUnitGroup=11,AntennaNearUnit=4,RetSubUnit=Y3 userLabel $nodenameT21
 set AntennaUnitGroup=11,AntennaNearUnit=5,RetSubUnit=Y4 userLabel $nodenameT21
 set AntennaUnitGroup=12,AntennaNearUnit=1,RetSubUnit=Y1 userLabel $nodenameF22
 set AntennaUnitGroup=12,AntennaNearUnit=2,RetSubUnit=Y2 userLabel $nodenameF22
 set AntennaUnitGroup=12,AntennaNearUnit=3,RetSubUnit=R1 userLabel $nodenameF12
 set AntennaUnitGroup=12,AntennaNearUnit=4,RetSubUnit=Y3 userLabel $nodenameT22
 set AntennaUnitGroup=12,AntennaNearUnit=5,RetSubUnit=Y4 userLabel $nodenameT22
 set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=Y1 userLabel $nodenameF23
 set AntennaUnitGroup=13,AntennaNearUnit=2,RetSubUnit=Y2 userLabel $nodenameF23
 set AntennaUnitGroup=13,AntennaNearUnit=3,RetSubUnit=R1 userLabel $nodenameF13
 set AntennaUnitGroup=13,AntennaNearUnit=4,RetSubUnit=Y3 userLabel $nodenameT23
 set AntennaUnitGroup=13,AntennaNearUnit=5,RetSubUnit=Y4 userLabel $nodenameT23
 confbd-
 gs-

lset EUtranCellFDD=.*F2(1|2|3|4),UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellFDD=.*F1(1|2|3|4),UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2
lset EUtranCellTDD=.*,UeMeasControl=1,ReportConfigSearch=1 qciA1A2ThrOffsets a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=4,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2

lset EUtranCellFDD=.*F2(1|2|3|4),EUtranFreqRelation= eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellFDD=.*F1(1|2|3|4),EUtranFreqRelation=.* eutranFreqToQciProfileRelation a5Thr1RsrpFreqQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
lset EUtranCellTDD=.*,EUtranFreqRelation= eutranFreqToQciProfileRelation a1a2ThrRsrpQciOffset=4,a5Thr2RsrpFreqQciOffset=4,a5Thr1RsrqFreqQciOffset=0,a5Thr2RsrqFreqQciOffset=0,atoThresh1QciProfileHandling=0,atoThresh2QciProfileHandling=0,lbA5Threshold2RsrpOffset=0,lbA5Threshold2RsrqOffset=0,lbQciProfileHandling=1,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1




set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=1421  eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=3601 eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=40940 eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=415  eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4

set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421  eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 eutranFreqToQciProfileRelation  a5Thr1RsrpFreqQciOffset=4
set . a2CriticalThresholdRsrp -123
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -110
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1   480

set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp   -110
set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1   480

set ENodeBFunction=1,RadioBearerTable=default,DataRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,RadioBearerTable=default,SignalingRadioBearer=1 dlMaxRetxThreshold 16
set ENodeBFunction=1,Rrc=1                                  t301              400
set ENodeBFunction=1,Rrc=1                                  t301Br            0
set ENodeBFunction=1,Rrc=1                                  t301Nb            10000

set . egressQosMarking  QosProfiles=1,DscpPcpMap=1
set . dscpSectorControlUL 48
set . hysteresisA1A2SearchRsrp 10


confbd+
gs+
set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=2 userLabel $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=3 userLabel $nodenameF11
set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=4 userLabel $nodenameT21
set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=5 userLabel $nodenameT21
set AntennaUnitGroup=12,AntennaNearUnit=1,RetSubUnit=3 userLabel $nodenameF22
set AntennaUnitGroup=12,AntennaNearUnit=1,RetSubUnit=4 userLabel $nodenameF22
set AntennaUnitGroup=12,AntennaNearUnit=1,RetSubUnit=5 userLabel $nodenameF12
set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=1 userLabel $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=2 userLabel $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=3 userLabel $nodenameF13
set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=4 userLabel $nodenameT23
set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=5 userLabel $nodenameT23
confbd-
gs-




set AntennaUnitGroup=21,AntennaNearUnit=1,RetSubUnit=1    userlabel $nodenameF11
set AntennaUnitGroup=21,AntennaNearUnit=2,RetSubUnit=2    userlabel $nodenameF21
set AntennaUnitGroup=21,AntennaNearUnit=3,RetSubUnit=3    userlabel $nodenameF21
set AntennaUnitGroup=21,AntennaNearUnit=4,RetSubUnit=4    userlabel $nodenameT21
set AntennaUnitGroup=21,AntennaNearUnit=5,RetSubUnit=5    userlabel $nodenameT21

set AntennaUnitGroup=22,AntennaNearUnit=1,RetSubUnit=1    userlabel $nodenameF12
set AntennaUnitGroup=22,AntennaNearUnit=2,RetSubUnit=2    userlabel $nodenameF22
set AntennaUnitGroup=22,AntennaNearUnit=3,RetSubUnit=3    userlabel $nodenameF22
set AntennaUnitGroup=22,AntennaNearUnit=4,RetSubUnit=4    userlabel $nodenameT22
set AntennaUnitGroup=22,AntennaNearUnit=5,RetSubUnit=5    userlabel $nodenameT22

set AntennaUnitGroup=22,AntennaNearUnit=1,RetSubUnit=1    userlabel $nodenameF13
set AntennaUnitGroup=22,AntennaNearUnit=2,RetSubUnit=2    userlabel $nodenameF23
set AntennaUnitGroup=22,AntennaNearUnit=3,RetSubUnit=3    userlabel $nodenameF23
set AntennaUnitGroup=22,AntennaNearUnit=4,RetSubUnit=4    userlabel $nodenameT23
set AntennaUnitGroup=22,AntennaNearUnit=5,RetSubUnit=5    userlabel $nodenameT23


set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=1    userlabel $nodenameF11
set AntennaUnitGroup=11,AntennaNearUnit=2,RetSubUnit=2    userlabel $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=3,RetSubUnit=3    userlabel $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=4,RetSubUnit=4    userlabel $nodenameT21
set AntennaUnitGroup=11,AntennaNearUnit=4,RetSubUnit=5    userlabel $nodenameT21


set AntennaUnitGroup=12,AntennaNearUnit=1,RetSubUnit=1    userlabel $nodenameF12
set AntennaUnitGroup=12,AntennaNearUnit=2,RetSubUnit=2    userlabel $nodenameF12
set AntennaUnitGroup=12,AntennaNearUnit=3,RetSubUnit=3    userlabel $nodenameF22
set AntennaUnitGroup=12,AntennaNearUnit=4,RetSubUnit=4    userlabel $nodenameT22
set AntennaUnitGroup=12,AntennaNearUnit=4,RetSubUnit=5    userlabel $nodenameT22

set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=1    userlabel $nodenameF13
set AntennaUnitGroup=13,AntennaNearUnit=2,RetSubUnit=2    userlabel $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=3,RetSubUnit=3    userlabel $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=4,RetSubUnit=4    userlabel $nodenameT23
set AntennaUnitGroup=13,AntennaNearUnit=4,RetSubUnit=5    userlabel $nodenameT23


set AntennaUnitGroup=11,AntennaNearUnit=RET-1,RetSubUnit=1 userlabel $nodenameF11
set AntennaUnitGroup=11,AntennaNearUnit=RET-1,RetSubUnit=2 userlabel $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=RET-1,RetSubUnit=3 userlabel $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=RET-1,RetSubUnit=4 userlabel $nodenameT21
set AntennaUnitGroup=11,AntennaNearUnit=RET-1,RetSubUnit=5 userlabel $nodenameT21


set AntennaUnitGroup=12,AntennaNearUnit=RET-1,RetSubUnit=1 userlabel $nodenameF12
set AntennaUnitGroup=12,AntennaNearUnit=RET-1,RetSubUnit=2 userlabel $nodenameF22
set AntennaUnitGroup=12,AntennaNearUnit=RET-1,RetSubUnit=3 userlabel $nodenameF22
set AntennaUnitGroup=12,AntennaNearUnit=RET-1,RetSubUnit=4 userlabel $nodenameT22
set AntennaUnitGroup=12,AntennaNearUnit=RET-1,RetSubUnit=5 userlabel $nodenameT22

set AntennaUnitGroup=13,AntennaNearUnit=RET-1,RetSubUnit=1 userlabel $nodenameF13
set AntennaUnitGroup=13,AntennaNearUnit=RET-1,RetSubUnit=2 userlabel $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=RET-1,RetSubUnit=3 userlabel $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=RET-1,RetSubUnit=4 userlabel $nodenameT23
set AntennaUnitGroup=13,AntennaNearUnit=RET-1,RetSubUnit=5 userlabel $nodenameT23

set AntennaUnitGroup=11,AntennaNearUnit=1,RetSubUnit=R1 userLabel   $nodenameF11
set AntennaUnitGroup=11,AntennaNearUnit=2,RetSubUnit=Y1 userLabel   $nodenameF21
set AntennaUnitGroup=11,AntennaNearUnit=3,RetSubUnit=Y2 userLabel   $nodenameF21
set AntennaUnitGroup=12,AntennaNearUnit=1,RetSubUnit=R1 userLabel   $nodenameF12
set AntennaUnitGroup=12,AntennaNearUnit=2,RetSubUnit=Y1 userLabel   $nodenameF12
set AntennaUnitGroup=12,AntennaNearUnit=3,RetSubUnit=Y2 userLabel   $nodenameF22
set AntennaUnitGroup=13,AntennaNearUnit=1,RetSubUnit=R1 userLabel   $nodenameF13
set AntennaUnitGroup=13,AntennaNearUnit=2,RetSubUnit=Y1 userLabel   $nodenameF23
set AntennaUnitGroup=13,AntennaNearUnit=3,RetSubUnit=Y2 userLabel   $nodenameF23


set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=2 userLabel $nodenameT22
set AntennaUnitGroup=1,AntennaNearUnit=2,RetSubUnit=1  userLabel $nodenameT21

set ENodeBFunction=1,Rrc=1                                  t311              10000
set ENodeBFunction=1,Rrc=1                                  t311Nb            5000


set  QciTable=default,QciProfilePredefined=qci1              dscp 46
set  QciTable=default,QciProfilePredefined=qci2              dscp 44
set  QciTable=default,QciProfilePredefined=qci3              dscp 42
set  QciTable=default,QciProfilePredefined=qci4              dscp 39
set  QciTable=default,QciProfilePredefined=qci5              dscp 48
set  QciTable=default,QciProfilePredefined=qci6              dscp 38
set  QciTable=default,QciProfilePredefined=qci65             dscp 46
set  QciTable=default,QciProfilePredefined=qci66             dscp 46
set  QciTable=default,QciProfilePredefined=qci69             dscp 38
set  QciTable=default,QciProfilePredefined=qci7              dscp 36
set  QciTable=default,QciProfilePredefined=qci70             dscp 38
set  QciTable=default,QciProfilePredefined=qci8              dscp 34
set  QciTable=default,QciProfilePredefined=qci9              dscp 34


set  QciTable=default,QciProfilePredefined=qci65             priority 2
set  QciTable=default,QciProfilePredefined=qci66             priority 2
set  QciTable=default,QciProfilePredefined=qci69             priority 6

set . ulHarqVolteBlerTarget 2
set  ENodeBFunction=1,Rrc=1 tWaitForRrcConnReest             9


set  QciTable=default,QciProfilePredefined=qci65            priorityFraction 0
set  QciTable=default,QciProfilePredefined=qci66            priorityFraction 0
set  QciTable=default,QciProfilePredefined=qci69            priorityFraction 0
set  QciTable=default,QciProfilePredefined=qci70          priorityFraction  5

crn ENodeBFunction=1,TimerProfile=0
tRelocOverall 20
tRrcConnReest 2
tRrcConnectionReconfiguration 9
tWaitForRrcConnReest 9
end
gs-

set QciTable=default,QciProfilePredefined=qci1              inactivityTimerOffset 30

set EUtranCellFDD=$nodenameF.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -115
set EUtranCellTDD=$nodenameT.*,UeMeasControl=1,ReportConfigA5=1 a5Threshold2Rsrp -115
set . a1a2SearchThresholdRsrp -115

set ENodeBFunction=1,Rrc=1                                  tWaitForRrcConnReest 10


set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 voicePrio         7
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 voicePrio         6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 voicePrio        5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=415  voicePrio         1
set EUtranCellTDD=$nodenameT.*,GeranFreqGroupRelation=1 voicePrio         0
set EUtranCellTDD=$nodenameT.*,GUtranFreqRelation=624096 voicePrio         0


set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=1421 voicePrio         7
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=3601 voicePrio         6
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=40940 voicePrio         5
set EUtranCellFDD=$nodenameF.*,GeranFreqGroupRelation=1 voicePrio         0
set EUtranCellFDD=$nodenameF.*,GUtranFreqRelation=624096 voicePrio         0

set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 connectedModeMobilityPrio         6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 connectedModeMobilityPrio         5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 connectedModeMobilityPrio         7
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=415  connectedModeMobilityPrio         1
set EUtranCellTDD=$nodenameT.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio         0
set EUtranCellTDD=$nodenameT.*,GUtranFreqRelation=624096 connectedModeMobilityPrio         0


set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=1421 connectedModeMobilityPrio         6
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=3601 connectedModeMobilityPrio         5
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=40940 connectedModeMobilityPrio         7
set EUtranCellFDD=$nodenameF.*,GeranFreqGroupRelation=1 connectedModeMobilityPrio         0
set EUtranCellFDD=$nodenameF.*,GUtranFreqRelation=624096 connectedModeMobilityPrio         0

set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=1421 cellReselectionPriority         6
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=3601 cellReselectionPriority         5
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=40940 cellReselectionPriority         7
set EUtranCellTDD=$nodenameT.*,EUtranFreqRelation=415  cellReselectionPriority         1
set EUtranCellTDD=$nodenameT.*,GeranFreqGroupRelation=1 cellReselectionPriority         0
set EUtranCellTDD=$nodenameT.*,GUtranFreqRelation=624096 cellReselectionPriority         0


set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=1421 cellReselectionPriority         6
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=3601 cellReselectionPriority         5
set EUtranCellFDD=$nodenameF.*,EUtranFreqRelation=40940 cellReselectionPriority         7
set EUtranCellFDD=$nodenameF.*,GeranFreqGroupRelation=1 cellReselectionPriority         0
set EUtranCellFDD=$nodenameF.*,GUtranFreqRelation=624096 cellReselectionPriority         0

cvms pre-SLEEP

lt all

confb+
gs+

*******************Cell Sleep Mode****************************************************************************

set eutrancell.*=.*,CellSleepFunction=1 capCellWakeUpDlPrbOffset 5
set eutrancell.*=.*,CellSleepFunction=1 capCellWakeUpRrcOffset 5
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 capCellSleepMonitorDurTimer 15
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 capCellDlPrbSleepThreshold 30
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 capCellRrcConnSleepThreshold  5
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 capCellSleepProhibitInterval 0
set . covCellWakeUpSeqTimer 15
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 covCellWakeUpMonitorDurTimer 15
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 covCellDlPrbWakeUpThreshold 30
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 covCellRrcConnWakeUpThreshold 20
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 covCellRrcConnWakeUpThresHigh 30
set ENodeBFunction=1,EUtranCell.*=.*.*,CellSleepFunction=1 covCellDlPrbWakeUpThresHigh 35
set ENodeBFunction=1,CellSleepNodeFunction=1 seqWakeUpEnabled true
set ENodeBFunction=1,EUtranCell.*=.*,CellSleepFunction=1 sleepStartTime 18:30
set ENodeBFunction=1,EUtranCell.*=.*,CellSleepFunction=1 sleepEndTime 00:30
set eutrancell.*=.*,CellSleepFunction=1 wakeUpTrafficCriteria 0

set ENodeBFunction=1,CellSleepNodeFunction=1 csmMinHitRateForCovCell 50
set SectorCarrier=  microSleepTxEnabled true


##--------------------------- LTE Cell Sleep Activation - L900 (CoverageCell) -------------------------------------
set ENodeBFunction=1,EUtranCellFDD=.*[F1][789],CellSleepFunction=1 sleepMode 0
set ENodeBFunction=1,EUtranCellFDD=.*[F1][789],CellSleepFunction=1 coverageCellDiscovery 0
set EUtranCellFDD=.*[F1][789],EUtranFreqRelation=.* cellSleepCovCellMeasOn false
set EUtranCellFDD=.*[F1][789],CellSleepFunction=1 capCellSleepProhibitInterval 24
##--------------------------- LTE Cell Sleep Activation - TDD (Capacity Cell) -------------------------------------
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1 sleepMode 1
set ENodeBFunction=1,EUtranCellTDD=.*,CellSleepFunction=1 coverageCellDiscovery 1
set EUtranCellTDD=.*,EUtranFreqRelation=.* cellSleepCovCellMeasOn true

##--------------------------- LTE Cell Sleep Activation - 1800 (Capacity Cell) -------------------------------------
set ENodeBFunction=1,EUtranCellFDD=.*[F2][789],CellSleepFunction=1 sleepMode 1
set ENodeBFunction=1,EUtranCellFDD=.*[F2][789],CellSleepFunction=1 coverageCellDiscovery 1
set EUtranCellFDD=.*[F2][123456],EUtranFreqRelation=.* cellSleepCovCellMeasOn true


##--------------------------- LTE Cell Sleep Activation - 2100 (Capacity Cell) -------------------------------------
set ENodeBFunction=1,EUtranCellFDD=.*[F3][789],CellSleepFunction=1 sleepMode 1
set ENodeBFunction=1,EUtranCellFDD=.*[F3][789],CellSleepFunction=1 coverageCellDiscovery 1
set EUtranCellFDD=.*[F3][123456],EUtranFreqRelation=.* cellSleepCovCellMeasOn true

hget EUtranCellTDD=.*,MimoSleepFunction=1 SleepMode

set EUtranCellTDD=.*,MimoSleepFunction=1 sleepMode 6

hget CXC4012533|CXC4011958|CXC4011808 featurestate|description|licenseState

set CXC4012533 featurestate 1
set CXC4011958 featurestate 1
set CXC4011808 featurestate 1

hget CXC4012533|CXC4011958|CXC4011808 featurestate|description|licenseState

confb-
gs-


cvms POST_SLEPP_Function


cvms Post_Baseline_$date



confb-
gs-

"""


DEL_Vi_TN_RN_GPS_MME_SCRIPT = """
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
userLabel DSCP-PCP-Map
end
#END Transport=1,QosProfiles=1,DscpPcpMap=1 --------------------

ld Transport=1,EthernetPort=TN_IDL_B
lset Transport=1,EthernetPort=TN_IDL_B$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=GSM_ABIS,InterfaceIPv4=GSM_ABIS
lset Transport=1,Router=GSM_ABIS,InterfaceIPv4=GSM_ABIS$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_CP,InterfaceIPv6=LTE_CP
lset Transport=1,Router=LTE_CP,InterfaceIPv6=LTE_CP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP
lset Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

ld Transport=1,Router=LTE_OM,InterfaceIPv6=LTE_OM
lset Transport=1,Router=LTE_OM,InterfaceIPv6=LTE_OM$ egressQosMarking Transport=1,QosProfiles=1,DscpPcpMap=1

crn Transport=1,Router=LTE_UP,TwampResponder=1
ipAddress Transport=1,Router=LTE_UP,InterfaceIPv6=LTE_UP,AddressIPv6=LTE_UP
udpPort 4001
userLabel LTE_UP
end
#END Transport=1,Router=LTE_UP,TwampResponder=1 --------------------

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 10
betaIndex 2
bundlingActivated true
bundlingTimer 0
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

ld Transport=1,Synchronization=1 #SystemCreated
lset Transport=1,Synchronization=1$ fixedPosition true
lset Transport=1,Synchronization=1$ telecomStandard 1

crn Transport=1,Synchronization=1,RadioEquipmentClock=1
minQualityLevel qualityLevelValueOptionI=2,qualityLevelValueOptionII=2,qualityLevelValueOptionIII=1
end
#END Transport=1,Synchronization=1,RadioEquipmentClock=1 --------------------

crn Transport=1,Synchronization=1,TimeSyncIO=1
compensationDelay 0
encapsulation Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},SyncPort=1
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
eNodeBPlmnId mcc=404,mnc=11,mncLength=2
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


crn ENodeBFunction=1,GeraNetwork=1
end
#END ENodeBFunction=1,GeraNetwork=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
frequencyGroupId 1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=597
arfcnValueGeranDl 597
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=597 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=598
arfcnValueGeranDl 598
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=598 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=599
arfcnValueGeranDl 599
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=599 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=644
arfcnValueGeranDl 644
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=644 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=645
arfcnValueGeranDl 645
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=645 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=646
arfcnValueGeranDl 646
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=646 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=647
arfcnValueGeranDl 647
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=647 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=648
arfcnValueGeranDl 648
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=648 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=649
arfcnValueGeranDl 649
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=649 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=643
arfcnValueGeranDl 643
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=643 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=601
arfcnValueGeranDl 601
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=601 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=640
arfcnValueGeranDl 640
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=640 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=639
arfcnValueGeranDl 639
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=639 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=603
arfcnValueGeranDl 603
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=603 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=605
arfcnValueGeranDl 605
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=605 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=638
arfcnValueGeranDl 638
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=638 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=600
arfcnValueGeranDl 600
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=600 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=641
arfcnValueGeranDl 641
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=641 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=602
arfcnValueGeranDl 602
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=602 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=604
arfcnValueGeranDl 604
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=604 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=606
arfcnValueGeranDl 606
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=606 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=607
arfcnValueGeranDl 607
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=607 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=636
arfcnValueGeranDl 636
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=636 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=637
arfcnValueGeranDl 637
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=637 --------------------

crn ENodeBFunction=1,GeraNetwork=1,GeranFrequency=642
arfcnValueGeranDl 642
geranFreqGroupRef ENodeBFunction=1,GeraNetwork=1,GeranFreqGroup=1
end
#END ENodeBFunction=1,GeraNetwork=1,GeranFrequency=642 --------------------

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=default #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ aqmMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ dscp 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=default$ pdb 300
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ drxPriority 98
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ drxProfileRef ENodeBFunction=1,DrxProfile=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ dscp 46
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ harqPriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ inactivityTimerOffset 20
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ qciSubscriptionQuanta 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ relativePriority 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1$ rlcSNLength 10
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ drxPriority 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ dscp 44
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdb 150
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ pdbOffset 0
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ srsAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ tReorderingUl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ ulMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary3 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary4 -2000000000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci2$ zzzTemporary5 -2000000000

ld ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3 #SystemCreated
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ absPrioOverride 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ aqmMode 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ bitRateRecommendationEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ caOffloadingEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ counterActiveMode false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ dscp 42
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci3$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dataFwdPerQciEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ dscp 39
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci4$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ drxProfileRef ENodeBFunction=1,DrxProfile=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ dscp 48
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=2
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ serviceType 2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ schedulingAlgorithm 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci5$ tReorderingDl 35
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ dscp 38
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ priority 6
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ relativePriority 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6$ rohcForUlDataEnabled false
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ dscp 44
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdb 75
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdbOffset 50
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ priority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci65$ priorityFraction 7
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ dscp 44
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci66$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dataFwdPerQciEnabled true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMaxHARQTxQci 5
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMaxWaitingTime 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlMinBitRate 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ dscp 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=2
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdb 60
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ priority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci69$ priorityFraction 5
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ dscp 36
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdb 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ priority 7
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ relativePriority 40
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci7$ tReorderingUl 35
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ dscp 36
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ laaSupported false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci70$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ priority 8
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ relativePriority 20
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci8$ tReorderingUl 35
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
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dlResourceAllocationStrategy 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ drxPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ drxProfileRef ENodeBFunction=1,DrxProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ dscp 34
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ endcProfileRef ENodeBFunction=1,EndcProfilePredefined=1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ essResourceAllocationMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ harqPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ inactivityTimerOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ laaSupported true
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ lessMaxDelayThreshold 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ logicalChannelGroupRef ENodeBFunction=1,QciTable=default,LogicalChannelGroup=3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ paPartitionOverride false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdb 300
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdbOffset 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlcMode 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ pdcpSNLength 12
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ priority 9
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ priorityFraction 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ qciACTuning 1000
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ qciSubscriptionQuanta 100
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ relativePriority 20
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ resourceAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlcSNLength 10
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlfPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rlfProfileRef ENodeBFunction=1,RlfProfile=0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rohcEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ rohcForUlDataEnabled false
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ serviceType 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ schedulingAlgorithm 3
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ srsAllocationStrategy 1
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ timerPriority 0
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ tReorderingDl 35
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci9$ tReorderingUl 35
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
lset ENodeBFunction=1,Rrc=1$ t301 400
lset ENodeBFunction=1,Rrc=1$ t311 3000

set 0 Userlabel {Phy_SiteID_Userlabel}

confb-
gs-

#######################MME############################################

crn ENodeBFunction=1,TermPointToMme=INVIDL13DLH4MMEX01NK
administrativeState 1
ipv6Address1 2402:8100:12:7:0:12:0:9a
end
#END ENodeBFunction=1,TermPointToMme=INVIDL13DLH4MMEX01NK --------------------

crn ENodeBFunction=1,TermPointToMme=INVIDL13DLH4MMEX02NK
administrativeState 1
ipv6Address1 2402:8100:12:7:0:13:0:9a
end
#END ENodeBFunction=1,TermPointToMme=INVIDL13DLH4MMEX02NK --------------------

crn ENodeBFunction=1,TermPointToMme=INVIDL13NOD1MMEX01NK
administrativeState 1
ipv6Address1 2402:8100:17:18c::32
end
#END ENodeBFunction=1,TermPointToMme=INVIDL13NOD1MMEX01NK --------------------

crn ENodeBFunction=1,TermPointToMme=INVIDL13NOD1MMEX02NK
administrativeState 1
ipv6Address1 2402:8100:17:19c::32
end
#END ENodeBFunction=1,TermPointToMme=INVIDL13NOD1MMEX02NK --------------------

gs-
confb-

"""




################################################################################### 5G SCRIPS FOR INTEGRATION SCRIPTS ###################################################################################
DEL_Vi_5G_Cell_creation_Sctp_Endpoint_Creation = """
######################################################## IPV6 Interface for NR ####################################################################

cr Transport=1,Router=LTEUP,InterfaceIPv6=NR
VlanPort=TN_E_UP
false

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
address {NR_IP}
configurationMode 0
duidType 0
primaryAddress true
userLabel
end


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
address {NR_ENDC_IP}
configurationMode 0
duidType 0
primaryAddress false
userLabel
end

gs+

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2                                                                                                              
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2,Dst=default                                                                                                   
dst ::/0                                                                                                                                                          
end



crn Transport=1,Router=LTEUP,RouteTableIPv6Static=2,Dst=default,NextHop=1
address {NR_GW}
adminDistance 1
bfdMonitoring true
discard false
reference
end


##################################################################################### TN SCRIPT #########################################################################

crn Transport=1,QosProfiles=1,DscpPcpMap=1
defaultPcp 0
pcp0 0 1 2 3 5 7 9 11 13 15 17 19 21 23 25 27 29 31 33 35 36 37 38 39 41 43 45 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63
pcp1
pcp2 22 24 26
pcp3 6 8 10 30 32
pcp4 12 14 40
pcp5 4 28
pcp6 16 18 34 42 44
pcp7 20 46
userLabel Traffic
end


crn Transport=1,Router=LTEUP,TwampResponder=2
ipAddress Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=3
ipAddress Router=LTEUP,InterfaceIPv4={tnPortId}_UP,AddressIPv4={tnPortId}_UP
udpPort 4002
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

crn Transport=1,SctpProfile=1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatInterval 5000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
pathMaxRtx 4
primaryPathMaxRtx 0
sackTimer 100
transmitBufferSize 64
userLabel SCTP
end

crn Transport=1,SctpEndpoint=1
localIpAddress Transport=1,Router=LTECP,InterfaceIPv4={tnPortId}_CP,AddressIPv4={tnPortId}_CP
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2_ENDC
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

##########

crn Transport=1,SctpProfile=Node_Internal_F1
alphaIndex 3
assocMaxRtx 8
betaIndex 2
bundlingActivated true
bundlingAdaptiveActivated true
bundlingTimer 0
cookieLife 60
dscp 46
hbMaxBurst 1
heartbeatActivated true
heartbeatInterval 2000
incCookieLife 30
initARWnd 16384
initialHeartbeatInterval 500
initRto 2000
maxActivateThr 65535
maxBurst 4
maxInitRt 5
maxInStreams 2
maxOutStreams 2
maxRto 4000
maxSctpPduSize 1480
maxShutdownRt 5
minActivateThr 1
minRto 1000
noSwitchback true
pathMaxRtx 4
primaryPathAvoidance true
primaryPathMaxRtx 0
sackTimer 100
thrTransmitBuffer 48
thrTransmitBufferCongCeased 85
transmitBufferSize 64
end

cr Transport=1,Router=Node_Internal_F1

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP
aclEgress
aclIngress
arpTimeout 300
bfdProfile
bfdStaticRoutes 0
egressQosMarking
encapsulation
ingressQosMarking
ipOptionsDisabled false
loopback true
mtu 1500
pcpArp 6
routesHoldDownTimer
routingPolicyIngress
trackedInterface
userLabel
end

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
address 10.0.0.1/32
configurationMode 0
dhcpClientIdentifier
dhcpClientIdentifierType 0
primaryAddress true
userLabel
end
gs-

crn Transport=1,SctpEndpoint=F1_NRCUCP
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

############

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU
aclEgress
aclIngress
arpTimeout 300
bfdProfile
bfdStaticRoutes 0
egressQosMarking
encapsulation
ingressQosMarking
ipOptionsDisabled false
loopback true
mtu 1500
pcpArp 6
routesHoldDownTimer
routingPolicyIngress
trackedInterface
userLabel
end

crn Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
address 10.0.0.2/32
configurationMode 0
dhcpClientIdentifier
dhcpClientIdentifierType 0
primaryAddress true
userLabel
end
gs-

crn Transport=1,SctpEndpoint=F1_NRDU
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_DU,AddressIPv4=1
portNumber 38472
sctpProfile Transport=1,SctpProfile=Node_Internal_F1
end

###########

crn Transport=1,SctpEndpoint=NG
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 38412
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=X2
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 36422
sctpProfile Transport=1,SctpProfile=1
end

crn Transport=1,SctpEndpoint=F1
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
portNumber 38472
sctpProfile SctpProfile=1
userLabel
end

gs+                                                                                                                                                          
crn Transport=1,SctpEndpoint=F1_NRCUCP                                                                                                                       
dtls                                                                                                                                                         
dtlsNodeCredential                                                                                                                                           
dtlsSctpSecurityMode 0                                                                                                                                       
dtlsTrustCategory                                                                                                                                            
localIpAddress Transport=1,Router=Node_Internal_F1,InterfaceIPv4=NR_CUCP,AddressIPv4=1                                                                       
portNumber 38472                                                                                                                                             
sctpProfile SctpProfile=Node_Internal_F1                                                                                                                     
userLabel                                                                                                                                                    
end  


###########################################GNBCUUPFunction=1#############################################################################

crn GNBCUUPFunction=1
gNBId {gNBId}
gNBIdLength 26
pLMNIdList mcc=404,mnc=10
sNSSAIList
userLabel
end

crn GNBCUUPFunction=1,EndpointResource=1
end

crn GNBCUUPFunction=1,EndpointResource=1,LocalIpEndpoint=1
addressRef Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
interfaceList 4 5 7 6
end


ld GNBCUUPFunction=1
lset GNBCUUPFunction=1$ endpointResourceRef GNBCUUPFunction=1,EndpointResource=1



crn GNBCUUPFunction=1,CardinalityLimits=1
maxNgUPath 600
maxS1UPath 600
end

crn GNBCUUPFunction=1,GtpuSupervision=1
gtpuErrorIndDscp 40
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=S1
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 5
userLabel
end

crn GNBCUUPFunction=1,GtpuSupervision=1,GtpuSupervisionProfile=X2
endpointResourceRef
gtpuEchoDscp 32
gtpuEchoEnabled true
interfaceList 7
userLabel
end


####################################GNBDUFunction=1###################################

crn GNBDUFunction=1
gNBDUId 1
gNBDUName
gNBId {gNBId}
gNBIdLength 26
end

crn GNBDUFunction=1,EndpointResource=1
end

crn GNBDUFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 3
sctpEndpointRef Transport=1,SctpEndpoint=F1_NRDU
end

crn GNBDUFunction=1,TermPointToGNBCUCP=1
administrativeState 1
ipv4Address 10.0.0.1
ipv6Address ::
end

ld GNBDUFunction=1
lset GNBDUFunction=1$ endpointResourceRef GNBDUFunction=1,EndpointResource=1


crn GNBDUFunction=1,MassiveMimoSleep=1                                                                                                                                                                             
end 

crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                         
sleepMode 0                                                                                                                                                                                                        
switchDownMonitorDurTimer 60                                                                                                                                                                                       
switchDownMonitorDurTimerEco 300                                                                                                                                                                                   
switchDownPrbThreshDl 10                                                                                                                                                                                           
switchDownPrbThreshDlEco 15                                                                                                                                                                                        
switchDownPrbThreshUlEco 10                                                                                                                                                                                        
switchDownRrcConnThresh 10                                                                                                                                                                                         
switchDownRrcConnThreshEco 30                                                                                                                                                                                      
switchUpMonitorDurTimer 30                                                                                                                                                                                         
switchUpMonitorDurTimerEco 120                                                                                                                                                                                     
switchUpPrbThreshDl 20                                                                                                                                                                                             
switchUpPrbThreshDlEco 30                                                                                                                                                                                          
switchUpPrbThreshUlEco 15                                                                                                                                                                                          
switchUpRrcConnThresh 20                                                                                                                                                                                           
switchUpRrcConnThreshEco 50                                                                                                                                                                                        
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1                                                                                                                                                       
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBDUFunction=1,MassiveMimoSleep=1,MMimoSleepTimeGroup=1,MMimoSleepTimeWindow=1                                                                                                                                
dayOfWeek 0                                                                                                                                                                                                        
mMimoSleepProfileRef MassiveMimoSleep=1,MMimoSleepProfile=1                                                                                                                                                        
startTime 20:30                                                                                                                                                                                                    
stopTime 23:30                                                                                                                                                                                                     
end    


{DEL_Vi_CGSWITCH_SCRIPT}

############################GNBCUCPFunction=1####################################################


crn GNBCUCPFunction=1
gNBId {gNBId}
gNBIdLength 26
pLMNId mcc=404,mnc=10
end

crn GNBCUCPFunction=1,EndpointResource=1
end

ld GNBCUCPFunction=1
lset GNBCUCPFunction=1$ endpointResourceRef GNBCUCPFunction=1,EndpointResource=1

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=1
interfaceUsed 4
sctpEndpointRef SctpEndpoint=NG
end

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=2
interfaceUsed 7
sctpEndpointRef SctpEndpoint=X2
end

crn GNBCUCPFunction=1,EndpointResource=1,LocalSctpEndpoint=3
interfaceUsed 3
sctpEndpointRef SctpEndpoint=F1_NRCUCP
end

                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1                                                                                                                                                                                
demoteCellRelMobAttThresh                                                                                                                                                                                          
promoteCellRelMobAttThresh                                                                                                                                                                                         
removeEUtranFreqRelTime 10000                                                                                                                                                                                      
removeEnbTime 7                                                                                                                                                                                                    
removeFreqRelTime 15                                                                                                                                                                                               
removeGnbTime 7                                                                                                                                                                                                    
removeNrelTime 7                                                                                                                                                                                                   
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1                                                                                                                                                                
anrAutoCreateXnForEndc false                                                                                                                                                                                       
anrCgiMeasInterFreqMode 0                                                                                                                                                                                          
anrCgiMeasIntraFreqEnabled true                                                                                                                                                                                    
anrEndcX2Enabled true                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1,AnrFunctionNRUeCfg=Base                                                                                                                                        
anrRsrpThreshold -156                                                                                                                                                                                              
anrRsrqThreshold -435                                                                                                                                                                                              
anrSinrThreshold -230                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   

crn GNBCUCPFunction=1,CarrierAggregation=1                                                                                                                                                                         
end                                                                                                                                                                                                                
                                       
crn GNBCUCPFunction=1,CarrierAggregation=1,CaCellMeasProfile=1                                                                                                                                                     
ueConfGroupType 0                                                                                                                                                                                                  
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,CarrierAggregation=1,CaCellMeasProfile=1,CaCellMeasProfileUeCfg=Base                                                                                                                         
betterSCellReportConfigMode 0                                                                                                                                                                                      
prefUeGroupList                                                                                                                                                                                                    
rsrpBetterSCell hysteresis=10,offset=30,timeToTrigger=160                                                                                                                                                          
rsrpSCellCoverage hysteresis=10,threshold=-117,timeToTrigger=160,timeToTriggerA1=-1                                                                                                                                
rsrqSCellCoverage hysteresis=10,threshold=-435,timeToTrigger=160,timeToTriggerA1=-1                                                                                                                                
sCellCoverageTriggerQuantity 0                                                                                                                                                                                     
ueConfGroupList                                                                                                                                                                                                    
ueGroupList                                                                                                                                                                                                        
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                            

crn GNBCUCPFunction=1,IntraFreqMC=1                                                                                                                                                                                
sCellDepHEnabled true                                                                                                                                                                                              
end                                                                                                                                                                                                                
                                                   
crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1                                                                                                                                                       
ueConfGroupType 0                                                                                                                                                                                                  
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base                                                                                                                      
betterSpCellTriggerQuantity 0                                                                                                                                                                                      
endcActionEvalFail 1                                                                                                                                                                                               
prefUeGroupList                                                                                                                                                                                                    
rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
rsrqBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
sinrBetterSpCell hysteresis=10,offset=30,timeToTrigger=640                                                                                                                                                         
ueConfGroupList                                                                                                                                                                                                    
ueGroupList                                                                                                                                                                                                        
useT312BetterPCellCandidateA3 false                                                                                                                                                                                
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                


crn GNBCUCPFunction=1,NRNetwork=1
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30
arfcnValueNRDl 629952
bandListManual
smtcDuration 1
smtcOffset 0
smtcPeriodicity 20
smtcScs 30
ssRssiMeasIdle
ssbToMeasureIdle
end

crn GNBCUCPFunction=1,NRNetwork=1,NRFrequency=629952-30,NRFrequencyUeCfg=Base
prefUeGroupList
ssRssiMeasConnected
ssbToMeasureConnected
ueConfGroupList
ueGroupList
userLabel
end

crn GNBCUCPFunction=1,UeGroupSelection=1                                                                                                                                                                           
validityTimeEmergencyCause 6                                                                                                                                                                                       
validityTimeHighPrioAccCause 6                                                                                                                                                                                     
validityTimeMcsPrioAccCause 6                                                                                                                                                                                      
validityTimeMoDataCause 6                                                                                                                                                                                          
validityTimeMoSignallingCause 6                                                                                                                                                                                    
validityTimeMoSmsCause 6                                                                                                                                                                                           
validityTimeMoVideoCallCause 6                                                                                                                                                                                     
validityTimeMoVoiceCallCause 6                                                                                                                                                                                     
validityTimeMpsPrioAccCause 6                                                                                                                                                                                      
validityTimeMtAccessCause 6                                                                                                                                                                                        
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,ImeiSvGroups=1                                                                                                                                                            
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,PrefUeGroupSelectionProfile=QCI6                                                                                                                                          
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
prefUeGroupId 6                                                                                                                                                                                                    
prefUeGroupPriority 65534                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,PrefUeGroupSelectionProfile=QCI7                                                                                                                                          
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
prefUeGroupId 7                                                                                                                                                                                                    
prefUeGroupPriority 1000                                                                                                                                                                                           
selectionCriteria qci==7                                                                                                                                                                                           
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeGroupSelectionProfile=QCI6                                                                                                                                              
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
selectionProbability 100                                                                                                                                                                                           
ueGroupId 6                                                                                                                                                                                                        
ueGroupPriority 65534                                                                                                                                                                                              
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeGroupSelectionProfile=QCI7                                                                                                                                              
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
selectionProbability 100                                                                                                                                                                                           
ueGroupId 7                                                                                                                                                                                                        
ueGroupPriority 1000                                                                                                                                                                                               
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeMobilityGroupDefinition=QCI6                                                                                                                                            
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
ueMobilityGroupId 6                                                                                                                                                                                                
ueMobilityGroupPriority 65534                                                                                                                                                                                      
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeMobilityGroupDefinition=QCI7                                                                                                                                            
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
ueMobilityGroupId 7                                                                                                                                                                                                
ueMobilityGroupPriority 1000                                                                                                                                                                                       
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeServiceGroupDefinition=QCI6                                                                                                                                             
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==6                                                                                                                                                                                           
ueServiceGroupId 6                                                                                                                                                                                                 
ueServiceGroupPriority 65534                                                                                                                                                                                       
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                
                                                                                                                                                                                                                   
crn GNBCUCPFunction=1,UeGroupSelection=1,UeServiceGroupDefinition=QCI7                                                                                                                                             
chipsetRef                                                                                                                                                                                                         
imeiSvRef                                                                                                                                                                                                          
selectionCriteria qci==7                                                                                                                                                                                           
ueServiceGroupId 7                                                                                                                                                                                                 
ueServiceGroupPriority 1000                                                                                                                                                                                        
userLabel                                                                                                                                                                                                          
end                                                                                                                                                                                                                

{DEL_Vi_GNBCUCPFunction}

crn GNBCUCPFunction=1,EUtraNetwork=1
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1511
arfcnValueEUtranDl 1511
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=1526
arfcnValueEUtranDl 1526
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=240
arfcnValueEUtranDl 240
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=265
arfcnValueEUtranDl 265
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=3663
arfcnValueEUtranDl 3663
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39150
arfcnValueEUtranDl 39150
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39294
arfcnValueEUtranDl 39294
userLabel
end
crn GNBCUCPFunction=1,EUtraNetwork=1,EUtranFrequency=39348
arfcnValueEUtranDl 39348
userLabel
end

{DEL_Vi_GNBDUFunction}

"""

DEL_Vi_Termpoint_GUtranFreqRelation_script = """


###########################Termpoint & FreqRelation################################



cvms bfranchor

#####1. Transport=1,Router=LTEUP,InterfaceIPv6=NR--Change TN Port as per configured in BBU

get Router=LTEUP,InterfaceIPv4=TN_._UP                      encapsulation  > $encapsulation

$reqipX2 = readinput( ipv6 IP for X2 ENDC )
$reqhopadd = readinput( ipv6 nexthop )

get Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR usedAddress > $reqipNR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
get GNBDUFunction=1 gNBId$ > $gnbid


gs+

crn Transport=1,Router=LTEUP,InterfaceIPv6=NR
aclEgress
aclIngress
bfdProfile
bfdStaticRoutes 0
dscpNdp 48
egressQosMarking
encapsulation $encapsulation
ingressQosMarking
loopback false
mtu 1500
neighborDiscoveryTimeout 30000
neighborSolicitationInterval 1000
routesHoldDownTimer
trackedInterface
userLabel
end


#####2. Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2/NR ---- Change IP address as per planning


crn Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
address $reqipX2 ###need to change ENDC IP according to plan in AD column###
configurationMode 0
duidType 0
primaryAddress true
userLabel
end	
gs-

#######3. Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1/NR--Change Nexthop address as per planning

gs+

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1                                                                                                               
end

crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default                                                                                                   
dst ::/0                                                                                                                                                          
end


crn Transport=1,Router=LTEUP,RouteTableIPv6Static=1,Dst=default,NextHop=1
address $reqhopadd ###need to change ENDC gateway according to plan in AA column###
adminDistance 1
bfdMonitoring true
discard false
reference
end
gs-

#########4. Transport=1,SctpEndpoint=X2_ENDC/NR 


gs+

crn Transport=1,SctpEndpoint=X2_ENDC
dtls
dtlsNodeCredential
dtlsSctpSecurityMode 0
dtlsTrustCategory
localIpAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
portNumber 36422
sctpProfile SctpProfile=1
userLabel
end

set ENodeBFunction=1$  endcAllowed  true                                                                                                                 
set ENodeBFunction=1$  sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                        
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                     
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                  
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=10,mnclength=2                                                                                                

crn ENodeBFunction=1,EndcProfile=1                                                                                                                                
end

set ENodeBFunction=1,EndcProfile=1 meNbS1TermReqArpLev 0                                                                                                          
set ENodeBFunction=1,EndcProfile=1 splitNotAllowedUeArpLev 0 
lset ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci[6789]$ endcProfileRef ENodeBFunction=1,EndcProfile=1

cr ENodeBFunction=1,UePolicyOptimization=1                                                                                                                        
set ENodeBFunction=1,UePolicyOptimization=1 ueCapPrioList 0                                                                                                       
set ENodeBFunction=1,UePolicyOptimization=1 coverageAwareImc true                                                                                                 
set ENodeBFunction=1  endcX2IpAddrViaS1Active  true
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR= gNodebIdLength 26                                                                                               
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1 anrStateNR 1 



################*Parameter Setting Required:

set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1  anrStateNR        1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1  anrFunctionNRId   1
set ENodeBFunction=1$   endcAllowed       true
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2

set  CXC4012095   featureState 1
set  CXC4012504   featurestate 1
set  CXC4012381   featurestate 1
set  CXC4012385   featurestate 1 
set  CXC4040006   featurestate 1                                                                                                                                   

set EUtranCellFDD=DL_.*,EUtranFreqRelation=240 endcHoFreqPriority 6
set EUtranCellFDD=DL_.*,EUtranFreqRelation=1511 endcHoFreqPriority 7
set EUtranCellFDD=DL_.*,EUtranFreqRelation=3663 endcAwareIdleModePriority 3
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39150 endcAwareIdleModePriority 5
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39151 endcAwareIdleModePriority 7
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39348 endcAwareIdleModePriority 5
set EUtranCellTDD=DL_.*,EUtranFreqRelation=39349 endcAwareIdleModePriority 7             

get Router=*.*,RouteTableIPv6Static=.*,Dst=default,NextHop= address > $gwip                                                                                          
mcc Router=*.*,InterfaceIPv6=NR,AddressIPv6=X2 ping6 $gwip -c 4



#############################################5. ENodeBFunction=1,GUtraNetwork=1###########################################

gs+

cr ENodeBFunction=1,GUtraNetwork=1


#############################################6. ENodeBFunction=1,GUtraNetwork=1###########################################

gs+                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
dirDataPathAvail true                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
eNBVlanPortRef                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
gNodeBId $gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
gNodeBIdLength 26                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
gNodeBPlmnId mcc=404,mnc=10,mncLength=2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
userLabel                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
end   

crn ENodeBFunction=1,GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid,TermPointToGNB=40410-$gnbid                                                                                                                                                                                                                                                                                                                                                                                                                                                                          
additionalCnRef                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
administrativeState 1                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
domainName                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ipAddress 0.0.0.0                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
ipAddress2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       
ipsecEpAddress ::                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
ipv6Address $reqipNR                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
ipv6Address2                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
upIpAddress ::                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
end    

########################7. ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=######################################

crn ENodeBFunction=1,GUtraNetwork=1,GUtranSyncSignalFrequency=629952-30
arfcn 629952
smtcScs 30
userLabel
end
gs-



lt all


get GNBDUFunction=1,NRCellDU= celllocalid > $CLID

mr CWA_CRP_2
ma CWA_CRP_2 EUtranCell.DD=.*,EUtranFreqRelation= cellReselectionPriority 2
lpr CWA_CRP_2

set CWA_CRP_2 cellReselectionPriority 4


ma L21_12_21 ^EUtranCell.DD                                                                                                                                       

for $mo in L21_12_21                                                                                                                                              
$mordn = rdn($mo)                                                                                                                                                 
pr ENodeBFunction=1,$mordn,GUtranFreqRelation=629952                                                                                                              
if $nr_of_mos = 0                                                                                                                                                 
cr ENodeBFunction=1,$mordn,GUtranFreqRelation=629952                                                                                                              
GUtraNetwork=1,GUtranSyncSignalFrequency=629952-30                                                                                                       
fi                                                                                                                                                                
done                                                                                                                                                              


func Relation_121L21                                                                                                                                              
for $j = 1 to 5                                                                                                                                                   
pr GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid,ExternalGUtranCell=40410-000000$gnbid-31$j                                                                  
if $nr_of_mos = 1                                                                                                                                                 
crn ENodeBFunction=1,$mordn,GUtranFreqRelation=629952,GUtranCellRelation=40410-000000$gnbid-31$j                                                                  
essEnabled false                                                                                                                                                  
isRemoveAllowed false                                                                                                                                             
neighborCellRef GUtraNetwork=1,ExternalGNodeBFunction=40410-$gnbid,ExternalGUtranCell=40410-000000$gnbid-31$j                                                     
userLabel                                                                                                                                                         
end                                                                                                                                                               
fi                                                                                                                                                                
done                                                                                                                                                              
endfunc                                                                                                                                                           



func Relation_121L2_18L                                                                                                                                           
for $mo in L21_12_21                                                                                                                                              
$mordn = rdn($mo)                                                                                                                                                 
Relation_121L21                                                                                                                                                   
done                                                                                                                                                              
endfunc                                                                                                                                                           

Relation_121L2_18L        


set EUtranCell.DD=.*,GUtranFreqRelation=629952 cellReselectionPriority 5
set CWA_CRP_2 cellReselectionPriority 2

set ENodeBFunction=1$  endcAllowed  true                                                                                                                 
set ENodeBFunction=1$  sctpEndcX2Ref Transport=1,SctpEndpoint=X2_ENDC                                                                                        
set ENodeBFunction=1$  upEndcX2IpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                     
set ENodeBFunction=1$  intraRanIpAddressRef Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=X2                                                                  
set ^EUtranCell.DD= endcAllowedPlmnList mcc=404,mnc=10,mnclength=2                                                                                                

"""


DEL_Vi_NR_GPL_LMS_SCRIPT = """


confb+

crn NodeSupport=1,ServiceDiscovery=1
localAddress Transport=1,Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
nodeCredential
primaryGsds host=localhost,hostIPs=,port=8301,serviceArea=NR_NSA
secondaryGsds
trustCategory SecM=1,CertM=1,TrustCategory=1
end

crn NodeSupport=1,ServiceDiscovery=1
localAddress Transport=1,Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
nodeCredential
primaryGsds host=localhost,hostIPs=,port=8301,serviceArea=NR_NSA
secondaryGsds
trustCategory SecM=1,CertM=1,TrustCategory=1
end

set NodeSupport=1,ServiceDiscovery=1 trustCategory SecM=1,CertM=1,TrustCategory=1


bl nrcell


get nrcelldu ssbFrequency$
set NRCellDU=.* ssbFrequency 629952







lt all
rbs
rbs

confb+

$date = `date +%y%m%d_%H%M`

lbl NRCellDU=.*
lbl NRSectorCarrier=

set CXC4012500 FeatureState 1
set CXC4012273 featurestate 1
set CXC4012375 featurestate 1
set CXC4012549 featurestate 1
set CXC4012492 featurestate 1
set CXC4012534 featurestate 1
set CXC4012347 featurestate 1
set CXC4012325 featurestate 1
set CXC4012493 featurestate 1
set CXC4012558 featurestate 1
set CXC4012272 featurestate 1
set CXC4012502 featurestate 1
set CXC4012347 featurestate 1
set CXC4012510 FeatureState 1
set CXC4012587 FeatureState 1
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
set CXC4010949 featureState 1
set CXC4010956 featureState 1
set CXC4010959 featureState 1
set CXC4010961 featureState 1
set CXC4010962 featureState 1
set CXC4010963 featureState 1
set CXC4010964 featureState 1
set CXC4010967 featureState 1
set CXC4010973 featureState 1
set CXC4010974 featureState 1
set CXC4010980 featureState 1
set CXC4010990 featureState 1
set CXC4011011 featureState 1
set CXC4011018 featureState 1
set CXC4011033 featureState 1
set CXC4011034 featureState 1
set CXC4011050 featureState 1
set CXC4011056 featureState 1
set CXC4011057 featureState 1
set CXC4011059 featureState 1
set CXC4011060 featureState 1
set CXC4011061 featureState 1
set CXC4011062 featureState 1
set CXC4011063 featureState 1
set CXC4011064 featureState 1
set CXC4011067 featureState 1
set CXC4011068 featureState 1
set CXC4011069 featureState 1
set CXC4011072 featureState 1
set CXC4011074 featureState 1
set CXC4011075 featureState 1
set CXC4011155 featureState 1
set CXC4011157 featureState 1
set CXC4011163 featureState 1
set CXC4011183 featureState 1
set CXC4011245 featureState 1
set CXC4011247 featureState 1
set CXC4011251 featureState 1
set CXC4011252 featureState 1
set CXC4011253 featureState 1
set CXC4011255 featureState 1
set CXC4011256 featureState 1
set CXC4011258 featureState 1
set CXC4011317 featureState 1
set CXC4011319 featureState 1
set CXC4011327 featureState 1
set CXC4011345 featureState 1
set CXC4011346 featureState 1
set CXC4011356 featureState 1
set CXC4011366 featureState 1
set CXC4011370 featureState 1
set CXC4011372 featureState 1
set CXC4011373 featureState 1
set CXC4011376 featureState 1
set CXC4011378 featureState 1
set CXC4011422 featureState 1
set CXC4011427 featureState 1
set CXC4011443 featureState 1
set CXC4011444 featureState 1
set CXC4011476 featureState 1
set CXC4011477 featureState 1
set CXC4011479 featureState 1
set CXC4011481 featureState 1
set CXC4011482 featureState 1
set CXC4011485 featureState 1
set CXC4011515 featureState 1
set CXC4011557 featureState 1
set CXC4011559 featureState 1
set CXC4011618 featureState 1
set CXC4011666 featureState 1
set CXC4011667 featureState 1
set CXC4011698 featureState 1
set CXC4011699 featureState 1
set CXC4011710 featureState 1
set CXC4011711 featureState 1
set CXC4011715 featureState 1
set CXC4011716 featureState 1
set CXC4011804 featureState 1
set CXC4011807 featureState 1
set CXC4011808 featureState 1
set CXC4011811 featureState 1
set CXC4011813 featureState 1
set CXC4011814 featureState 1
set CXC4011815 featureState 1
set CXC4011820 featureState 1
set CXC4011823 featureState 1
set CXC4011910 featureState 1
set CXC4011914 featureState 1
set CXC4011917 featureState 1
set CXC4011918 featureState 1
set CXC4011922 featureState 1
set CXC4011930 featureState 1
set CXC4011933 featureState 1
set CXC4011937 featureState 1
set CXC4011938 featureState 1
set CXC4011939 featureState 1
set CXC4011940 featureState 1
set CXC4011941 featureState 1
set CXC4011942 featureState 1
set CXC4011946 featureState 1
set CXC4011951 featureState 1
set CXC4011958 featureState 1
set CXC4011967 featureState 1
set CXC4011969 featureState 1
set CXC4011973 featureState 1
set CXC4011974 featureState 1
set CXC4011975 featureState 1
set CXC4011982 featureState 1
set CXC4011983 featureState 1
set CXC4011991 featureState 1
set CXC4012003 featureState 1
set CXC4012015 featureState 1
set CXC4012018 featureState 1
set CXC4012022 featureState 1
set CXC4012036 featureState 1
set CXC4012070 featureState 1
set CXC4012089 featureState 1
set CXC4012097 featureState 1
set CXC4012111 featureState 1
set CXC4012123 featureState 1
set CXC4012129 featureState 1
set CXC4012199 featureState 1
set CXC4012218 featureState 1
set CXC4012238 featureState 1
set CXC4012240 featureState 1
set CXC4012256 featureState 1
set CXC4012259 featureState 1
set CXC4012260 featureState 1
set CXC4012261 featureState 1
set CXC4012271 featureState 1
set CXC4012272 featureState 1
set CXC4012273 featureState 1
set CXC4012316 featureState 1
set CXC4012324 featureState 1
set CXC4012325 featureState 1
set CXC4012326 featureState 1
set CXC4012347 featureState 1
set CXC4012349 featureState 1
set CXC4012356 featureState 1
set CXC4012371 featureState 1
set CXC4012374 featureState 1
set CXC4012375 featureState 1
set CXC4012381 featureState 1
set CXC4012385 featureState 1
set CXC4012480 featureState 0
set CXC4012485 featureState 1
set CXC4012492 featureState 1
set CXC4012493 featureState 1
set CXC4012500 featureState 1
set CXC4012502 featureState 1
set CXC4012503 featureState 1
set CXC4012504 featureState 1
set CXC4012505 featureState 1
set CXC4012510 featureState 1
set CXC4012534 featureState 1
set CXC4012549 featureState 1
set CXC4012558 featureState 1
set CXC4012578 featureState 1
set CXC4012587 featureState 1
set CXC4040004 featureState 1
set CXC4040005 featureState 1
set CXC4040006 featureState 1
set CXC4040008 featureState 1
set CXC4040009 featureState 1
set CXC4040010 featureState 1
set CXC4040014 featureState 1
set CXC4012590 FeatureState 1
set CXC4012562 FeatureState 1
set CXC4012330 FeatureState 1
set CXC4012373 FeatureState 1
set CXC4012406 FeatureState 1
set CXC4012589 FeatureState 1
set CXC4012547 FeatureState 0


///common_Parameters_32t_8t
set NRSectorCarrier=.*,CommonBeamforming=1               cbfMacroTaperType 0
set CUUP5qi=6$  estimatedE2ERTT 50
set CUUP5qi=8$  estimatedE2ERTT 50
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1  tPollRetransmitUl 80
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 tStatusProhibitUl 10
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxInactivityTimer 15
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxLongCycle      10
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base  drxOnDurationTimer  39
set GNBCUUPFunction=1          dcDlPdcpInitialScgRate 100

set NRCellDU=.* tddSpecialSlotPattern 3
set NRCellDU=.* tddUlDlPattern 1
set NRCellDU=.* rachPreambleFormat 0
set NRCellDU=.* cellRange 5000
set NRCellDU=.* csiRsShiftingPrimary 1
set NRCellDU=.* csiRsShiftingSecondary 1
set NRCellDU=.* dl256QamEnabled true
set NRCellDU=.* drxProfileEnabled true
set NRCellDU=.* maxUeSpeed 2
set NRCellDU=.* pdschStartPrbStrategy 3
set NRCellDU=.* puschStartPrbStrategy 3
set NRCellDU=.* pZeroNomPucch -114
set NRCellDU=.* secondaryCellOnly False
set NRCellDU=.* ssbDuration 1
set NRCellDU=.* ssbOffset 0
set NRCellDU=.* ssbPeriodicity 20
set NRCellDU=.* ssbSubCarrierSpacing 30
set NRCellDU=.* subCarrierSpacing 30
set NRCellDU=.* trsPeriodicity 20
set NRCellDU=.* trsPowerBoosting 0
set NRCellDU=.* ul256QamEnabled true
set NRCellDU=.* rachPreambleRecTargetPower -110
set NRCellDU=.* rachPreambleTransMax 10
Set NRCellDU=.* maxUsersRachSchedPusch 100
set NRCellDU=.* pZeroNomPuschGrant -102
set NRCellDU=.* csiRsPeriodicity 40
set NRCellDU=.* additionalPucchForCaEnabled FALSE
set NRSectorCarrier=.* configuredMaxTxPower    200000
set NRCellDU=.*  maxNoOfAdvancedDlMuMimoLayers 8

#lkf required with dmrs feature for bm
set NRCellDU=.* pdschAllowedInDmrsSym TRUE
set NRCellDU=.* puschAllowedInDmrsSym TRUE

set QciProfileEndcConfigExt=1   initialUplinkConf 1
set GNBCUCPFunction=1,UeCC=1,InactivityProfile=Default,InactivityProfileUeCfg=Base tInactivityTimerEndcSn 5
set NRSectorCarrier= nRMicroSleepTxEnabled true
set NRSectorCarrier=.*,CommonBeamforming=1  coverageShape 1
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1    tPollRetransmitDl 80
set AnrFunctionNR anrCgiMeasInterFreqMode 1
set AnrFunctionNR anrCgiMeasIntraFreqEnabled TRUE
set AnrFunctionNR anrEndcX2Enabled TRUE
set AnrFunction removeGnbTime 7
set AnrFunction removeNrelTime 7
set GNBDUFunction=1,Rrc=1 n310 20
set GNBDUFunction=1,Rrc=1 n311 1
set GNBDUFunction=1,Rrc=1 t300 1500
set GNBDUFunction=1,Rrc=1 t301 600
set GNBDUFunction=1,Rrc=1 t304 2000
set GNBDUFunction=1,Rrc=1 t310 2000
set GNBDUFunction=1,Rrc=1 t311 3000
set GNBDUFunction=1,Rrc=1 t319 400

set GNBCUUPFunction=1    endcDataUsageReportEnabled true
set GNBDUFunction=1,UeCC=1,Prescheduling=1,PreschedulingUeCfg=Base preschedulingUeMode 1
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1

set NRCellDU=.* csiRsConfig4P csiRsControl4Ports=0,i11Restriction=
set NRCellDU=.* csiRsConfig8P  csiRsControl8Ports=1,i11Restriction=FFFF,i12Restriction=
set NRCellDU=.* csiRsConfig32P csiRsControl32Ports=EIGHT_TWO_N1AZ,i11Restriction=FFFFFFFF,i12Restriction=FF
set NRCellDU=.* ssbPowerBoost 6
set NRCellDU=.* advancedDlSuMimoEnabled TRUE
set NRCellDU=.* pZeroNomSrs -110
set NRCellDU=.* srsPeriodicity 40
set NRCellDU=.* dlMaxMuMimoLayers 8
set NRCellDU=.* ulMaxMuMimoLayers 4
set NRCellDU=.* pZeroUePuschOffset256Qam 4
set .  cbfMacroTaperType 0
set GNBCUCPFunction=1,AnrFunction=1,AnrFunctionNR=1         anrAutoCreateXnForEndc True

set . endcDlNrRetProhibTimer 400
set . endcDlNrQualHyst 3
set . initialUplinkConf SCG
set . endcUlNrRetProhibTimer 1000
set . dcDlAggActTime 1
set . dcDlAggExpiryTimer 100
set . ulDataSplitThreshold

set NRCellRelation= isHoAllowed true
set NRCellDU=.* endcDlLegSwitchEnabled true
set NRCellDU=.* endcDlNrLowQualThresh 0
set NRCellDU=.* endcUlLegSwitchEnabled true
set NRCellDU=.* endcUlNrLowQualThresh 10
set NRCellDU=.* endcUlNrQualHyst 6
set NRCellCU=.* mcpcPSCellEnabled true

cr GNBCUCPFunction=1,IntraFreqMC=1
cr GNBCUCPFunction=1,IntraFreqMC=1,IntraFreqMCCellProfile=1

set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base betterSpCellTriggerQuantity 0
set IntraFreqMC=1,IntraFreqMCCellProfile=1,IntraFreqMCCellProfileUeCfg=Base rsrpBetterSpCell hysteresis=10,offset=30,timeToTrigger=640


set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpSCellCoverage hysteresis=10,threshold=-117
set IntraFreqMC=1,IntraFreqMCCellProfile=1 rsrpBetterSCell offset=30,hysteresis=10
set Mcpc=1,McpcPSCellProfile=.*,McpcPSCellProfileUeCfg=Base  rsrpCriticalEnabled true
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpSearchZone threshold=-112,hysteresis=10,timeToTriggerA1=160
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCandidateA5 threshold1=-118,threshold2=-112,hysteresis=10,timeToTrigger=640
set Mcpc=1,McpcPSCellNrFreqRelProfile=Default,McpcPSCellNrFreqRelProfileUeCfg=Base rsrpCandidateA5Offsets threshold1Offset=0,threshold2Offset=0
set Mcpc=1,McpcPSCellProfile=Default,McpcPSCellProfileUeCfg=Base rsrpCritical threshold=-110,timeToTrigger=256,hysteresis=20
set QciProfileEndcConfigExt=1  ulDataSplitThresholdMcg -1

set ENodeBFunction=1 dlBbCapacityTarget 300

wait 5

set NRCellDU=.* drxProfileRef GNBDUFunction=1,UeCC=1,DrxProfile=Default
set . mcpcPSCellProfileRef GNBCUCPFunction=1,Mcpc=1,McpcPSCellProfile=Default

##################################3

cvms pre_Twamp_NR

set SystemFunctions=1,Lm=1,FeatureState=CXC4040009 featureState 1
gs+

crn Transport=1,Router=NR,TwampResponder=NR
ipAddress Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
userLabel
end

###################

set NRCellDU=.*  maxNoOfAdvancedDlMuMimoLayers 8
set PmEventService=1     cellTraceFileSize 30000

###########################

gs+
crn Transport=1,Synchronization=1,TimeSyncIO=1,GnssInfo=1
end
gs-

########  QOS ####################

cvms Pre_QOS_NR_$date
set ENodeBFunction=1 dscpLabel 46
set ENodeBFunction=1 gtpuErrorIndicationDscp 46
set ENodeBFunction=1 interEnbCaTunnelDscp 26
set ENodeBFunction=1 interEnbUlCompTunnelDscp 26
set ENodeBFunction=1 s1GtpuEchoDscp 46
set ENodeBFunction=1 x2GtpuEchoDscp 46

cr Transport=1,QosProfiles=1,DscpPcpMap=1
set QciTable=default,QciProfilePredefined=qci1$ dscp 34
set QciTable=default,QciProfilePredefined=qci2$ dscp 34
set QciTable=default,QciProfilePredefined=qci3$ dscp 26
set QciTable=default,QciProfilePredefined=qci4$ dscp 26
set QciTable=default,QciProfilePredefined=qci5$ dscp 46
set QciTable=default,QciProfilePredefined=qci6$ dscp 32
set QciTable=default,QciProfilePredefined=qci7$ dscp 40
set QciTable=default,QciProfilePredefined=qci8$ dscp 30
set QciTable=default,QciProfilePredefined=qci9$ dscp 26
set SysM=1,OamTrafficClass=1 dscp 28
set SctpProfile= dscp 46
set Ntp=1,NtpFrequencySync= dscp 46

set QosProfiles=1,DscpPcpMap=1 pcp0
set QosProfiles=1,DscpPcpMap=1 pcp1
set QosProfiles=1,DscpPcpMap=1 pcp2
set QosProfiles=1,DscpPcpMap=1 pcp3
set QosProfiles=1,DscpPcpMap=1 pcp4
set QosProfiles=1,DscpPcpMap=1 pcp5
set QosProfiles=1,DscpPcpMap=1 pcp6
set QosProfiles=1,DscpPcpMap=1 pcp7

lset Transport=1,QosProfiles=1,DscpPcpMap=1 pcp0 0,1,2,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,36,37,38,39,41,43,45,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp2 22,24,26
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp3 6,8,10,30,32
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp4 12,14,40
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp5 4,28
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp6 16,18,34,42,44
set Transport=1,QosProfiles=1,DscpPcpMap=1 pcp7 20,46
set SctpProfile=Node_Internal_F1  dscp 46
set SctpProfile=1 dscp 46
set Router=.*,DnsClient=1 dscp 28

set . egressQosMarking QosProfiles=1,DscpPcpMap=1

######### Del Data_3 ######

rdel Equipment=1,FieldReplaceableUnit=AAS-S.*_N1,RiPort=DATA_3
y

################  Digital tilt for 3219 A #############

get NRSectorCarrier=S1_N11,CommonBeamforming=1  ^digitalTilt > $1st-sec-tilt
get NRSectorCarrier=S2_N11,CommonBeamforming=1  ^digitalTilt > $2nd-sec-tilt
get NRSectorCarrier=S3_N11,CommonBeamforming=1  ^digitalTilt > $3rd-sec-tilt

hget field prod@name 3219
for $mo in hget_group
$mordn = rdn($mo)
cr Equipment=1,$mordn,AntennaNearUnit=1
cr Equipment=1,$mordn,AntennaNearUnit=1,RetSubUnit=1
set Equipment=1,$mordn,Transceiver=1 retSubUnitRef $mordn,AntennaNearUnit=1,RetSubUnit=1
set FieldReplaceableUnit=AAS-S1_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $1st-sec-tilt
set FieldReplaceableUnit=AAS-S2_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $2nd-sec-tilt
set FieldReplaceableUnit=AAS-S3_N1,AntennaNearUnit=1,RetSubUnit=1 electricalAntennaTilt $3rd-sec-tilt
done

wait 3
lt all

accn hget_group restartunit 1 0 0

######################   SCTP profile for 5G    ########################

confd+
set Transport=1,SctpProfile=Node_Internal_F1 alphaIndex 3
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=Node_Internal_F1 betaIndex 2
set Transport=1,SctpProfile=Node_Internal_F1 bundlingActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 bundlingTimer 0
set Transport=1,SctpProfile=Node_Internal_F1 cookieLife 60
set Transport=1,SctpProfile=Node_Internal_F1 dscp 46
set Transport=1,SctpProfile=Node_Internal_F1 hbMaxBurst 1
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatActivated TRUE
set Transport=1,SctpProfile=Node_Internal_F1 heartbeatInterval 2000
set Transport=1,SctpProfile=Node_Internal_F1 incCookieLife 30
set Transport=1,SctpProfile=Node_Internal_F1 initARWnd 16384
set Transport=1,SctpProfile=Node_Internal_F1 maxRto 4000
set Transport=1,SctpProfile=Node_Internal_F1 initRto 2000
set Transport=1,SctpProfile=Node_Internal_F1 minRto 1000
set Transport=1,SctpProfile=Node_Internal_F1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=Node_Internal_F1 maxActivateThr 65535
set Transport=1,SctpProfile=Node_Internal_F1 maxBurst 4
set Transport=1,SctpProfile=Node_Internal_F1 maxInStreams 2
set Transport=1,SctpProfile=Node_Internal_F1 maxInitRt 5
set Transport=1,SctpProfile=Node_Internal_F1 maxOutStreams 2
set Transport=1,SctpProfile=Node_Internal_F1 maxSctpPduSize 1480
set Transport=1,SctpProfile=Node_Internal_F1 maxShutdownRt 5
set Transport=1,SctpProfile=Node_Internal_F1 minActivateThr 1
set Transport=1,SctpProfile=Node_Internal_F1 noSwitchback TRUE
set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=Node_Internal_F1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=Node_Internal_F1 sackTimer 100
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBuffer 48
set Transport=1,SctpProfile=Node_Internal_F1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=Node_Internal_F1 transmitBufferSize 64
set Transport=1,SctpProfile=Node_Internal_F1 userLabel SCTP
set Transport=1,SctpProfile=1 alphaIndex 3
set Transport=1,SctpProfile=1 assocMaxRtx 8
set Transport=1,SctpProfile=1 betaIndex 2
set Transport=1,SctpProfile=1 bundlingActivated TRUE
set Transport=1,SctpProfile=1 bundlingAdaptiveActivated TRUE
set Transport=1,SctpProfile=1 bundlingTimer 0
set Transport=1,SctpProfile=1 cookieLife 60
set Transport=1,SctpProfile=1 dscp 46
set Transport=1,SctpProfile=1 hbMaxBurst 1
set Transport=1,SctpProfile=1 heartbeatActivated TRUE
set Transport=1,SctpProfile=1 heartbeatInterval 2000
set Transport=1,SctpProfile=1 incCookieLife 30
set Transport=1,SctpProfile=1 initARWnd 16384
set Transport=1,SctpProfile=1 maxRto 4000
set Transport=1,SctpProfile=1 initRto 2000
set Transport=1,SctpProfile=1 minRto 1000
set Transport=1,SctpProfile=1 initialHeartbeatInterval 500
set Transport=1,SctpProfile=1 maxActivateThr 65535
set Transport=1,SctpProfile=1 maxBurst 4
set Transport=1,SctpProfile=1 maxInStreams 2
set Transport=1,SctpProfile=1 maxInitRt 5
set Transport=1,SctpProfile=1 maxOutStreams 2
set Transport=1,SctpProfile=1 maxSctpPduSize 1480
set Transport=1,SctpProfile=1 maxShutdownRt 5
set Transport=1,SctpProfile=1 minActivateThr 1
set Transport=1,SctpProfile=1 noSwitchback TRUE
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=1 primaryPathAvoidance TRUE
set Transport=1,SctpProfile=1 primaryPathMaxRtx 0
set Transport=1,SctpProfile=1 sackTimer 100
set Transport=1,SctpProfile=1 thrTransmitBuffer 48
set Transport=1,SctpProfile=1 thrTransmitBufferCongCeased 85
set Transport=1,SctpProfile=1 transmitBufferSize 64
set Transport=1,SctpProfile=1 userLabel SCTP

############# 5G GTP ##################################

set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoEnabled true
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoEnabled true

set GtpuSupervision=1,GtpuSupervisionProfile=S1 gtpuEchoDscp 32
set GtpuSupervision=1,GtpuSupervisionProfile=X2 gtpuEchoDscp 32

set Transport=1,SctpProfile=Node_Internal_F1 pathMaxRtx 4
set Transport=1,SctpProfile=1 pathMaxRtx 4
set Transport=1,SctpProfile=Node_Internal_F1 assocMaxRtx 8
set Transport=1,SctpProfile=1 assocMaxRtx 8

######### PDCCH Beamforming

set CXC4012589 featurestate 1
set NRCellDU pdcchLaSinrOffset -20

set EUtranCell.DD=.*,EUtranFreqRelation=.* anrMeasOn true
set GNBDUFunction=1,UeCC=1,DrxProfile=Default,DrxProfileUeCfg=Base drxEnabled        true

##### System Constant

scw RP136:20
scw RP137:20
scw RP138:20
scw RP139:20

#### Pmax #####

set NRCellDU pMax 26

##### DLMAX RETX #####

set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 dlMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,DataRadioBearer=1 ulMaxRetxThreshold 32
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 ulMaxRetxThreshold 32
set Mcfb=1,McfbCellProfile=1,McfbCellProfileUeCfg=Base      epsFallbackOperation 2

#### DFTS OFDM #####

set CXC4012373 featurestate 1
set NRCellDU dftSOfdmMsg3Enabled TRUE
set NRCellDU dftSOfdmPuschEnabled TRUE

##### endcActionEvalFail #####

set IntraFreqMCCellProfileUeCfg endcActionEvalFail 1

############# 2nd script from mail ##################

### advanced DL SUMIMO ###

set CXC4012510 featurestate 1
set NRCellDU advancedDlSuMimoEnabled TRUE
set NRCellDU nrSrsDlBufferVolThr 100
set NRCellDU nrSrsDlPacketAgeThr 0
set NRCellDU pZeroNomSrs -110
set NRCellDU srsPeriodicity 40
set NRCellDU srsHoppingBandwidth 0

###  tDcOverall ###

set GNBCUCPFunction tDcOverall 11

###  uldatasplitthreshold ###

set QciProfileEndcConfigExt uldatasplitthresholdmcg -1

set QciProfileEndcConfigExt uldatasplitthreshold 102400

#################################

set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitDl 80
set GNBDUFunction=1,RadioBearerTable=1,SignalingRadioBearer=1 tPollRetransmitUl 80

###################################

ldeb  NRSectorCarrier=
ldeb  NRCellDU=.*

#####################################

#######################################

$date = `date +%y%m%d_%H%M`
confb-


lt all
rbs
rbs

$date = `date +%y%m%d_%H%M`
confb+

get . additionalUpperLayerIndList
get . primaryUpperLayerInd

set CXC4012371 featurestate 1
set CXC4012381 featurestate 1
set CXC4012504 featurestate 1
set CXC4012218 featurestate 1
set CXC4011559 featurestate 1
set CXC4012324 featurestate 1
set CXC4012385 featurestate 1
set CXC4012503 featurestate 1
set CXC4011967 featurestate 1
set CXC4011251 featurestate 1
set CXC4011163 featurestate 1
set CXC4011063 featurestate 1
set CXC4011345 featurestate 1
set CXC4011815 featurestate 1
set CXC4011477 featurestate 1
set CXC4012480 featurestate 0
set CXC4010620 featurestate 1
set CXC4012578 featurestate 1
set CXC4012015 featurestate 1
set CXC4012095 featurestate 1


set ENodeBFunction=1,EUtranCell.*DD= endcSetupDlPktVolThr 5
set EUtranCell.*DD=.*,UeMeasControl=1,ReportConfigA5EndcHo=1 hysteresisA5 10
set UePolicyOptimization=1  endcAwareImc 2

set CarrierAggregationFunction=1 dcSCellActDeactDataThres 30
set CarrierAggregationFunction=1 dcSCellActDeactDataThresHyst 30
set CarrierAggregationFunction=1 dcSCellDeactDelayTimer 200
set CarrierAggregationFunction=1 endcCaPolicy 1
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasRestartTime 10000
set EUtranCell.DD=.*  measGapPattEndc 1
set ENodeBFunction=1   endcS1OverlapMode True
set EUtranCell.DD=.*,UeMeasControl=1 endcMeasTime 2000
set EUtranCell.DD=.*,UeMeasControl=1 endcB1MeasWindow 40
set EUtranCell.DD=.*,UeMeasControl=1 maxMeasB1Endc 3
set ENodeBFunction=1       endcDataUsageReportEnabled true
set ENodeBFunction=1       zzzTemporary81    1
crn ENodeBFunction=1,EndcProfile=2
meNbS1TermReqArpLev 15
splitNotAllowedUeArpLev 0
userLabel
end

set  ENodeBFunction=1,EndcProfile=2  meNbS1TermReqArpLev  15
set  ENodeBFunction=1,EndcProfile=2 splitNotAllowedUeArpLev 0
set QciTable=default,QciProfilePredefined=qci5              endcProfileRef    EndcProfile=2
set QciTable=default,QciProfilePredefined=qci1              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3
set QciTable=default,QciProfilePredefined=qci2              endcProfileRef    ENodeBFunction=1,EndcProfilePredefined=3



ma cellockqqwer  ^eutrancell administrativeState 0
lbl  cell
ldeb cell
lbl cellockqqwer

#set EUtranCell.DD=.*  primaryUpperLayerInd 0
#set EUtranCell.DD=.*  additionalUpperLayerIndList 0 0 0 0 0
set ^EUtranCell.DD=.* endcAllowedPlmnList mcc=404,mnc=49,mnclength=2
set . anrstateNR 1
set ENodeBFunction=1,AnrFunction=1,AnrFunctionNR=1          gNodebIdLength 26
set . endcX2IpAddrViaS1Active 1

set EUtranFreqRelation=39150    endcHoFreqPriority -1
set EUtranFreqRelation=39294    endcHoFreqPriority -1
set EUtranFreqRelation=39151    endcHoFreqPriority -1
set EUtranFreqRelation=39295    endcHoFreqPriority -1
set EUtranFreqRelation=1415     endcHoFreqPriority 7
set EUtranFreqRelation=3690    endcHoFreqPriority 6

set EUtranFreqRelation=39150    endcAwareIdleModePriority 5
set EUtranFreqRelation=39294    endcAwareIdleModePriority 5
set EUtranFreqRelation=39151    endcAwareIdleModePriority 7
set EUtranFreqRelation=39295    endcAwareIdleModePriority 7
set EUtranFreqRelation=1415     endcAwareIdleModePriority 6
set EUtranFreqRelation=3690    endcAwareIdleModePriority 4

##need to add small cell arfcn

cr ENodeBFunction=1,UePolicyOptimization=1
set UePolicyOptimization=1      t320              180
set GUtranFreqRelation=    endcB1MeasPriority 7
set ENodeBFunction=1       endcAllowed       true
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= triggerQuantityA5 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= reportQuantityA5  0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= timeToTriggerA5  100
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrp -44
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold1Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrp -113
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= a5Threshold2Rsrq -195
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA5EndcHo= hysteresisA5 10

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 triggerQuantityB1 0
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrp -105
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 b1ThresholdRsrq -435

set EUtranCell.DD=.*,GUtranFreqRelation= b1ThrRsrpFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation=         b1ThrRsrqFreqOffset 0
set EUtranCell.DD=.*,GUtranFreqRelation= qOffsetFreq 0

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 hysteresisB1     6
set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigB1GUtra=1 timeToTriggerB1  640

set LoadBalancingFunction=1        lbAllowedForEndcUe False
set EUtranCell.DD=                 lbActionForEndcUe 0
set ENodeBFunction=1               endcSplitAllowedMoVoice false

###added SubscriberGroupProfile=ENDC(PA13)
crn ENodeBFunction=1,SubscriberGroupProfile=ENDC
customTriggerType 2
customTriggerList 2
qciOffsetForQCI6 24
qciOffsetForQCI9 22
end


###added Qci30=Qci6 and Qci31=Qci9//set eutranFreqToQciProfileRelation values (PA13)

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci30
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         2000
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             6
priorityFraction                     0
qci                                  30
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     2
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        60
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         300
zzzTemporary1                        1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

crn ENodeBFunction=1,QciTable=default,QciProfileOperatordefined=qci31
absPrioOverride                      0
aqmMode                              1
bitRateRecommendationEnabled         false
caOffloadingEnabled                  false
counterActiveMode                    false
dataFwdPerQciEnabled                 true
dlMaxHARQTxQci                       5
dlMaxWaitingTime                     0
dlMinBitRate                         0
dlResourceAllocationStrategy         1
drxPriority                          0
drxProfileRef                        ENodeBFunction=1,DrxProfile=0
dscp                                 26
endcProfileRef                       EndcProfile=1
harqPriority                         0
inactivityTimerOffset                0
laaSupported                         true
lessMaxDelayThreshold                0
logicalChannelGroupRef               QciTable=default,LogicalChannelGroup=3
paPartitionOverride                  false
pdb                                  300
pdbOffset                            0
pdcpSNLength                         12
priority                             9
priorityFraction                     0
qci                                  31
qciACTuning                          1000
qciSubscriptionQuanta                200
relativePriority                     1
resourceAllocationStrategy           1
resourceType                         0
rlcMode                              0
rlcSNLength                          10
rlfPriority                          0
rlfProfileRef                        RlfProfile=0
rohcEnabled                          false
rohcForUlDataEnabled                 false
schedulingAlgorithm                  4
serviceType                          0
srsAllocationStrategy                0
tReorderingDl                        35
tReorderingUl                        35
timerPriority                        0
timerProfileRef
ulMaxHARQTxQci                       5
ulMaxWaitingTime                     0
ulMinBitRate                         0
zzzTemporary1                        1
zzzTemporary2
zzzTemporary3                        -2000000000
zzzTemporary4                        -2000000000
zzzTemporary5                        -2000000000
end

lt all

set EUtranCell.DD=.*,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6

mr TABTAB21
ma TABTAB21 ^eutrancell arfcn ^1415
pr TABTAB21
if $nr_of_mos >= 1
for $mo in TABTAB21
$mordn = rdn($mo)
set $mordn,UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc  a1a2ThrRsrpQciOffsetEndc-6,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffsetEndc=0,a1a2ThrRsrqQciOffsetEndc=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci6
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

mr TABTAB23
ma TABTAB23 ^eutrancelltdd=
pr TABTAB23
if $nr_of_mos >= 1
for $mo in TABTAB23
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi


mr TABTAB09
ma TABTAB09 ^eutrancell earfcn  ^3690$
pr TABTAB09
if $nr_of_mos >= 1
for $mo in TABTAB09
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation   qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a5Thr1RsrpFreqQciOffset=72,a5Thr1RsrqFreqQciOffset=160,a5Thr2RsrpFreqQciOffset=-8,a5Thr2RsrqFreqQciOffset=-40,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
set $mordn,UeMeasControl=1,ReportConfigSearch qciA1A2ThrOffsets     qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30;a1a2ThrRsrpQciOffset=0,a1a2ThrRsrQQciOffset=0,qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31
done
fi

set QciTable=default,QciProfilePredefined=qci6$ relativePriority 2
set QciTable=default,QciProfileOperatorDefined=qci30$ relativePriority 100

cr EnodeBfunction=1,PmFlexCounterFilter=ENDC
set EnodeBfunction=1,PmFlexCounterFilter=ENDC endcFilterEnabled true
set EnodeBFunction=1,PmFlexCounterFilter=ENDC endcFilterMin 2
Set SubscriberGroupProfile=ENDC       profilePriority   5


#############################

gs+

set . qciA1A2ThrOffsets qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1

set . eutranFreqToQciProfileRelation qciProfileRef=ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1

set UeMeasControl=1,ReportConfigA1A2Endc=1 qciA1A2ThrOffsetsEndc

rdel ENodeBFunction=1,SubscriberGroupProfile=ENDC

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci30

rdel ENodeBFunction=1,QciTable=default,QciProfileOperatorDefined=qci31

#############################

mr TABTAB23
ma TABTAB23 ^eutrancelltdd=
pr TABTAB23
if $nr_of_mos >= 1
for $mo in TABTAB23
$mordn = rdn($mo)
set $mordn,EUtranFreqRelation=1415  eutranFreqToQciProfileRelation  a5Thr2RsrqFreqQciOffset=0,qciProfileRef=ManagedElement=$Nodename,ENodeBFunction=1,QciTable=default,QciProfilePredefined=qci1
done
fi

#############################

## CAIMAC Priority Changes CAIMC for ULS earfcn will be highest followed with preferred anchor layer & then other lte layers ###


set UePolicyOptimization zzzTemporary1 1

set EUtranFreqRelation=39150    endcHoFreqPriority -1
set EUtranFreqRelation=39294    endcHoFreqPriority -1
set EUtranFreqRelation=39151    endcHoFreqPriority -1
set EUtranFreqRelation=39295    endcHoFreqPriority -1
set EUtranFreqRelation=1415     endcHoFreqPriority 7
set EUtranFreqRelation=3690    endcHoFreqPriority 6

set EUtranFreqRelation=39150    endcAwareIdleModePriority 5
set EUtranFreqRelation=39294    endcAwareIdleModePriority 5
set EUtranFreqRelation=39151    endcAwareIdleModePriority 7
set EUtranFreqRelation=39295    endcAwareIdleModePriority 7
set EUtranFreqRelation=1415     endcAwareIdleModePriority 6
set EUtranFreqRelation=3690    endcAwareIdleModePriority 4

wait 2

#############################################################

ma cellockqqwer  ^eutrancell administrativeState 0
wait 5
lbl  EUtranCell
wait 10
lt all
wait 10
st EUtranCell
ldeb EUtranCell
wait 20
lt all
ldeb EUtranCell
st EUtranCell
lbl cellockqqwer
wait 20

##################################################

mr BAN_FUPPER
mr BAN_F8PQ
ma BAN_FUPPER ^EUtranCell.*DD primaryUpperLayerInd 1
st BAN_FUPPER

if $nr_of_mos >= 1
ma BAN_F8PQ EUtranCellFDD earfcndl ^1415
ma BAN_F8PQ ^eutrancelltdd=
pr BAN_F8PQ
for $mo in BAN_F8PQ
$mordn = rdn($mo)
set $mordn primaryUpperLayerInd  1
done
fi

get BAN_F8PQ additionalUpperLayerIndList
get BAN_F8PQ primaryUpperLayerInd

################################

set EUtranCell.DD=.*,EUtranFreqRelation=.* anrMeasOn true

################## Twamp addition in anchor nodes #######

crn Transport=1,Router=LTEUP,TwampResponder=NR
ipAddress Router=LTEUP,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
end

crn Transport=1,Router=NR,TwampResponder=NR
ipAddress Router=NR,InterfaceIPv6=NR,AddressIPv6=NR
udpPort 4001
end


"""


DEL_Vi_GNBCUCPFunction=""" 
########################################################################### Cell Specific Started -- NRCellCU={gUtranCell}##################################################

crn GNBCUCPFunction=1,NRCellCU={gUtranCell}
admissionLimitRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionLimit=Default
admissionPriorityRef GNBCUCPFunction=1,AdmissionControl=1,AdmissionPriority=Default
advUePosMode 0
caCellMeasProfileRef CarrierAggregation=1,CaCellMeasProfile=Default
caCellProfileRef CarrierAggregation=1,CaCellProfile=Default
cellLocalId {cellLocalId}
checkUeGrpAtCellOffload false
hiPrioDetEnabled false
interfaceSupervision 0
intraFreqMCCellProfileRef IntraFreqMC=1,IntraFreqMCCellProfile=Default
mcfbCellProfileRef Mcfb=1,McfbCellProfile=Default
mcpcNrdcPSCellEnabled false
mcpcNrdcPSCellProfileRef
mcpcPCellEnabled false
mcpcPCellProfileRef Mcpc=1,McpcPCellProfile=Default
mcpcPSCellEnabled false
mcpcPSCellProfileRef Mcpc=1,McpcPSCellProfile=Default
mdtCellProfileRef Mdt=1,MdtCellProfile=Default
mdtEnabled false
nCellChangeHigh
nCellChangeMedium
nRFrequencyRef NRNetwork=1,NRFrequency=629952-30
noOfPeriodicUeMeasPerRop 900
nrdcMnCellProfileRef NrdcControl=1,NrdcMnCellProfile=Default
offloadCellProfileRef TrafficOffload=1,OffloadCellProfile=Default
periodicCellProfileRef
pmUeIntraFreqCellProfileRef
pmUeIntraFreqEnabled false
primaryPLMNId mcc=404,mnc=10
pwsEmergencyAreaIdList
qHyst 4
qHystSfHigh
qHystSfMedium
resourceStatusMaxConnUe -2
sNonIntraSearchP 0
sNonIntraSearchQ
tEvaluation
tHystNormal
threshServingLowP 0
threshServingLowQ
trStPSCellProfileRef TrafficSteering=1,TrStPSCellProfile=Default
trStSaCellProfileRef TrafficSteering=1,TrStSaCellProfile=Default
transmitSib2 false
transmitSib4 false
transmitSib5 false
transmitSib9 false
uacProfileRef GNBCUCPFunction=1,AdmissionControl=1,Uac=1,UacProfile=Default
ucmCellProfileRef UeCovMeas=1,UcmCellProfile=Default
ueMCCellProfileRef UeMC=1,UeMCCellProfile=Default
userLabel {gUtranCell}
end

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},DESManagementFunction=1
desSwitch false
esNotAllowedTimePeriod
intraRatEsActivationOriginalCellLoadParameters threshold=10,timeDuration=900
periodicEsDuration 120
requiredWakeUpTime 180
end

crn GNBCUCPFunction=1,NRCellCU={gUtranCell},NRFreqRelation=629952
anrMeasOn true
caFreqRelMeasProfileRef CarrierAggregation=1,CaFreqRelMeasProfile=Default
cellReselectionPriority 7
cellReselectionSubPriority
mcpcPCellNrFreqRelProfileRef Mcpc=1,McpcPCellNrFreqRelProfile=Default
mcpcPSCellNrFreqRelProfileRef Mcpc=1,McpcPSCellNrFreqRelProfile=Default
mdtMeasOn true
nRFrequencyRef NRNetwork=1,NRFrequency=629952-30
nrdcA4ThrRsrpFreqOffset 0
offloadNrFreqRelProfileRef TrafficOffload=1,OffloadNrFreqRelProfile=Default
pMax 23
plmnIdList
plmnRestriction false
qOffsetFreq 0
qQualMin
qRxLevMin -140
redCapEnabled false
sIntraSearchP 62
sIntraSearchQ
tReselectionNR 2
tReselectionNrSfHigh
tReselectionNrSfMedium
threshXHighP 4
threshXHighQ
threshXLowP 0
threshXLowQ
trStSaNrFreqRelProfileRef TrafficSteering=1,TrStSaNrFreqRelProfile=Default
ucmNrFreqRelProfileRef UeCovMeas=1,UcmNrFreqRelProfile=Default
ueMCNrFreqRelProfileRef UeMC=1,UeMCNrFreqRelProfile=Default
end


##################################Cell Specific Ended-- NRCellCU={gUtranCell}############################


"""

DEL_Vi_GNBDUFunction = """
###############################Cell Specific Started -- NRCellDU={gUtranCell}############################


crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
administrativeState 1
arfcnDL {arfcnDL}
arfcnUL {arfcnUL}
bSChannelBwDL {bSChannelBwDL_UL}
bSChannelBwUL {bSChannelBwDL_UL}
configuredMaxTxPower {configuredMaxTxPower}
latitude {Latitude}
longitude {Longitude}
sectorEquipmentFunctionRef NodeSupport=1,SectorEquipmentFunction={sectorEquipmentFunctionId}
txDirection 0
txPowerChangeRate 1
txPowerPersistentLock false
txPowerRatio 100
end

crn GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId},CommonBeamforming=1
cbfMacroTaperType 0
coverageShape 1
digitalTilt 30
end

crn GNBDUFunction=1,NRCellDU={gUtranCell}
csiRsConfig16P csiRsControl16Ports=0
csiRsConfig2P aRestriction=3F,csiRsControl2Ports=1
csiRsConfig32P csiRsControl32Ports=0
csiRsConfig4P csiRsControl4Ports=1,i11Restriction=FF
csiRsConfig8P csiRsControl8Ports=1,i11Restriction=FFFF
pLMNIdList mcc=404,mnc=10
sibType2 siBroadcastStatus=0,siPeriodicity=64
sibType4 siBroadcastStatus=0,siPeriodicity=64
sibType5 siBroadcastStatus=0,siPeriodicity=64
sibType6 siBroadcastStatus=0,siPeriodicity=16
sibType7 siBroadcastStatus=0,siPeriodicity=64
sibType8 siBroadcastStatus=0,siPeriodicity=64
administrativeState 0
ailgDlPrbLoadLevel 0
ailgModType 0
ailgPdcchLoadLevel 0
bandListManual 78
cellBarred 1
cellLocalId {cellLocalId}
cellRange 12000
cellReservedForOperator 1
csiReportFormat 0
csiRsPeriodicity 40
dftSOfdmMsg3Enabled false
dftSOfdmPuschEnabled false
dl256QamEnabled true
dlMaxMuMimoLayers 0
maxUeSpeed 2
nRPCI {nRPCI}
nRSectorCarrierRef GNBDUFunction=1,NRSectorCarrier={nRSectorCarrierId}
nRTAC {nRTAC}
pdschStartPrbStrategy 3
pMax 23
puschStartPrbStrategy 3
pZeroNomPucch -110
pZeroNomPuschGrant -102
qRxLevMin -128
rachPreambleFormat 0
rachPreambleRecTargetPower -110
rachPreambleTransMax 10
rachRootSequence {rachRootSequence}
secondaryCellOnly false
siWindowLength 20
ssbDuration 1
ssbFrequency 629952
ssbOffset 0
ssbPeriodicity 20
ssbSubCarrierSpacing 30
subCarrierSpacing 30
tddSpecialSlotPattern 3
tddUlDlPattern 1
trsPeriodicity 40
trsPowerBoosting 0
ul256QamEnabled true
ulMaxMuMimoLayers 0
ulStartCrb 0
userLabel {gUtranCell}
end

############################################################################ Cell Specific Ended -- NRCellDU={gUtranCell}##########################################

"""


DEL_Vi_CGSWITCH_SCRIPT = """
############Cell Specific Started -- CgSwitch={gUtranCell}################

crn GNBDUFunction=1,UeCC=1,CgSwitch={gUtranCell}
ueConfGroupType 1
userLabel
end

crn GNBDUFunction=1,UeCC=1,CgSwitchCfg={gUtranCell}
dlCgSwitchMode 1
dlScgCritQualHyst 100
dlScgCritQualThresh
dlScgLowQualHyst 50
dlScgLowQualThresh 50
dlScgNoDataAcsiPeriodicity 300
ulCgSwitchMode 1
ulScgCritQualHyst 100
ulScgCritQualThresh
ulScgLowQualHyst 60
ulScgLowQualThresh 170
userLabel
end

crn GNBDUFunction=1,UeCC=1,CgSwitch={gUtranCell},CgSwitchUeCfg=Base
cgSwitchCfgRef GNBDUFunction=1,UeCC=1,CgSwitchCfg={gUtranCell}
prefUeGroupList
ueConfGroupList
ueGroupList
userLabel
end

############Cell Specific Ended -- CgSwitch={gUtranCell}################

"""
