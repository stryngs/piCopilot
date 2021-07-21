import csv
import os
import psycopg2
import sys

class Exporter(object):
    """All things sql export"""

    def __init__(self, shared):
        self.shared = shared


    def pgsqlConnect(self):
        ## Connects
        cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(self.shared.conf.db, self.shared.conf.user, self.shared.conf.host, self.shared.conf.password)
        self.con = psycopg2.connect(cStr)
        self.con.autocommit = True
        self.db = self.con.cursor()


    def pgsqlExporter(self):
        ## Tables
        self.db.execute("""
                        CREATE TEMPORARY TABLE allprobes AS
                        SELECT P.pi_timestamp, M.rssi, P.essid, P.subtype, P.addr2, P.addr1
                        FROM probes P INNER JOIN main M
                        ON M.marker = P.marker
                        WHERE
                        P.devid = M.devid
                        AND
                        P.subtype LIKE 'Probe %';
                        """)
        self.db.execute("""
                        CREATE TEMPORARY TABLE tods AS
                        SELECT addr2, addr3
                        FROM main WHERE type = 'Data'
                        AND direc = 'to-ds';
                        """)
        self.db.execute("""
                        CREATE TEMPORARY TABLE dsto AS
                        SELECT addr3, addr2
                        FROM main WHERE type = 'Data'
                        AND direc = 'to-ds';
                        """)
        self.db.execute("""
                        SELECT * FROM tods;
                        """)
        t1 = set(self.db.fetchall())
        self.db.execute("""
                        SELECT * FROM dsto;
                        """)
        t2 = set(self.db.fetchall())
        pipeList = list(t1 & t2)

        ## fsprep
        os.system('rm -f /opt/piCopilot-idrop/logs/probes.csv')
        os.system('rm -f /opt/piCopilot-idrop/logs/pipes.csv')

        ## Probes -n- pipes
        self.db.execute("""
                        copy allprobes to '/opt/piCopilot-idrop/logs/probes.csv' delimiter ',' csv header;
                        """)
        hdrs = ['x', 'y']
        with open('/opt/piCopilot-idrop/logs/pipes.csv', 'w') as oFile:
           csv_out = csv.writer(oFile,
                                delimiter = ',',
                                quotechar = '"',
                                quoting = csv.QUOTE_MINIMAL)
           csv_out.writerow(hdrs)
           for row in pipeList:
               csv_out.writerow(row)
