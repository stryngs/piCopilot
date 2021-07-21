import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from lib.parent_modules.k9 import K9
from lib.parent_modules.probes import Probes
from lib.parent_modules.k9 import K9
from lib.main import Main
from lib.notifier import Alert
from lib.shared import Shared

class Snarf(object):
    """Main class for packet handling"""
    def __init__(self, dbInstance, unity, sProtocol):
        self.cap = dbInstance
        self.unity = unity
        self.main = Main(self.cap, self.unity)
        self.protocols = []
        self.unity.seenDict = {}
        self.packetCount = 0
        self.alt = Alert()
        self.kSeen = None

        ### Eventually backport this
        self.sh = Shared()
        self.sh.unity = self.unity
        
        ## Notate devid and current marker
        dbInstance.db.execute("""
                              SELECT marker FROM main WHERE devid = %s ORDER BY marker DESC LIMIT 1;
                              """,[str(self.unity.devid),])
        tMarker = dbInstance.db.fetchone()
        if tMarker is not None:
            self.unity.marker = tMarker[0]
        else:
            self.unity.marker = 0

        print ('Using pkt silent time of:\n{0}\n'.format(self.unity.seenMaxTimer))

        ## Protocols
        if sProtocol is not None:
            self.probes = Probes(self.cap, self.unity)

        ## k9 prep
        self.k9 = K9(self.cap, self.unity)
        if self.k9.kExist is True:
            self.pHandler = self.snarfTgt
        else:
            self.pHandler = self.snarfOpen

        ## Deal with PCAP storage
        if self.unity.args.pcap:
            tStamp = time.strftime('%Y%m%d_%H%M', time.localtime()) + '.pcap'
            pLog = self.cap.dDir + '/' + tStamp
            self.pStore = PcapWriter(pLog, sync = True)
        else:
            self.pStore = False

        ## Track unique addr combos
        self.cap.db.execute("""
                            CREATE TABLE IF NOT EXISTS uniques(marker INT,
                                                               devid TEXT,
                                                               pi_timestamp TIMESTAMPTZ,
                                                               coord TEXT,
                                                               type TEXT,
                                                               subtype TEXT,
                                                               FCfield TEXT,
                                                               addr1 TEXT,
                                                               addr2 TEXT,
                                                               addr3 TEXT,
                                                               addr4 TEXT,
                                                               UNIQUE (subtype,
                                                                       type,
                                                                       FCfield,
                                                                       addr1,
                                                                       addr2,
                                                                       addr3,
                                                                       addr4))
                             """)

    def snarfMin(self, packet):
        """Main only"""
        self.main.trigger(packet)

    def snarfOpen(self, packet):
        """Main and probes"""
        self.main.trigger(packet)
        self.probes.trigger(packet)


    def snarfTgt(self, packet):
        """Main, probes and k9"""
        self.main.trigger(packet)
        self.probes.trigger(packet)
        self.k9.trigger(packet)

    def seenTest(self, packet):
        """Gather essential identifiers for "have I seen this packet" test

        Return False to continue with this test.  "seenTest", if not seen,
        then continue

        Will return False if the delta of now and previous timestamp
        for a given frame are > self.unity.seenMaxTimer {Default 30 seconds},
        otherwise we ignore, and thus by ignoring, we do not clog up the logs
        """
        try:
            p = (packet[Dot11].subtype,
                 packet[Dot11].type,
                 packet[Dot11].FCfield,
                 packet[Dot11].addr1,
                 packet[Dot11].addr2,
                 packet[Dot11].addr3,
                 packet[Dot11].addr4)

            ## Figure out if this combo has been seen before
            if p not in self.unity.seenDict:
                self.unity.seenDict.update({p: (1, time.time())})

                ## Store the entry
                pType = self.unity.PE.conv.symString(packet[Dot11], 'type')
                subType = self.subParser(packet)
                fcField = self.unity.PE.conv.symString(packet[Dot11], 'FCfield')
                try:
                    self.cap.db.execute("""
                                        INSERT INTO uniques (marker,
                                                             devid,
                                                             pi_timestamp,
                                                             coord,
                                                             type,
                                                             subtype,
                                                             FCfield,
                                                             addr1,
                                                             addr2,
                                                             addr3,
                                                             addr4)
                                                     VALUES (%s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s,
                                                             %s);
                                        """, (self.unity.marker,
                                              self.unity.devid,
                                              self.unity.pi_timestamp,
                                              self.unity.coord,
                                              pType,
                                              subType,
                                              fcField,
                                              packet.addr1,
                                              packet.addr2,
                                              packet.addr3,
                                              packet.addr4))
                except Exception as E:
                    pass
                    #print (E)

                return False

            ## Has been seen, now check time
            else:
                lastTime = self.unity.seenDict.get(p)[1]
                lastCount = self.unity.seenDict.get(p)[0]
                if (time.time() - lastTime) > self.unity.seenMaxTimer:

                    ## Update delta timestamp
                    self.unity.seenDict.update({p: (lastCount + 1, time.time())})
                    #print ('PASS TIMER')
                    return False
                else:
                    #print ('FAIL TIMER')
                    
                    ## Revert the count
                    self.unity.marker -= 1
                    
                    return True
        except:
            pass


    def sniffer(self):
        def snarf(packet):
            """Sniff the data"""
            
            ## Notate the time
            self.unity.times()

            ## Test for whitelisting if wanted
            if len(self.unity.wSet) > 0:
                if self.whiteLister(self.unity.wSet, packet) is False:
                    if self.seenTest(packet) is False:
                        self.pHandler(packet)
                        if self.pStore is not False:
                            self.pStore.write(packet)
                    else:
                        return
                else:
                    return
            else:
                if self.seenTest(packet) is False:
                    self.pHandler(packet)
                    if self.pStore is not False:
                        self.pStore.write(packet)
                else:
                    return
        return snarf


    def subParser(self, packet):
        if packet.type == 0:
            self.subType = self.unity.PE.sType.mgmtSubtype(packet.subtype)
        elif packet.type == 1:
            self.subType = self.unity.PE.sType.ctrlSubtype(packet.subtype)
        elif packet.type == 2:
            self.subType = self.unity.PE.sType.dataSubtype(packet.subtype)
        else:
            self.subType = packet.subtype

        if self.subType is None:
            return packet.subtype
        else:
            return self.subType


    def whiteLister(self, wSet, packet):
        """Return True if any addr found in wSet"""
        if packet.addr1 in wSet:
            return True
        if packet.addr2 in wSet:
            return True
        if packet.addr3 in wSet:
            return True
        if packet.addr4 in wSet:
            return True
        return False
