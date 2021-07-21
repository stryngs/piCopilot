# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
import os, time

class TELEMETRY(object):
    """Class for all things telemetry"""

    def __init__(self, mc):

        ## Grab our multiClass object
        self.mc = mc

        ## Call up our blueprint
        self.telemetry = Blueprint('telemetry',
                                   __name__,
                                   template_folder = 'templates')
###############################################################################



        ## Homepages ##
        @self.telemetry.route('/Telemetry')
        def index():
            return render_template('telemetry/index.html',
                                   serviceStatus = self.mc.svCheck('telemetry_Service'))
###############################################################################



        ## Configurations ##
        @self.telemetry.route('/Telemetry/Config')
        def telemetryConfig():
            return render_template('telemetry/config/telemetry-config.html')


        @self.telemetry.route('/Telemetry/Service-Config')
        def serviceConfig():
            """Start the service"""
            return render_template('telemetry/control/serviceControl.html',
                                   uChoice = ['On', 'Off'])
###############################################################################



        ## No-Click Functions ##
        @self.telemetry.route('/Telemetry/config-set', methods = ['POST'])
        def telemetrySet():
            return render_template('telemetry/index.html',
                                   serviceStatus = self.mc.svCheck('telemetry_Service'))


        @self.telemetry.route('/Telemetry/Service-Control', methods = ['POST'])
        def serviceControl():
            """Change the Telemetry Bridge Controls"""
            self.mc.telemetryServiceControl = request.form.get('buttonStatus')

            ## If the service is running and we turn off
            if self.mc.svCheck('telemetry_Service') == 'RUNNING':
                if self.mc.telemetryServiceControl == 'Off':
                    self.mc.svControl('stop', 'telemetry_Service')

            ## If the service is not running and we turn on
            else:
                if self.mc.telemetryServiceControl == 'On':
                    self.mc.svControl('start', 'telemetry_Service')

            return render_template('telemetry/index.html',
                                   serviceStatus = self.mc.svCheck('telemetry_Service'))


        @self.telemetry.route('/Telemetry/___Service-OFF')
        def serviceOFF():
            """Turn the Telemetry Off"""
            if self.mc.svCheck('telemetry_Service') == 'RUNNING':
                self.mc.svControl('stop', 'telemetry_Service')

            return render_template('telemetry/index.html',
                                   serviceStatus = self.mc.svCheck('telemetry_Service'))

        @self.telemetry.route('/Telemetry/___Service-ON')
        def serviceON():
            """Turn the Telemetry On"""
            if self.mc.svCheck('telemetry_Service') != 'RUNNING':
                self.mc.svControl('start', 'telemetry_Service')

            return render_template('telemetry/index.html',
                                   serviceStatus = self.mc.svCheck('telemetry_Service'))
