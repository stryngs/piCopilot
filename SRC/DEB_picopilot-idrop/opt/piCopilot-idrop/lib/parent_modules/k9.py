import os
from scapy.all import *

class K9(object):
    """Handles all aspects of notating specific MACs for 802.11"""

    def __init__(self, dbInstance, unity):
        self.unity = unity
        self.dbInstance = dbInstance
        self.kExist = False

        ## Create table for storing info about various targets -- Allows for multiple insertions for a given mac
        dbInstance.db.execute("""
                              CREATE TABLE IF NOT EXISTS targets(target TEXT,
                                                                 reason TEXT,
                                                                 UNIQUE (target,
                                                                         reason));
                              """)

        ## Create table to store finds in
        dbInstance.db.execute("""
                                CREATE TABLE IF NOT EXISTS k9(marker INT,
                                                              devid TEXT,
                                                              pi_timestamp TIMESTAMPTZ,
                                                              coord TEXT,
                                                              addr TEXT);
                                """)

        ## Bring in any new targets
        if os.path.isfile('targets.lst'):
            with open('targets.lst') as iFile:
                tRows = iFile.read().splitlines()

            for t in tRows:
                if len(t) > 0:

                    ## Mark it
                    self.kExist = True

                    ## Notate it
                    mac = t.split()[0].lower()
                    reason = ' '.join(t.split()[1:])
                    try:
                        self.unity.kTargets.add(mac)
                    except Exception as E:
                        print(E)
                    try:
                        dbInstance.db.execute("""
                                            INSERT INTO targets (target,
                                                                 reason)
                                                         VALUES (%s,
                                                                 %s);
                                            """, (mac, reason))
                    except Exception as E:
                        pass


    def trigger(self, packet):
        """Trigger mechanism for k9 entries"""
        addr1 = None
        addr2 = None
        addr3 = None
        addr4 = None
        if packet.addr1 in self.unity.kTargets:
            tgr = True
            addr1 = packet.addr1
        elif packet.addr2 in self.unity.kTargets:
            tgr = True
            addr2 = packet.addr2
        elif packet.addr3 in self.unity.kTargets:
            tgr = True
            addr3 = packet.addr3
        elif packet.addr4 in self.unity.kTargets:
            tgr = True
            addr4 = packet.addr4
        else:
            tgr = False

        ## The most likely, thus first
        if tgr is False:
            return
        else:
            if addr1 is not None:
                try:
                    self.dbInstance.db.execute("""
                                        INSERT INTO k9 (marker,
                                                        devid,
                                                        pi_timestamp,
                                                        coord,
                                                        addr)
                                                VALUES (%s,
                                                        %s,
                                                        %s,
                                                        %s,
                                                        %s);
                                        """, (self.unity.marker,
                                              self.unity.devid,
                                              self.unity.pi_timestamp,
                                              self.unity.coord,
                                              addr1))
                except Exception as E:
                    print (E)
            if addr2 is not None:
                try:
                    self.dbInstance.db.execute("""
                                        INSERT INTO k9 (marker,
                                                        devid,
                                                        pi_timestamp,
                                                        coord,
                                                        addr)
                                                VALUES (%s,
                                                        %s,
                                                        %s,
                                                        %s,
                                                        %s);
                                        """, (self.unity.marker,
                                              self.unity.devid,
                                              self.unity.pi_timestamp,
                                              self.unity.coord,
                                              addr2))
                except Exception as E:
                    print (E)
            if addr3 is not None:
                try:
                    self.dbInstance.db.execute("""
                                        INSERT INTO k9 (marker,
                                                        devid,
                                                        pi_timestamp,
                                                        coord,
                                                        addr)
                                                VALUES (%s,
                                                        %s,
                                                        %s,
                                                        %s,
                                                        %s);
                                        """, (self.unity.marker,
                                              self.unity.devid,
                                              self.unity.pi_timestamp,
                                              self.unity.coord,
                                              addr3))
                except Exception as E:
                    print (E)
            if addr4 is not None:
                try:
                    self.dbInstance.db.execute("""
                                        INSERT INTO k9 (marker,
                                                        devid,
                                                        pi_timestamp,
                                                        coord,
                                                        addr)
                                                VALUES (%s,
                                                        %s,
                                                        %s,
                                                        %s,
                                                        %s);
                                        """, (self.unity.marker,
                                              self.unity.devid,
                                              self.unity.pi_timestamp,
                                              self.unity.coord,
                                              addr4))
                except Exception as E:
                    print (E)
        return
