from lib.child_modules.probes import request
from lib.child_modules.probes import response
from scapy.all import *

class Probes(object):
    """Handles all aspects of Probes for 802.11"""

    def __init__(self, dbInstance, unity):
        self.unity = unity
        self.request = request.Request(dbInstance, unity)
        self.response = response.Response(dbInstance, unity)

        ## Create
        dbInstance.db.execute("""
                                CREATE TABLE IF NOT EXISTS probes(marker INT,
                                                                  devid TEXT,
                                                                  pi_timestamp TIMESTAMPTZ,
                                                                  coord TEXT,
                                                                  subtype TEXT,
                                                                  addr1 TEXT,
                                                                  addr2 TEXT,
                                                                  essid TEXT);
                                """)


    def trigger(self, packet):
        """Trigger mechanism for Probe entries

        Returns True if:
            - Probe Request
            - Probe Response
        Otherwise returns False
        """

        ## Probe Request
        if packet.haslayer('Dot11ProbeReq'):
            self.request.entry(packet)
            return True

        ## Probe Response
        elif packet.haslayer('Dot11ProbeResp'):
            self.response.entry(packet)
            return True

        else:
            return False
