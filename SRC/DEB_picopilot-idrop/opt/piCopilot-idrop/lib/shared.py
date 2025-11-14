import subprocess
import os
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
        return os.popen(f'supervisorctl status {relay}').read().split()[1]


    def rlControl(self, button, relay):
        """Control the relay"""
        self.sysMode = relay
        os.psopen(f'supervisorctl {button} {relay}')


    def bashReturn(self, cmd):
        """Cheap bash return"""
        return os.popen(f'{cmd}').read().strip()

