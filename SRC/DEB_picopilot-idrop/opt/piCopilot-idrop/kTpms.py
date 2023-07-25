#!/usr/bin/python3

"""
kTpms -- Sniff anything TPMS
"""

import ast
import os
import psycopg2
import sh
import time
from configparser import ConfigParser
from easyThread import Backgrounder


class Tpms(object):
    """A base class for handling tpms
    """
    def __init__(self):

        ## Static string for now --
        self.tString = 'rtl_433 -M level -f 315000000 -F json:log.json -T0 -R 110 -Y minlevel=-0.5'

        ## db creds
        class Foo(object):
            pass
        self.conf = Foo()
        parser = ConfigParser()
        parser.read('system.conf')
        self.conf.dbUser = parser.get('creds', 'dbUser')
        self.conf.dbPass = parser.get('creds', 'dbPass')
        self.conf.dbHost = parser.get('creds', 'dbHost')
        self.conf.dbName = parser.get('creds', 'dbName')
        self.conf.devid = int(parser.get('creds', 'devid'))
        self.conf.seenMax = int(parser.get('prop', 'seenMax'))

        ## Connect to the db
        self.con, self.db, self.dbName = self.pgsqlPrep()


    def pgsqlPrep(self):
        """ Connect and prep the pgsql db"""
        try:
            cStr = f"dbname='{self.conf.dbName}' user='{self.conf.dbUser}' host='{self.conf.dbHost}' password='{self.conf.dbPass}'"
            con = psycopg2.connect(cStr)
            con.autocommit = True
            db = con.cursor()

            ## db prep
            db.execute("""
                       CREATE TABLE IF NOT EXISTS tpms(dev_timestamp TIMESTAMPTZ,
                                                       model TEXT,
                                                       id TEXT,
                                                       status INT,
                                                       battery_ok INT,
                                                       counter INT,
                                                       failed TEXT,
                                                       pressure_kpa REAL,
                                                       temperature_c REAL,
                                                       freq1 REAL,
                                                       freq2 REAL,
                                                       rssi REAL,
                                                       snr REAL,
                                                       noise REAL);
                       """)
        except Exception as E:
            print (f'I am unable to connect to the database {self.conf.dbName}')
            print(E)
            sys.exit(1)
        return (con, db, self.conf.dbName)


def tpmsBackground(self):
    """Holds the instance of rtl_433
    Will be redone with a nicer shell in the future
    """
    os.system(tpms.tString)

if __name__ == '__main__':

    ## os prep
    try:
        os.remove('log.json')
    except:
        pass

    ## Grab tpms
    tpms = Tpms()

    ## Add our function to Backgrounder
    Backgrounder.theThread = tpmsBackground

    ## Instantiate using #s other than defaults
    bg = Backgrounder()

    ## Start the work
    bg.easyLaunch()

    ## Read the stream
    tail = sh.tail('-f', './log.json', _iter = True)
    while True:
        newTpms = tail.next()

        ## Evaluate output from rtl_433
        try:
            tLog = ast.literal_eval(newTpms)

            ### CLEARED HOT TO LOG
            try:

                ## Update the db
                tpms.db.execute(f"""
                                INSERT INTO tpms (dev_timestamp,
                                                  model,
                                                  id,
                                                  status,
                                                  battery_ok,
                                                  counter,
                                                  failed,
                                                  pressure_kpa,
                                                  temperature_c,
                                                  freq1,
                                                  freq2,
                                                  rssi,
                                                  snr,
                                                  noise)
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
                                                     %s,
                                                     %s,
                                                     %s,
                                                     %s);
                                         """, (tLog.get('time'),
                                               tLog.get('model'),
                                               tLog.get('id'),
                                               tLog.get('status'),
                                               tLog.get('battery_ok'),
                                               tLog.get('counter'),
                                               tLog.get('failed'),
                                               tLog.get('pressure_kPa'),
                                               tLog.get('temperature_C'),
                                               tLog.get('freq1'),
                                               tLog.get('freq2'),
                                               tLog.get('rssi'),
                                               tLog.get('snr'),
                                               tLog.get('noise')))
            except Exception as E:
                print('inner ~~', E)
        except Exception as E:
            print('outer ~~', E)

        print(tLog)
        print()
