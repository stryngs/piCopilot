# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, send_file
import json
import os
import time
import sqlite3 as lite
import shutil
import subprocess

class SYSTEM(object):
    """Class for all things system"""

    def __init__(self, mc):

        ## Grab our multiClass object
        self.mc = mc

        ## Call up our blueprint
        self.system = Blueprint('system',
                                __name__,
                                template_folder = 'templates')

###############################################################################



        ## Homepages ##
        @self.system.route('/System-Info')
        def index():
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'
            return render_template('system/index.html',
                                   logSize = self.mc.logSize(),
                                   bridgeStatus = self.mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   hddAvail = self.mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   hostNic = self.mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)
###############################################################################

        @self.system.route('/System/hostWlan0')
        def hostWlan0():
            curStatus = self.mc.bashReturn('grep interface /etc/hostapd/hostapd.conf')
            if curStatus != 'interface=wlan0':
                self.mc.bashReturn("sed -i 's/interface=wlan1/interface=wlan0/' /etc/hostapd/hostapd.conf")
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'
            return render_template('system/index.html',
                                   logSize = self.mc.logSize(),
                                   bridgeStatus = self.mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   hddAvail = self.mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   hostNic = self.mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)


        @self.system.route('/System/hostWlan1')
        def hostWlan1():
            curStatus = self.mc.bashReturn('grep interface /etc/hostapd/hostapd.conf')
            if curStatus != 'interface=wlan1':
                self.mc.bashReturn("sed -i 's/interface=wlan0/interface=wlan1/' /etc/hostapd/hostapd.conf")
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'
            return render_template('system/index.html',
                                   logSize = self.mc.logSize(),
                                   bridgeStatus = self.mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   hddAvail = self.mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   hostNic = self.mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)


        @self.system.route('/System/Log-Delete')
        def logDelete():
            telem_status = self.mc.svCheck('telemetry_Service')
            if telem_status == 'RUNNING':
                return render_template('system/control/logDelete.html',
                                       action = 'deleted')
            else:
                try:
                    os.remove('/root/piController/templates/system/downloads/logs.zip')
                except:
                    pass
                shutil.rmtree('/root/piController/modules/telemetry/myVehicle')
                os.mkdir('/root/piController/modules/telemetry/myVehicle')
                try:
                    if mc.hostAPD is True:
                        hostStatus = 'Active'
                    else:
                        hostStatus = 'Inactive'
                except:
                    hostStatus = 'Inactive'
                return render_template('system/index.html',
                                    logSize = self.mc.logSize(),
                                    bridgeStatus = self.mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                    hddAvail = self.mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                    hostNic = self.mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                    hostStatus = hostStatus)


        @self.system.route('/System/Log-Download')
        def logDownload():
            """Controls the download capabilities"""
            telem_status = self.mc.svCheck('telemetry_Service')
            if telem_status == 'RUNNING':
                return render_template('system/control/logDelete.html',
                                       action = 'downloaded')
            else:
                try:
                    os.remove('/root/piController/templates/system/downloads/logs.zip')
                except:
                    pass
                shutil.make_archive('/root/piController/templates/system/downloads/logs', 'zip', root_dir='/root/piController/modules/telemetry/myVehicle')
                return send_file('/root/piController/templates/system/downloads/logs.zip', as_attachment=True)


        @self.system.route('/System/nicPrep')
        def nicPrep():
            """Sets wlan0 to the built-in NIC"""
            self.mc.bashReturn('bash /opt/piCopilot-scripts/nicPrep.sh')
            return ('System is rebooting')
