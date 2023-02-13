import subprocess
import time

class Multi(object):
    """Useful for passing information"""

    def __init__(self):
        pass


    def svCheck(self, bridge, listAll = False):
        """Check the status of the bridge"""

        if listAll is False:
            return subprocess.check_output('supervisorctl status {0}'.format(bridge),
                                           shell = True).decode().split()[1]
        else:
            motionPrep =  subprocess.check_output('supervisorctl status {0}'.format('motionPrep'),
                                                  shell = True).decode().split()[1]
            gsPrep =  subprocess.check_output('supervisorctl status {0}'.format('motionPrep'),
                                              shell = True).decode().split()[1]

            rString =  'motionPrep: {0} -- '.format(motionPrep)
            rString += 'gsPrep: {0}'.format(gsPrep)
            return rString



    def svControl(self, button, bridge):
        """Control the bridge"""
        subprocess.check_output('supervisorctl {0} {1}'.format(button, bridge),
                                shell = True)


    def logSize(self):
        """Return the total size of all logs for mavproxy"""
        return subprocess.check_output('du -h /opt/piCopilot-unmanned/modules/telemetry/myVehicle/ | tail -n 1 | cut -f1',
                                       shell = True).decode().strip()


    def bashReturn(self, cmd):
        """Return teh bash"""
        return subprocess.check_output(cmd,
                                       shell = True).decode().strip()


    def videoStop(self):
        """Hard stop on GStreamer or Motion"""
        try:
            self.bashReturn('killall -9 raspivid')
        except:
            pass
        try:
            self.bashReturn('systemctl stop motion')
            time.sleep(1)
            self.bashReturn('systemctl stop motioneye')
        except:
            pass
        time.sleep(1)
