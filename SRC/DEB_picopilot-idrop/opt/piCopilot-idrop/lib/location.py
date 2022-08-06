try:
    import gpsd
except:
    pass

class Location(object):

    def __init__(self):
        self.trigger = None
        try:
            gpsd.connect()
            self.gpsObj = gpsd
            self.trigger = True
        except:
            pass


    def getCoord(self):
        try:
            return self.gpsObj.get_current().position()
        except:
            return None
