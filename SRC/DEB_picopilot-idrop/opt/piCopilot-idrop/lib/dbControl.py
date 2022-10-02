import getpass
import logging
import os
import psycopg2
import sys
import time
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

class Builder(object):
    """This class builds or adds on to a pgsql database"""

    def __init__(self, unity):

        ## Unify
        self.unity = unity

        ## Create Base directory
        self.bDir = os.getcwd()

        ## Logs
        self.dDir = '%s/logs' % self.bDir
        if not os.path.isdir(self.dDir):
            os.makedirs(self.dDir)

        ## Create directory list for dDir
        self.dList = os.listdir(self.dDir)

        ## Construct and connect to pgsql
        if self.unity.conf.mode != 'ids':
            try:
                cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(unity.conf.db, unity.conf.user, unity.conf.host, unity.conf.password)
                self.con = psycopg2.connect(cStr)
                self.con.autocommit = True
                self.db = self.con.cursor()

                ## Test for wipe
                if self.unity.args.wipe is True:
                    self.db.execute('DROP TABLE IF EXISTS blue;')
                    self.db.execute('DROP TABLE IF EXISTS k9;')
                    self.db.execute('DROP TABLE IF EXISTS main;')
                    self.db.execute('DROP TABLE IF EXISTS probes;')
                    self.db.execute('DROP TABLE IF EXISTS targets;')
                    self.db.execute('DROP TABLE IF EXISTS timer;')
                    self.db.execute('DROP TABLE IF EXISTS uniques;')
                    self.con.close()
                    print('Tables dropped\n  [+] Exiting\n')
                    sys.exit(0)
            except Exception as E:
                print(E)
                sys.exit(1)
        else:
            try:
                cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}' sslmode='verify-full'" % (unity.conf.dbName, unity.conf.user, unity.conf.host, unity.conf.password)
                self.con = psycopg2.connect(cStr)
                self.con.autocommit = True
                self.db = self.con.cursor()

                ## Test for wipe
                if self.unity.args.wipe is True:
                    self.db.execute('DROP TABLE IF EXISTS ids;')
                    self.db.execute('DROP TABLE IF EXISTS heartbeats;')
                    self.con.close()
                    print('Tables dropped\n  [+] Exiting\n')
                    sys.exit(0)
            except Exception as E:
                print(E)
                sys.exit(1)


    def heartStamp(self):
        return time.strftime('%Y%m%d-%H%M%S', time.localtime())
