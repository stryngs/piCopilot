import subprocess
from configparser import ConfigParser

class Shared(object):
    """Shared idrop class"""

    def __init__(self, unity = None, conf = None):

        ## bring in the config file
        if conf is not None:
            self.conf = conf

        self.sysMode = 'None'
        if unity is not None:
            self.unity = unity


    def rlCheck(self, relay):
        """Check the status of the relay"""
        return subprocess.check_output('supervisorctl status {0}'.format(relay),
                                       shell = True).decode().split()[1]


    def rlControl(self, button, relay):
        """Control the relay"""
        self.sysMode = relay
        subprocess.check_output('supervisorctl {0} {1}'.format(button, relay),
                                shell = True)


    def bashReturn(self, cmd):
        """Cheap bash return"""
        return subprocess.check_output(cmd,
                                       shell = True).decode().strip()
