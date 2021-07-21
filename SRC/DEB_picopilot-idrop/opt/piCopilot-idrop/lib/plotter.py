import os
import psycopg2
import sys
import pandas as pd
import plotly.express as px
import officeTasks as OT


class Plotter(object):
    """All things sql export"""

    def __init__(self, shared):
        self.shared = shared
        self.pgsqlConnect()
        x, y = OT.gnr.fileMenu(fileType = 'html', mDir = '/opt/piCopilot-idrop/visuals')
        for i in y:
            OT.gnr.sweep(i)


    def lDir(self):
        x, y = OT.gnr.fileMenu(fileType = 'html', mDir = '/opt/piCopilot-idrop/visuals')
        iHtml = '<html>'
        with open('/opt/piCopilot-idrop/visuals/index.html', 'w') as oFile:
            for i in y:
                iHtml += '<a href="http://192.168.10.254:9090/{0}"</a>{0}</br>'.format(i)
            oFile.write(iHtml)


    def pgsqlConnect(self):
        """Connect to the db"""
        cStr = "dbname='{0}' user='{1}' host='{2}' password='{3}'".format(self.shared.conf.db, self.shared.conf.user, self.shared.conf.host, self.shared.conf.password)
        self.con = psycopg2.connect(cStr)
        self.con.autocommit = True
        self.db = self.con.cursor()


    def probeReq(self, rType = 'max'):
        """
        Flip the colors over to addr and see what it looks like



        probe requests by rType, rssi
        grouped by addr2_oui, addr2 and essid
        """
        self.db.execute("""
                        SELECT M.addr2_oui, P.addr2, P.essid, ARRAY_TO_STRING(ARRAY_AGG(M.rssi), ',') AS "rssis" FROM probes P INNER JOIN main M ON P.marker = M.marker GROUP BY M.addr2_oui, P.addr2, P.essid;
                        """)
        self.ourTuples = self.db.fetchall()
        if len(self.ourTuples) > 0:
            self.probeReqRssi_preDF = []
            if rType == 'max':
                rStr = 'rssi_max'
            else:
                rStr = 'rssi_min'
            for our in self.ourTuples:
                tList = our[3].split(',')
                rList = []
                for r in tList:
                    rList.append(int(r))
                if rType == 'max':
                    rVal = max(rList)
                else:
                    rVal = min(rList)
                lenR = len(tList)
                rAdjusted = (our[0], our[1], our[2], rVal, lenR)
                self.probeReqRssi_preDF.append(rAdjusted)
            hdrs = ['addr2_oui',
                    'addr2',
                    'essid',
                    rStr,
                    'rssi_len']
            df = pd.DataFrame(self.probeReqRssi_preDF, columns = hdrs)
            fig = px.scatter(df,
                             x = 'addr2_oui',
                             y = rStr,
                             color = 'essid',
                             size = 'rssi_len',
                             hover_name = 'addr2',
                             title = 'Probes by Addr - {0}'.format(rStr))
            with open('/opt/piCopilot-idrop/visuals/probeReqOui_{0}.html'.format(rStr), 'w') as oFile:
                oFile.write(fig.to_html())
            fig = px.scatter(df,
                             x = 'addr2',
                             y = rStr,
                             color = 'essid',
                             size = 'rssi_len',
                             hover_name = 'addr2_oui',
                             title = 'Probes by Addr - {0}'.format(rStr))
            with open('/opt/piCopilot-idrop/visuals/probeReqAddr_{0}.html'.format(rStr), 'w') as oFile:
                oFile.write(fig.to_html())


if __name__ == '__main__':
    class Foo(object):
        pass
    shared = Foo()
    shared.user = input('user?\n')
    shared.password = input('password?\n')
    shared.host = input('host?\n')
    shared.db = input('db?\n')
    s = Plotter(shared)
    s.probeReq(rType = 'max')
    s.probeReq(rType = 'min')
    s.lDir()
