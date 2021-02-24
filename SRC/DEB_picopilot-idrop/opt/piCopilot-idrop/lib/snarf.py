import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *
from lib.parent_modules.probes import Probes
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
                              """,[self.unity.devid,])
        tMarker = dbInstance.db.fetchone()
        if tMarker is not None:
            self.unity.marker = tMarker[0]
        else:
            self.unity.marker = 0

        print ('Using pkt silent time of:\n{0}\n'.format(self.unity.seenMaxTimer))

        if sProtocol is not None:
            self.probes = Probes(self.cap, self.unity)
                #print('added probes')

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

    def k9(self, kDict):
        def snarf(packet):
            """This function listens for a given MAC
            Currently no logic for detecting FCfield, etc.
            This functionality will be added later on

            As well, no logic for multiple tgts on a given frame,
            yet.
            """
            #print self.packetCount
            #self.packetCount += 1

            tName = None
            match = False
            while match is False:
                a1 = kDict.get(packet.addr1)
                if a1 is not None:
                    tName = a1
                    match = True
                a2 = kDict.get(packet.addr2)
                if a2 is not None:
                    tName = a2
                    match = True
                a3 = kDict.get(packet.addr3)
                if a3 is not None:
                    tName = a3
                    match = True
                a4 = kDict.get(packet.addr4)
                if a4 is not None:
                    tName = a4
                    match = True
                match = True
            if tName is not None:

                ## Avoid 30 second lag on first sighting
                if self.kSeen is None:
                    self.kSeen = True

                    ## Handle main
                    self.handlerMain(packet)

                    ## Notify
                    #print('SNARF!! {0} traffic detected!'.format(tName))

                    ### verify before trusting hexstr(str())
                    notDecoded = hexstr(str(packet.notdecoded), onlyhex=1).split(' ')

                    try:
                        fSig = -(256 - int(notDecoded[self.unity.offset + 3], 16))
                    except IndexError:
                        fSig = ''
                    print('RSSI: {0}\n'.format(fSig))

                    ## Silence deltas
                    timeDelta = self.unity.origTime - int(time.time())
                    #if timeDelta > 30:

                    ## Reset the counter
                    self.unity.origTime = int(time.time())

                    notice = 'SNARF!! {0} traffic detected!'.format(tName)

                    ### MODIFY /opt/piCopilot-idrop/lib/notifier.py
                    #self.alt.notify(notice)
                    #time.sleep(3)
                    #self.cap.entry(packet)
                else:
                    ## Handle main
                    self.handlerMain(packet)


                    ## Notify
                    print('SNARF!! {0} traffic detected!'.format(tName))

                    ### verify before trusting hexstr(str())
                    notDecoded = hexstr(str(packet.notdecoded), onlyhex = 1).split(' ')

                    try:
                        fSig = -(256 - int(notDecoded[self.unity.offset + 3], 16))
                    except IndexError:
                        fSig = ''
                    print('RSSI: %s\n'.format(fSig))

                    ## Timestamp
                    timeDelta = self.unity.epoch - int(time.time())
                    if timeDelta > 30:
                        ## Reset the counter
                        self.unity.origTime = int(time.time())

                        notice = 'SNARF!! {0} traffic detected!'.format(tName)

                        ### MODIFY /opt/piCopilot-idrop/lib/notifier.py
                        # self.alt.notify(notice)
                        #time.sleep(3)
                        #self.cap.entry(packet)
            else:
                return
        return snarf


    ### Move to handler.py
    def handlerMain(self, packet):
        """Handles core aspect of logging

        As main is the total, only an entry to total is needed to track main
        """
        self.main.trigger(packet)

    ### Move to handler.py
    ### Break this down for a speed boost
    def handlerProtocol(self, packet):
        self.probes.trigger(packet)


    def seenTest(self, packet):
        """Gather essential identifiers for "have I seen this packet" test

        Return False to continue with this test.  "seenTest", if not seen,
        then continue

        Will return False if the delta of now and previous timestamp
        for a given frame are > self.unity.seenMaxTimer {Default 30 seconds},
        otherwise we ignore, and thus by ignoring, we do not clog up the logs

        Create a table, and store this data so we can query on the fly
            - only with psql
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
                    print('Trying unique')
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
                    
                    
                    ### THIS IS ENTRY POINT
                    if self.seenTest(packet) is False:
                        ### CLEAR HOT TO LOG

                        self.handlerMain(packet)
                        self.handlerProtocol(packet)
                        if self.pStore is not False:
                            self.pStore.write(packet)

                    else:
                        return

                else:
                    return


            else:
                ### THIS IS ENTRY POINT
                if self.seenTest(packet) is False:
                    ### CLEAR HOT TO LOG
                    self.handlerMain(packet)
                    self.handlerProtocol(packet)
                    if self.pStore is not False:
                        self.pStore.write(packet)
                else:
                    return
        return snarf


    def string(self, word):
        def snarf(packet):
            """This function controls what we gather and pass to the DB
            Right now, there is no filtering at all
            The object word is simply an example of closure

            The parsing work is currently done in dbControl.py,
            Eventually this needs to be a pure API type call with different libs,
            for choosing what type of db entries to make
            """
            self.cap.entry(packet)
            self.pCount += 1
            self.tCount += 1
            if self.pCount == 100:
                #print('{0} frames logged'.format(self.tCount))
                self.pCount = 0
        return snarf


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
