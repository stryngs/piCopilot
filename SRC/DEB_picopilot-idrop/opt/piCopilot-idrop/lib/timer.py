import gpsd
import psycopg2
import time
from lib.location import Location

class Timer(object):
    def __init__(self, db, user, host, password):
        self.epoch = None
        self.coord = None
        self.loc = Location()
        self.db = db
        self.user = user
        self.host = host
        self.password = password
        self.dbCon()

        ## Create table for time marking
        self._db.execute("""
                         CREATE TABLE IF NOT EXISTS timer(pi_timestamp TIMESTAMPTZ,
                                                         coord TEXT);
                         """)


        ## Construct and connect to pgsql
    def dbCon(self):
        cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(self.db, self.user, self.host, self.password)
        self._con = psycopg2.connect(cStr)
        self._con.autocommit = True
        self._db = self._con.cursor()


    def tMark(self):
        """Timestamp function

        Sets a unified timestamp marker
        """
        ### This converts to Wireshark style
        #int(wepCrypto.endSwap('0x' + p.byteRip(f.notdecoded[8:], qty = 8, compress = True)), 16)
        epoch = time.localtime()
        coord = self.loc.getCoord()
        pi_timestamp = time.strftime('%Y-%m-%d %H:%M:%S', epoch)

        self._db.execute("""
                         INSERT INTO timer (pi_timestamp,
                                           coord)
                                   VALUES (%s,
                                           %s);
                         """, (pi_timestamp, coord))
