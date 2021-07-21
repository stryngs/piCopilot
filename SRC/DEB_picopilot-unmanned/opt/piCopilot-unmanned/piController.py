#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import current_app, Flask, render_template, request
from lib.shared import Multi
from lib.web.telemetry import TELEMETRY
from lib.web.system import SYSTEM
from lib.web.video import VIDEO
import subprocess

## Homepages ##
app = Flask(__name__)
@app.route('/')
def index():

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
###############################################################################



## Static files
@app.route('/jquery-3.1.1.min.js')
def jquery():
    return current_app.send_static_file('jquery-3.1.1.min.js')
###############################################################################

if __name__ == '__main__':
    ## Setup libs
    mc = Multi()

    ## Determine if hostapd in use
    mc.hostAPD = False
    with open('/etc/network/interfaces.d/wlan0', 'r') as iFile:
        p = iFile.read().splitlines()
    for i in p:
        if '#' in i:
            mc.hostAPD = True
            break

    ## set mc vars
    mc.system_bridgeStatus = None
    mc.system_logSize = None

    ## Instantiate needed classes
    telemClass = TELEMETRY(mc)
    telemetryObj = telemClass.telemetry
    systemClass = SYSTEM(mc)
    systemObj = systemClass.system
    videoClass = VIDEO(mc)
    videoObj = videoClass.video

    ## Register children
    app.register_blueprint(telemetryObj)
    app.register_blueprint(systemObj)
    app.register_blueprint(videoObj)

    ## Launch app
    app.run(debug = False, host = '0.0.0.0', port = 8000, threaded = True)
