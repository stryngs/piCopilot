#!/usr/bin/python3

import officeTasks as OT
import psycopg2
import time
from datetime import datetime, timedelta

if __name__ == '__main__':
    ## Grab current time based off the last hour
    tNow = datetime.today()
    tThen = tNow - timedelta(hours=72, minutes=0)

    ## SQL connect
    print('Grabbing info')
    cStr = "dbname='idrop' user='root' host='127.0.0.1' password='idrop'"
    con = psycopg2.connect(cStr)
    con.autocommit = True
    db = con.cursor()

    ## Grab list of all known MACs transmitting within the given time period
    ### Deal with rssi bug
    db.execute("""
               SELECT addr2, rssi, channel FROM main WHERE pi_timestamp BETWEEN '{0}' AND '{1}' AND direc = '00' AND rssi IS NOT NULL
               UNION ALL
               SELECT addr2, rssi, channel FROM main WHERE pi_timestamp BETWEEN '{0}' AND '{1}' AND direc = '01' AND rssi IS NOT NULL
               UNION ALL
               SELECT addr4, rssi, channel FROM main WHERE pi_timestamp BETWEEN '{0}' AND '{1}' AND direc = '11' AND rssi IS NOT NULL;
               """.format(tThen.strftime('%Y-%m-%d %H:%M:%S'), tNow.strftime('%Y-%m-%d %H:%M:%S')))
    res = db.fetchall()

    ## Notate MAC set
    macList = [i[0] for i in res]
    macList = list(set(macList))

    ## Track RSSIs based on high and low for TX
    cDict = {}

    ## Iterate through res and get high/low rssi for a given MAC
    for mac, rssi, channel in res:
        mCur = cDict.get(mac)
        if mCur is None:
            cDict.update({mac: ([rssi], [channel])})
        else:
            tList = cDict.get(mac)
            cDict.update({mac: (tList[0] + [rssi], tList[1] + [channel])})

    ## Find likely RSSI set
    vMac = []
    vDict = {}
    for k, v in cDict.items():
        nDict = {}
        rssiList = v[0]
        chanList = v[1]

        ## Iterate over rssis for chan to dict
        cnt = 0
        for rssi in rssiList:

            ## Check for current channel existing in nDict
            cVal = nDict.get(chanList[cnt])
            if cVal is not None:
                nDict.update({chanList[cnt]: cVal + [rssiList[cnt]]})
            else:
                nDict.update({chanList[cnt]: [rssiList[cnt]]})
            cnt += 1

            ## Rip through nDict and determine the realistic channel
            nFinal = {}

            closeToFarList = []
            for k1, v1 in nDict.items():
                nFinal.update({sum(v1) / len(v1): k1})

            likelyRSSIs = nFinal.get(max([i for i in nFinal.keys()]))
            vMac.append(nDict)

            ## close, far, avg, skew, total length
            vDict.update({k: (max(nDict.get(likelyRSSIs)),
                              min(nDict.get(likelyRSSIs)),
                              int(sum(nDict.get(likelyRSSIs)) / len(nDict.get(likelyRSSIs))),
                              max(nDict.get(likelyRSSIs)) - min(nDict.get(likelyRSSIs)),
                              len(nDict.get(likelyRSSIs)))})

    ## Outputs
    vList = []
    tRange = tThen.strftime('%Y-%m-%d %H:%M:%S') + ' ' + tNow.strftime('%Y-%m-%d %H:%M:%S')
    tStore = tRange.replace(' ', '').replace(':', '_').replace('-', '_')
    print(tRange)
    hdrs = ['tRange', 'mac', 'close', 'far', 'avg', 'skew', 'count']
    for k, v in vDict.items():
        # print(k, v)
        vList.append(((tRange, k) + tuple([i for i in v])))
    OT.csv.csvGen('tmp.csv', hdrs, vList)
    con = OT.csv.csv2sql('tmp.csv', tStore, 'baseline.sqlite3')
    con.close()

    print('./baseline.sqlite3 created!')
    # OT.gnr.sweep('tmp.csv')

    ### Next steps
    ## Cycle this data into idrop
