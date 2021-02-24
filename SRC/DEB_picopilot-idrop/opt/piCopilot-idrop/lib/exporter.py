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
        ### Need to fix this for config.ini purposes
        cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(self.shared.unity.db, self.shared.unity.user, self.shared.unity.host, self.shared.unity.password)
        self.con = psycopg2.connect(cStr)
        self.con.autocommit = True
        self.db = self.con.cursor()


    def pgsqlExporter(self):
        ## Tables
        self.db.execute("""
                        CREATE TEMPORARY TABLE allprobes AS
                        SELECT pi_timestamp, essid, subtype, addr2, addr1
                        FROM probes WHERE
                        subtype LIKE 'Probe %';
                        """)
        self.db.execute("""
                        CREATE TEMPORARY TABLE allds AS
                        SELECT pi_timestamp, addr2, addr1, addr3, addr4
                        FROM main WHERE type = 'Data'
                        AND (direc = 'from-ds' OR direct = 'to-ds');
                        """)

        ## Pipe logics
        ### Broken logic because we changed how to/from-ds works
        ###self.db.execute("""
        ###                CREATE TEMPORARY TABLE fd AS
        ###                SELECT pi_timestamp, addr1, addr3
        ###                FROM main WHERE type = 'Data'
        ###                AND direc = 'from-ds';
        ###                """)
        ###self.db.execute("""
        ###                SELECT * FROM fd;
        ###                """)
        ###fromRows = set(self.db.fetchall())
        ###self.db.execute("""
        ###                SELECT * FROM tods;
        ###                """)
        ###toRows = set(self.db.fetchall())
        ###pipeList = list(fromRows & toRows)

        ## fsprep
        os.system('rm -f /opt/piCopilot-idrop/logs/probes.csv')
        os.system('rm -f /opt/piCopilot-idrop/logs/ds.csv')
#        os.system('rm -f /opt/piCopilot-idrop/logs/pipes.csv')

        ## Outputs
        self.db.execute("""
                        copy allprobes to '/opt/piCopilot-idrop/logs/probes.csv' delimiter ',' csv header;
                        """)
        self.db.execute("""
                        copy allds to '/opt/piCopilot-idrop/logs/ds.csv' delimiter ',' csv header;
                        """)

        ### Broken til a new query is created
        ###hdrs = ['date', 'x', 'y']
        ###with open('/opt/piCopilot-idrop/logs/pipes.csv', 'w') as oFile:
        ###    csv_out = csv.writer(oFile,
        ###                         delimiter = ',',
        ###                         quotechar = '"',
        ###                         quoting = csv.QUOTE_MINIMAL)
        ###    csv_out.writerow(hdrs)
        ###    for row in pipeList:
        ###        csv_out.writerow(row)
