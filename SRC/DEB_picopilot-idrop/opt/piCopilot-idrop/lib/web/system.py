# -*- coding: utf-8 -*-
import os
#import RPi.GPIO as GPIO
import subprocess
import time
from datetime import datetime
from flask import Blueprint, render_template, request

class SYSTEM(object):
    """Class for all things idrop or Pi Shutdown/Reboot"""

    def __init__(self, sh):

        ## Grab our shared object
        self.sh = sh

        ## Set mode to board and prep
        #GPIO.setmode(GPIO.BOARD)
        #GPIO.setup(23, GPIO.OUT)

        ## Cheap monitor
        self.monMode = None

        ## Get our blueprint
        self.system = Blueprint('system',
                                   __name__,
                                   template_folder = 'templates')
###############################################################################



        ## Homepages ##
        @self.system.route('/System')
        def index():
            """Start the service"""
            return render_template('system/control/index.html',
                                   uChoice = ['On', 'Off'])
###############################################################################


        ## No-Click Functions ##
        @self.system.route('/System/Service-Control', methods = ['POST'])
        def serviceControl():
            """Change the idrop system Relay Controls"""

            self.sh.systemServiceControl = request.form.get('buttonStatus')

            ## If the service is running and we turn off
            if self.sh.rlCheck('kSnarfPsql') == 'RUNNING':

                ### Really need to add more mature logic.  This is just to get us running with psql
                if self.sh.systemServiceControl == 'Off':
                    self.sh.rlControl('stop', 'kSnarfPsql')
                    #GPIO.output(23, GPIO.LOW)


                    ## Cheap way to snipe kSnarf as it is hanging
                    kPID = str(self.sh.bashReturn("ps aux | grep kSnar[f] | awk '{print $2}'"))
                    print ('OUR kSnarf PID IS {0}'.format(str(kPID)))
                    print ('OUR kSnarf PID IS TYPE {0}'.format(str(type(kPID))))
                    try:
                        self.sh.bashReturn("kill -9 %s" % kPID)
                    except:
                        time.sleep(2)
                        try:
                            self.sh.bashReturn("kill -9 %s" % kPID)
                        except:
                            pass
                        pass

            ## If the service is not running and we turn on
            else:

                ## Check for monitor mode
                if self.monMode is None:
                    self.sh.rlControl('start', 'nicMon')
                    self.monMode = True

                ## Check for listen mode psql
                if self.sh.systemServiceControl == 'On':
                    self.sh.rlControl('start', 'kSnarfPsql')
                    #GPIO.output(23, GPIO.HIGH)

            return render_template('system/index.html',
                                   serviceStatus = self.sh.rlCheck(self.sh.sysMode))
