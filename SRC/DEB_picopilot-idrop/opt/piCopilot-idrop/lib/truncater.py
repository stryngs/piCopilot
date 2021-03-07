import os
import psycopg2
import sys

class Truncater(object):
    """All things sql export"""

    def __init__(self, shared):
        self.pgsqlConnect(shared)

    def pgsqlConnect(self, shared):
        ## Connects
        ### Need to fix this for config.ini purposes
        cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(shared.conf.db, shared.conf.user, shared.conf.host, shared.conf.password)
        self.con = psycopg2.connect(cStr)
        self.con.autocommit = True
        self.db = self.con.cursor()


    def truncate(self):
        ## Grab all tables, then truncateTables
        self.db.execute("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public';
                        """)
        tables = [i[0] for i in self.db.fetchall()]
        for table in tables:
            self.db.execute("""
                            TRUNCATE TABLE {0};
                            """.format(table))
