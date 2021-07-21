from scapy.all import *

class Response(object):
    """Adds Probe Response entries"""
    def __init__(self, dbInstance, unity):
        self.cap = dbInstance
        self.unity = unity


    def entry(self, packet):
        """packet.haslayer('Dot11ProbeResp')"""
        try:
            self.cap.db.execute("""
                                INSERT INTO probes (marker,
                                                    devid,
                                                    pi_timestamp,
                                                    coord,
                                                    subtype,
                                                    addr1,
                                                    addr2,
                                                    essid)
                                            VALUES (%s,
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
                                      self.unity.PE.sType.mgmtSubtype(packet.subtype),
                                      packet.addr1,
                                      packet.addr2,
                                      packet[Dot11Elt].info.decode()))
        except Exception as E:
            print (E)
