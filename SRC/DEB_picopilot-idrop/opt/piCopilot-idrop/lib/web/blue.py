# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request
import os, time

import RPi.GPIO as GPIO
import subprocess
from datetime import datetime
import time

class BLUE(object):
    """Class for all things bluetooth"""

    def __init__(self, sh):

        ## Grab our shared object
        self.sh = sh

        ## Set mode to board and prep                                           ## Determine blue LED later on
        # GPIO.setmode(GPIO.BOARD)
        # GPIO.setup(23, GPIO.OUT)

        ## Get our blueprint
        self.blue = Blueprint('blue',
                                   __name__,
                                   template_folder = 'templates')
###############################################################################



        ## Homepages ##
        @self.blue.route('/kBlue')
        def index():
            """Start the service"""
            return render_template('blue/control/index.html',
                                   uChoice = ['On', 'Off'])
###############################################################################

        @self.blue.route('/kBlue/Service-Control', methods = ['POST'])
        def serviceControl():
            """Change the kBlue system Relay Controls"""

            self.sh.systemServiceControl = request.form.get('buttonStatus')

            ## If the service is running and we turn off
            if self.sh.rlCheck('kBlue') == 'RUNNING':

                if self.sh.systemServiceControl == 'Off':
                    self.sh.rlControl('stop', 'kBlue')
                    # GPIO.output(23, GPIO.LOW)

                    ## Cheap way to snipe kBlue if it hangs
                    kPID = str(self.sh.bashReturn("ps aux | grep kBlu[e] | awk '{print $2}'"))
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

                ## Check for On
                if self.sh.systemServiceControl == 'On':
                    self.sh.rlControl('start', 'kBlue')
                    # GPIO.output(23, GPIO.HIGH)

            return render_template('blue/index.html',
                                   kBlue_Service = sh.rlCheck('kBlue'))
