# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
import json
import os
import time
import sqlite3 as lite
import shutil
import subprocess

class VIDEO(object):
    """Class for all things video"""

    def __init__(self, mc):

        ## Grab our multiClass object
        self.mc = mc

        ## Call up our blueprint
        self.video = Blueprint('video',
                                __name__,
                                template_folder = 'templates')

###############################################################################



        ## Homepages ##
        @self.video.route('/Video-Info')
        def index():
            return render_template('video/index.html',
                                   logSize = self.mc.logSize(),
                                   bridgeStatus = self.mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   video_Type = 'HELLO')
###############################################################################

        ## Button pushes
        @self.video.route('/GStreamer_640x480')
        def gstreamerStart():

            ### Class this out
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'

            ## Stop GStreaner and Motion
            mc.videoStop()

            ## Start
            mc.svControl('start', 'gsPrep')
            return render_template('index.html',
                                   telem_Service = mc.svCheck('telemetry_Service'),
                                   system_bridgeStatus = mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   system_logSize = mc.logSize(),
                                   system_hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   video_Type = mc.svCheck('blah', True),
                                   hostNic = mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)


            ## video stopping
        @self.video.route('/videoStop')
        def videoStop():

            ## Stop GStreaner and Motion
            mc.videoStop()

            ### Class this out
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'
            return render_template('index.html',
                                   telem_Service = mc.svCheck('telemetry_Service'),
                                   system_bridgeStatus = mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   system_logSize = mc.logSize(),
                                   system_hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   video_Type = mc.svCheck('blah', True),
                                   hostNic = mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)


        @self.video.route('/GStreamer_800x600')
        def gstreamerStartII():

            ### Class this out
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'

            ## Stop GStreaner and Motion
            mc.videoStop()

            ## Start
            mc.svControl('start', 'gsPrepII')
            return render_template('index.html',
                                   telem_Service = mc.svCheck('telemetry_Service'),
                                   system_bridgeStatus = mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   system_logSize = mc.logSize(),
                                   system_hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   video_Type = mc.svCheck('blah', True),
                                   hostNic = mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)


        @self.video.route('/GStreamer_1280x720')
        def gstreamerStartIII():

            ### Class this out
            try:
                if mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'

            ## Stop GStreaner and Motion
            mc.videoStop()

            ## Start
            mc.svControl('start', 'gsPrepIII')
            return render_template('index.html',
                                   telem_Service = mc.svCheck('telemetry_Service'),
                                   system_bridgeStatus = mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                   system_logSize = mc.logSize(),
                                   system_hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                   video_Type = mc.svCheck('blah', True),
                                   hostNic = mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                   hostStatus = hostStatus)

        ## Configurations ##
        @self.video.route('/Video/Log-Delete')
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
                return render_template('system/index.html',
                                       logSize = self.mc.logSize(),
                                       bridgeStatus = self.mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                       hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"))


        @self.video.route('/Motion')
        def motionStart():

            ### Class this out
            try:
                if self.mc.hostAPD is True:
                    hostStatus = 'Active'
                else:
                    hostStatus = 'Inactive'
            except:
                hostStatus = 'Inactive'

            ## Stop GStreaner and Motion
            mc.videoStop()

            mc.svControl('start', 'motionPrep')
            return render_template('index.html',
                                telem_Service = mc.svCheck('telemetry_Service'),
                                system_bridgeStatus = mc.bashReturn('systemctl status apache2 | grep "Active:" | cut -d: -f2 | cut -d\( -f1'),
                                system_logSize = mc.logSize(),
                                system_hddAvail = mc.bashReturn("df -h | grep '/dev/root' | awk '{print $4}'"),
                                video_Type = mc.svCheck('blah', True),
                                hostNic = mc.bashReturn('grep interface /etc/hostapd/hostapd.conf').split('=')[1],
                                hostStatus = hostStatus)
###############################################################################




        ## No-Click Functions ##
        @self.video.route('/System/Log-Download')
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
