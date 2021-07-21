# -*- coding: utf-8 -*-

import json
import officeTasks as OT
import os
import time
import shutil
import subprocess
from lib.exporter import Exporter
from lib.truncater import Truncater
from lib.plotter import Plotter
from flask import Blueprint, render_template, request, send_file

class QUERY(object):
    """Class for all things Query"""

    def __init__(self, sh):

        ## Grab our shared object
        self.sh = sh

        self.exporter = Exporter(self.sh)
        self.truncater = Truncater(self.sh)
        self.plotter = Plotter(self.sh)


        ## Call up our blueprint
        self.query = Blueprint('query',
                                __name__,
                                template_folder = 'templates')

###############################################################################



        ## Homepage ##
        @self.query.route('/Queries')
        def index():
            #if sh.sysMode = 'None':

            return render_template('query/index.html',
                                   _kSnarf = self.sh.rlCheck('kSnarfPsql'),
                                   logSize = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                                   hddAvail = self.sh.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"))
###############################################################################



        ## Log deletion ##
        @self.query.route('/Query/Log-Delete')
        def logDelete():
            try:
                os.remove('/opt/piCopilot-idrop/downloads/logs.zip')
            except:
                pass
            shutil.rmtree('/opt/piCopilot-idrop/logs')
            os.mkdir('/opt/piCopilot-idrop/logs')
            os.system('chown -R postgres /opt/piCopilot-idrop/logs')
            os.system('chown -R postgres /opt/piCopilot-idrop/downloads')
            self.truncater.truncate()
            return render_template('query/index.html',
                                   _kSnarf = self.sh.rlCheck('kSnarfPsql'),
                                   logSize = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                                   hddAvail = sh.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"))
###############################################################################


        ## Log download ##
        @self.query.route('/Query/Log-Download_pgsql')
        def pgLogDownload():
            """Controls the download capabilities for pgsql"""
            try:
                os.remove('/opt/piCopilot-idrop/downloads/logs.zip')
            except Exception as E:
                print(E)
            self.exporter.pgsqlConnect()
            self.exporter.pgsqlExporter()
            self.exporter.con.close()
            shutil.make_archive('/opt/piCopilot-idrop/downloads/logs/', 'zip', root_dir='/opt/piCopilot-idrop/logs')

            ## fsprep
            #os.system('rm -f /opt/piCopilot-idrop/logs/pipes.csv')
            return send_file('/opt/piCopilot-idrop/downloads/logs.zip', as_attachment=True)
###############################################################################


        ## Visuals ##
        @self.query.route('/Query/visuals')
        def pgVisuals():
            """Create interactive visuals for pgsql"""
            OT.gnr.sweep('/opt/piCopilot-idrop/visuals', mkdir = True)
            self.plotter.probeReq(rType = 'max')
            self.plotter.probeReq(rType = 'min')
            self.plotter.lDir()
            return render_template('query/index.html',
                                   _kSnarf = self.sh.rlCheck('kSnarfPsql'),
                                   logSize = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                                   hddAvail = self.sh.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"))
