RJ_Vi_SiteBasic_ipv6_6631 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="1" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <dnPrefix>SubNetwork=Raj,SubNetwork=LTE,SubNetwork=BaseBand,MeContext={eNodeBName}</dnPrefix>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm xmlns="urn:com:ericsson:ecim:RcsLM">
            <lmId>1</lmId>
            <fingerprint>{eNodeBName}</fingerprint>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="2" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <action xmlns="urn:com:ericsson:ecim:1.0">
    <data>
      <ManagedElement>
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <Lm>
            <lmId>1</lmId>
            <IntegrationUnlock>
              <integrationUnlockId>1</integrationUnlockId>
              <activate />
            </IntegrationUnlock>
          </Lm>
        </SystemFunctions>
      </ManagedElement>
    </data>
  </action>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="3" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SecM xmlns="urn:com:ericsson:ecim:RcsSecM">
            <secMId>1</secMId>
            <UserManagement>
              <userManagementId>1</userManagementId>
              <LdapAuthenticationMethod xmlns="urn:com:ericsson:ecim:RcsLdapAuthentication">
                <ldapAuthenticationMethodId>1</ldapAuthenticationMethodId>
                <administrativeState>UNLOCKED</administrativeState>
              </LdapAuthenticationMethod>
              <UserIdentity xmlns="urn:com:ericsson:ecim:RcsUser">
                <userIdentityId>1</userIdentityId>
                <MaintenanceUser>
                  <maintenanceUserId>1</maintenanceUserId>
                  <userName>rbs</userName>
                  <password>
                    <cleartext />
                    <password>rbs</password>
                  </password>
                </MaintenanceUser>
              </UserIdentity>
            </UserManagement>
          </SecM>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <CliTls>
              <cliTlsId>1</cliTlsId>
              <administrativeState>UNLOCKED</administrativeState>
            </CliTls>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_OM</routerId>
            <ttl>64</ttl>
            <userLabel>LTE_OM</userLabel>
          </Router>
        </Transport>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>{fieldReplaceableUnitId}</fieldReplaceableUnitId>
            <TnPort xmlns="urn:com:ericsson:ecim:ReqTnPort">
              <tnPortId>{tnPortId}</tnPortId>
              <userLabel>{tnPortId}</userLabel>
            </TnPort>
          </FieldReplaceableUnit>
        </Equipment>
        <Transport>
          <transportId>1</transportId>
          <EthernetPort xmlns="urn:com:ericsson:ecim:RtnL2EthernetPort">
            <ethernetPortId>{tnPortId}</ethernetPortId>
            <administrativeState>UNLOCKED</administrativeState>
            <admOperatingMode>1G_FULL</admOperatingMode>
            <autoNegEnable>false</autoNegEnable>
            <encapsulation>ManagedElement=1,Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},TnPort={tnPortId}</encapsulation>
            <userLabel>{tnPortId}</userLabel>
          </EthernetPort>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>LTE_OM</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>LTE_OM</userLabel>
            <vlanId>{OAM_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_OM</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>LTE_OM</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_OM</encapsulation>
              <mtu>1500</mtu>
              <userLabel>LTE_OM</userLabel>
              <AddressIPv6>
                <addressIPv6Id>LTE_OM</addressIPv6Id>
                <address>{OAM_IP}</address>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
        </Transport>
        <SystemFunctions>
          <systemFunctionsId>1</systemFunctionsId>
          <SysM xmlns="urn:com:ericsson:ecim:RcsSysM">
            <sysMId>1</sysMId>
            <OamAccessPoint>
              <oamAccessPointId>1</oamAccessPointId>
              <accessPoint>ManagedElement=1,Transport=1,Router=LTE_OM,InterfaceIPv6=LTE_OM,AddressIPv6=LTE_OM</accessPoint>
            </OamAccessPoint>
            <OamTrafficClass>
              <oamTrafficClassId>1</oamTrafficClassId>
              <dscp>40</dscp>
            </OamTrafficClass>
            <Snmp xmlns="urn:com:ericsson:ecim:RcsSnmp">
              <snmpId>1</snmpId>
              <administrativeState>UNLOCKED</administrativeState>
              <agentAddress>
                <host>0.0.0.0</host>
                <port>161</port>
              </agentAddress>
              <SnmpTargetV2C>
                <snmpTargetV2CId>1</snmpTargetV2CId>
                <community>enm-public</community>
                <address>2400:5200:a000:0000:0000:0009:0f00:03e5</address>
                <port>162</port>
                <administrativeState>UNLOCKED</administrativeState>
              </SnmpTargetV2C>
            </Snmp>
            <TimeM xmlns="urn:com:ericsson:ecim:RcsTimeM">
              <timeMId>1</timeMId>
              <Ntp>
                <ntpId>1</ntpId>
                <NtpServer>
                  <ntpServerId>1</ntpServerId>
                  <serverAddress>2400:5200:a000:0000:0000:0009:0f00:0344</serverAddress>
                  <userLabel>NTP TOD1</userLabel>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
                <NtpServer>
                  <ntpServerId>2</ntpServerId>
                  <serverAddress>2400:5200:a000:0000:0000:0009:0f00:0343</serverAddress>
                  <userLabel>NTP TOD2</userLabel>
                  <administrativeState>UNLOCKED</administrativeState>
                </NtpServer>
              </Ntp>
            </TimeM>
          </SysM>
        </SystemFunctions>
        <Transport>
          <transportId>1</transportId>
          <Ptp xmlns="urn:com:ericsson:ecim:RsyncPtp">
            <ptpId>1</ptpId>
            <BoundaryOrdinaryClock>
              <boundaryOrdinaryClockId>PTP1</boundaryOrdinaryClockId>
              <clockType>SLAVE_ONLY_ORDINARY_CLOCK</clockType>
              <domainNumber>0</domainNumber>
              <priority1>255</priority1>
              <priority2>255</priority2>
              <ptpProfile>G_8265_1</ptpProfile>
              <PtpBcOcPort xmlns="urn:com:ericsson:ecim:RsyncPtpBcOcPort">
                <ptpBcOcPortId>1</ptpBcOcPortId>
                <administrativeState>UNLOCKED</administrativeState>
                <announceMessageInterval>1</announceMessageInterval>
                <associatedGrandmaster>2400:5200:a000:0:0:9:1a00:42</associatedGrandmaster>
                <asymmetryCompensation>0</asymmetryCompensation>
                <dscp>56</dscp>
                <durationField>300</durationField>
                <localPriority>128</localPriority>
                <masterOnly>false</masterOnly>
                <pBit>7</pBit>
                <ptpMulticastAddress>FORWARDABLE</ptpMulticastAddress>
                <ptpPathTimeError>750</ptpPathTimeError>
                <syncMessageInterval>-4</syncMessageInterval>
                <transportInterface>ManagedElement=1,Transport=1,Router=LTE_OM,InterfaceIPv6=LTE_OM,AddressIPv6=LTE_OM</transportInterface>
              </PtpBcOcPort>
            </BoundaryOrdinaryClock>
          </Ptp>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_OM</routerId>
            <DnsClient xmlns="urn:com:ericsson:ecim:RtnDnsClient">
              <dnsClientId>1</dnsClientId>
              <dscp>40</dscp>
              <serverAddress>2400:5200:a000:0000:0000:0009:0f00:0344</serverAddress>
              <serverAddress>2400:5200:a000:0000:0000:0009:0f00:0343</serverAddress>
            </DnsClient>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <ttl>64</ttl>
            <userLabel>LTE_CP</userLabel>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_UP</routerId>
            <ttl>64</ttl>
            <userLabel>LTE_UP</userLabel>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>GSM_ABIS</routerId>
            <ttl>64</ttl>
            <userLabel>GSM_ABIS</userLabel>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>GSM_ABIS</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>GSM_ABIS</userLabel>
            <vlanId>{ABIS_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>GSM_ABIS</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>GSM_ABIS</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=GSM_ABIS</encapsulation>
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
              <userLabel>GSM_ABIS</userLabel>
              <AddressIPv4>
                <addressIPv4Id>GSM_ABIS</addressIPv4Id>
                <address>{ABIS_IP}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>LTE_CP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>LTE_CP</userLabel>
            <vlanId>{LTE_S1_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>LTE_CP</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_CP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>LTE_CP</userLabel>
            </InterfaceIPv6>
          </Router>
          <VlanPort xmlns="urn:com:ericsson:ecim:RtnL2VlanPort">
            <vlanPortId>LTE_UP</vlanPortId>
            <encapsulation>ManagedElement=1,Transport=1,EthernetPort={tnPortId}</encapsulation>
            <isTagged>true</isTagged>
            <userLabel>LTE_UP</userLabel>
            <vlanId>{LTE_UP_vlan}</vlanId>
          </VlanPort>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_UP</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>LTE_UP</interfaceIPv6Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_UP</encapsulation>
              <mtu>1500</mtu>
              <userLabel>LTE_UP</userLabel>
            </InterfaceIPv6>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>LTE_CP</interfaceIPv6Id>
              <AddressIPv6>
                <addressIPv6Id>LTE_CP</addressIPv6Id>
                <address>{LTE_S1_IP}</address>
                <configurationMode>MANUAL</configurationMode>
                <duidType>DUID_LLT</duidType>
                <primaryAddress>true</primaryAddress>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_UP</routerId>
            <InterfaceIPv6 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv6">
              <interfaceIPv6Id>LTE_UP</interfaceIPv6Id>
              <AddressIPv6>
                <addressIPv6Id>LTE_UP</addressIPv6Id>
                <address>{LTE_UP_IP}</address>
                <configurationMode>MANUAL</configurationMode>
                <duidType>DUID_LLT</duidType>
                <primaryAddress>true</primaryAddress>
              </AddressIPv6>
            </InterfaceIPv6>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>GSM_ABIS</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>1</routeTableIPv4StaticId>
              <Dst>
                <dstId>GSM_ABIS</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{ABIS_GW}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>4</routeTableIPv6StaticId>
              <Dst>
                <dstId>LTE_CP</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_UP</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>3</routeTableIPv6StaticId>
              <Dst>
                <dstId>LTE_UP</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
              <Dst>
                <dstId>TWAMP</dstId>
                <dst>2402:8100:4000:1:1:1:ff:f806/128</dst>
                <NextHop>
                  <nextHopId>2</nextHopId>
                  <address>{LTE_UP_GW}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_OM</routerId>
            <RouteTableIPv6Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv6">
              <routeTableIPv6StaticId>1</routeTableIPv6StaticId>
              <Dst>
                <dstId>LTE_OM</dstId>
                <dst>::/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{OAM_GW}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
            </RouteTableIPv6Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE_CP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_CP</encapsulation>
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
              <userLabel>LTE_CP</userLabel>
              <AddressIPv4>
                <addressIPv4Id>LTE_CP</addressIPv4Id>
                <address>{LTE_S1_IP_V4}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_CP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>3</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTE_CP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_S1_GW_V4}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_UP</routerId>
            <InterfaceIPv4 xmlns="urn:com:ericsson:ecim:RtnL3InterfaceIPv4">
              <interfaceIPv4Id>LTE_UP</interfaceIPv4Id>
              <encapsulation>ManagedElement=1,Transport=1,VlanPort=LTE_UP</encapsulation>
              <mtu>1500</mtu>
              <pcpArp>6</pcpArp>
              <userLabel>LTE_UP</userLabel>
              <AddressIPv4>
                <addressIPv4Id>LTE_UP</addressIPv4Id>
                <address>{LTE_UP_IP_V4}</address>
              </AddressIPv4>
            </InterfaceIPv4>
          </Router>
          <Router xmlns="urn:com:ericsson:ecim:RtnL3Router">
            <routerId>LTE_UP</routerId>
            <RouteTableIPv4Static xmlns="urn:com:ericsson:ecim:RtnRoutesStaticRouteIPv4">
              <routeTableIPv4StaticId>2</routeTableIPv4StaticId>
              <Dst>
                <dstId>LTE_UP</dstId>
                <dst>0.0.0.0/0</dst>
                <NextHop>
                  <nextHopId>1</nextHopId>
                  <address>{LTE_UP_GW_V4}</address>
                  <adminDistance>1</adminDistance>
                  <bfdMonitoring>true</bfdMonitoring>
                </NextHop>
              </Dst>
            </RouteTableIPv4Static>
          </Router>
        </Transport>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="4" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>1</managedElementId>
        <networkManagedElementId>{eNodeBName}</networkManagedElementId>
      </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>
"""


# Vi_RBSSummary_script with the package the Vi RJ nodes run (LO01INRJ207062: CXP2010174/2-R32S15)
RJ_Vi_RBSSummary_script = """
<summary:AutoIntegrationRbsSummaryFile xmlns:summary="http://www.ericsson.se/RbsSummaryFileSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.ericsson.se/RbsSummaryFileSchemaSummaryFile.xsd">
  <Format revision="F" />
  <ConfigurationFiles siteBasicFilePath="{siteBasicFilePath}" siteEquipmentFilePath="{siteEquipmentFilePath}" upgradePackageFilePath="Baseband_Radio_Node-CXP2010174_2-R32S15" />
</summary:AutoIntegrationRbsSummaryFile>
"""


# 02 SiteEquipment of the RJ_Vi radios, as configured on LO01INRJ207062 (25.Q2):
# Radio 2271 B0C (L900 + GSM, RRU-11..13): RfPort A / B (RfBranch 1 / 2) + R (RET, no VSWR supervision), DATA_1 / 2,
# AntennaSubunit=1 tilt range -900..900, 2 RfBranches on the SectorEquipmentFunction. The RET (AntennaNearUnit) is
# site specific and not created here.
RJ_Vi_RRU_2271_B0C_2X2 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="sectorEquipmentFunctionId={sectorEquipmentFunctionId}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
		<userLabel>{eNodeBName}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
		  <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>RRU-{Radio_UnitId}</fieldReplaceableUnitId>
			<administrativeState>UNLOCKED</administrativeState>
			<isSharedWithExternalMe>false</isSharedWithExternalMe>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>A</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>B</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>R</rfPortId>
              <vswrSupervisionActive>false</vswrSupervisionActive>
              <vswrSupervisionSensitivity>-1</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>			
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_1</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_2</riPortId>
            </RiPort>
          </FieldReplaceableUnit>
        </Equipment>
		
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
          </AntennaUnitGroup>		  
        </Equipment>
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
			<AntennaUnit>
              <antennaUnitId>1</antennaUnitId>
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>
			  <AntennaSubunit>
                <antennaSubunitId>1</antennaSubunitId>  
                <maxTotalTilt>900</maxTotalTilt>
                <minTotalTilt>-900</minTotalTilt>				
				<AuPort>
                  <auPortId>1</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>2</auPortId>
                </AuPort>				
			  </AntennaSubunit>
            </AntennaUnit>
          </AntennaUnitGroup>
        </Equipment>		
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
            <RfBranch>
              <rfBranchId>1</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=1</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=A</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>2</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=2</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=B</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
          </AntennaUnitGroup>
		</Equipment>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>		  
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>{Radio_UnitId}</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>
          </RiLink>
		</Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>		  
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>
            <administrativeState>LOCKED</administrativeState>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=1</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=2</rfBranchRef>
          </SectorEquipmentFunction>  
        </NodeSupport>
	  </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>


"""

# Radio 4490 44B1 44B3 C (UBR L1800 + L2100, RRU-21/22): RfPort A-D = RfBranch 1-4, no RfPort R, DATA_1 / 2,
# AntennaSubunit=1 tilt range -900..900, 4 RfBranches on the SectorEquipmentFunction.
RJ_Vi_RRU_4490_B1B3_4X4 = """
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <capabilities>
    <capability>urn:ietf:params:netconf:base:1.0</capability>
  </capabilities>
</hello>
]]>]]>
<rpc message-id="sectorEquipmentFunctionId={sectorEquipmentFunctionId}" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <edit-config>
    <target>
      <running />
    </target>
    <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <ManagedElement xmlns="urn:com:ericsson:ecim:ComTop">
        <managedElementId>{eNodeBName}</managedElementId>
		<userLabel>{eNodeBName}</userLabel>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
		  <FieldReplaceableUnit xmlns="urn:com:ericsson:ecim:ReqFieldReplaceableUnit">
            <fieldReplaceableUnitId>RRU-{Radio_UnitId}</fieldReplaceableUnitId>
			<administrativeState>UNLOCKED</administrativeState>
			<isSharedWithExternalMe>false</isSharedWithExternalMe>			
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>A</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>B</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>C</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>
            <RfPort xmlns="urn:com:ericsson:ecim:ReqRfPort">
              <rfPortId>D</rfPortId>
              <vswrSupervisionActive>true</vswrSupervisionActive>
              <vswrSupervisionSensitivity>100</vswrSupervisionSensitivity>
              <administrativeState>UNLOCKED</administrativeState>
              <antennaSupervisionActive>false</antennaSupervisionActive>
            </RfPort>			
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_1</riPortId>
            </RiPort>
            <RiPort xmlns="urn:com:ericsson:ecim:ReqRiPort">
              <riPortId>DATA_2</riPortId>
            </RiPort>
          </FieldReplaceableUnit>
        </Equipment>
		
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
          </AntennaUnitGroup>		  
        </Equipment>
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
			<AntennaUnit>
              <antennaUnitId>1</antennaUnitId>
              <mechanicalAntennaTilt>0</mechanicalAntennaTilt>
			  <AntennaSubunit>
                <antennaSubunitId>1</antennaSubunitId>  
                <maxTotalTilt>900</maxTotalTilt>
                <minTotalTilt>-900</minTotalTilt>				
				<AuPort>
                  <auPortId>1</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>2</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>3</auPortId>
                </AuPort>
				<AuPort>
                  <auPortId>4</auPortId>
                </AuPort>				
			  </AntennaSubunit>
            </AntennaUnit>
          </AntennaUnitGroup>
        </Equipment>		
		<Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>
          <AntennaUnitGroup xmlns="urn:com:ericsson:ecim:ReqAntennaSystem">
            <antennaUnitGroupId>{Radio_UnitId}</antennaUnitGroupId>
            <RfBranch>
              <rfBranchId>1</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=1</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=A</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>2</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=2</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=B</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>3</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=3</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=C</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>	
            <RfBranch>
              <rfBranchId>4</rfBranchId>
              <auPortRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},AntennaUnit=1,AntennaSubunit=1,AuPort=4</auPortRef>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlAttenuation>0</dlAttenuation>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <dlTrafficDelay>-1</dlTrafficDelay>
              <rfPortRef>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RfPort=D</rfPortRef>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulAttenuation>0</ulAttenuation>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
              <ulTrafficDelay>-1</ulTrafficDelay>
            </RfBranch>			
          </AntennaUnitGroup>
		</Equipment>
        <Equipment xmlns="urn:com:ericsson:ecim:ReqEquipment">
          <equipmentId>1</equipmentId>		  
          <RiLink xmlns="urn:com:ericsson:ecim:ReqRiLink">
            <riLinkId>{Radio_UnitId}</riLinkId>
            <riPortRef1>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit={fieldReplaceableUnitId},RiPort={RiPort_BB}</riPortRef1>
            <riPortRef2>ManagedElement={eNodeBName},Equipment=1,FieldReplaceableUnit=RRU-{Radio_UnitId},RiPort={RiPort_Radio}</riPortRef2>
          </RiLink>
		</Equipment>
        <NodeSupport xmlns="urn:com:ericsson:ecim:RmeSupport">
          <nodeSupportId>1</nodeSupportId>		  
          <SectorEquipmentFunction xmlns="urn:com:ericsson:ecim:RmeSectorEquipmentFunction">
            <sectorEquipmentFunctionId>{sectorEquipmentFunctionId}</sectorEquipmentFunctionId>
            <administrativeState>LOCKED</administrativeState>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=1</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=2</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=3</rfBranchRef>
				<rfBranchRef>ManagedElement={eNodeBName},Equipment=1,AntennaUnitGroup={Radio_UnitId},RfBranch=4</rfBranchRef>
          </SectorEquipmentFunction>  
        </NodeSupport>
	  </ManagedElement>
    </config>
  </edit-config>
</rpc>
]]>]]>
<rpc message-id="Closing" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <close-session></close-session>
</rpc>
]]>]]>


"""
