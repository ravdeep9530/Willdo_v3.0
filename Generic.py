from  datetime import datetime,timedelta
import os
class Generic:
    def getDateTime():
        return datetime.now().strftime("%d/%m/%Y %H:%M")
    def getDate():
        return datetime.now().strftime("%d/%m/%Y")
    def getTime():
        return datetime.now().strftime("%H:%M")
    def strToDate(str):
        return datetime.strptime(str, "%d/%m/%Y")
    def strToTime(str):
        return datetime.strptime(str, "%H:%M")
    def addDate(date,days):
        return date+timedelta(days=int(days))
    def addTime(time,mins):
        time=time+timedelta(minutes=int(mins))
        return time.strftime("%H:%M")
    def dateToStr(date):
        return date.strftime("%d/%m/%Y")
    def currentTimestamp():
        return str(datetime.now())
    def timeDiff(time1,time2):
        t = 0
        format = '%H:%M'
        #print(time1,time2)
        #print(str(datetime.strptime(time2, format)-datetime.strptime(time1, format)))
        for u in str(datetime.strptime(time2, format)-datetime.strptime(time1, format)).split(':'):
            b=0
            try:
                b=int(u)
            except Exception as e:
                b=0
                pass
            t = 60 * t + b
        #print(t)
        return t
    def prefixTimeStamp(data,spreator="=>"):
        return Generic.currentTimestamp()+spreator+data
    def getOSvarsion():
        return str(os.sys.platform)[:3]
    def getPathConnector():
        pathConnector="/"
        if Generic.getOSvarsion()=="lin":
            pathConnector="/"
        else:
            pathConnector="\\"

        return pathConnector
    def getRemotePathConnector(remote_dict):
        pathConnector="/"
        if remote_dict['os']=="Liniux":
            pathConnector="/"
        else:
            pathConnector="\\"

        return pathConnector

    def getFileNameFromPath(actualPath):
        pathConnector=Generic.getPathConnector()
        path=actualPath.split(pathConnector)
        if len(path)>1:
            return path[len(path)-1]
        else:
            if pathConnector=="/":
                pathConnector="\\"
            else:
                pathConnector="/"
            path=actualPath.split(pathConnector)
        #print(path)
        return path[len(path)-1]
    def replaceConnectorInPath(path):
        return path.replace('/',Generic.getPathConnector())
    def getCurrentPath():
        return os.getcwd()
    def removeLastSperator(s):
        if s[-1:] in [",","|"]:
            return s[:-1]
        return s
