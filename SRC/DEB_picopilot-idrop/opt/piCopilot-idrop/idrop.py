#!/usr/bin/python3

import os
from configparser import ConfigParser
from flask import current_app
from flask import Flask
from flask import render_template
from lib.shared import Shared
from lib.timer import Timer
from lib.unifier import Unify
from lib.web.system import SYSTEM
from lib.web.query import QUERY
from lib.web.blue import BLUE

app = Flask(__name__)

## Homepages ##
@app.route('/')
def index():

    i1 = "iwlist {0} channel | grep Current | ".format(sh.conf.nic)
    i2 = "awk '{print $5}' | cut -d\) -f1| tail -n 1"
    iStr = i1 + i2
    try:
        usbHDD = sh.bashReturn("df -h /mnt/usb_storage/ | grep 'usb_storage'")
    except:
        usbHDD = None

    if sh.sysMode == 'None':
        return render_template('index.html',
                               kBlue_Service = sh.rlCheck('kBlue'),
                               system_Service = sh.sysMode,
                               system_Mode = 'None',
                               system_Channel = sh.bashReturn(iStr),
                               query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                               system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                               usb_hddAvail = usbHDD,
                               system_Time = sh.bashReturn("date"))
    if sh.sysMode == 'kSnarfPsql':
        return render_template('index.html',
                               kBlue_Service = sh.rlCheck('kBlue'),
                               system_Service = sh.sysMode,
                               system_Mode = sh.rlCheck('kSnarfPsql'),
                               system_Channel = sh.bashReturn(iStr),
                               query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                               system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                               usb_hddAvail = usbHDD,
                               system_Time = sh.bashReturn("date"))
    if sh.sysMode == 'Off':
        return render_template('index.html',
                               kBlue_Service = sh.rlCheck('kBlue'),
                               system_Service = sh.sysMode,
                               system_Mode = 'Off',
                               system_Channel = sh.bashReturn(iStr),
                               query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                               system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                               usb_hddAvail = usbHDD,
                               system_Time = sh.bashReturn("date"))

    if sh.sysMode == 'kBlue':
        return render_template('index.html',
                               kBlue_Service = sh.rlCheck('kBlue'),
                               system_Service = sh.sysMode,
                               system_Mode = sh.sysMode,
                               system_Channel = sh.bashReturn(iStr),
                               query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                               system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                               usb_hddAvail = usbHDD,
                               system_Time = sh.bashReturn("date"))

    ## Unexpected prep
    return render_template('index.html',
                           kBlue_Service = sh.rlCheck('kBlue'),
                           system_Service = sh.sysMode,
                           system_Mode = sh.sysMode,
                           system_Channel = sh.bashReturn(iStr),
                           query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                           system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                           usb_hddAvail = usbHDD,
                           system_Time = sh.bashReturn("date"))
###############################################################################



## Static files
@app.route('/jquery-3.1.1.min.js')
def jquery():
    return current_app.send_static_file('jquery-3.1.1.min.js')
###############################################################################

## No sub btns
@app.route('/timer')
def timeClick():
    sh.tmr.tMark()
    i1 = "iwlist {0} channel | grep Current | ".format(sh.conf.nic)
    i2 = "awk '{print $5}' | cut -d\) -f1| tail -n 1"
    iStr = i1 + i2
    return render_template('index.html',
                           kBlue_Service = sh.rlCheck('kBlue'),
                           system_Service = sh.sysMode,
                           system_Mode = 'None',
                           system_Channel = sh.bashReturn(iStr),
                           query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                           system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                           usb_hddAvail = usbHDD,
                           system_Time = sh.bashReturn("date"))

@app.route('/NICprep')
def nicPrep():
    sh.rlControl('start', 'nicPrep')

@app.route('/TIMEsync')
def timeSync():
    i1 = "iwlist {0} channel | grep Current | ".format(sh.conf.nic)
    i2 = "awk '{print $5}' | cut -d\) -f1| tail -n 1"
    iStr = i1 + i2

    ### DEBUG
    ## Modify as needed if not running in a conventional setup
    os.system('/bin/bash /opt/piCopilot-scripts/timeSync.sh')

    return render_template('index.html',
                           kBlue_Service = sh.rlCheck('kBlue'),
                           system_Service = sh.sysMode,
                           system_Mode = 'None',
                           system_Channel = sh.bashReturn(iStr),
                           query_Exports = sh.bashReturn("du -h /var/lib/postgresql/11/main | tail -n 1 | awk '{print $1}'"),
                           system_hddAvail = sh.bashReturn("df -h | grep '/dev/root'"),
                           usb_hddAvail = usbHDD,
                           system_Time = sh.bashReturn("date"))

###############################################################################

if __name__ == '__main__':

    ## Gen an empty class to pass around
    class Foo(object):
        pass

    ## Setup
    conf = Foo()
    parser = ConfigParser()
    parser.read('system.conf')
    conf.user = parser.get('creds', 'dbUser')
    conf.password = parser.get('creds', 'dbPass')
    conf.host = parser.get('creds', 'dbHost')
    conf.db = parser.get('creds', 'dbName')
    conf.nic = parser.get('hw', 'nic')
    sh = Shared(conf = conf)

    ## Setup timer and link to shared
    tmr = Timer(conf.db, conf.user, conf.host, conf.password)
    sh.tmr = tmr

    ## Instantiate needed classes
    systemClass = SYSTEM(sh)
    system = systemClass.system

    queryClass = QUERY(sh)
    query = queryClass.query

    blueClass = BLUE(sh)
    blue = blueClass.blue

    ## Register children
    app.register_blueprint(system)
    app.register_blueprint(query)
    app.register_blueprint(blue)


    ## Launch app
    app.run(debug = False, host = '0.0.0.0', port = 8001, threaded = True)
