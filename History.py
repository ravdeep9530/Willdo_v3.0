from include.Variable import __logPath__,__logFile__,__guidePath__,__connectionFile__,__historyPath__
from Generic import Generic
from Json_evaluation import log
class History:
    def addJobHistory(data,path=__historyPath__,filename=__logFile__):
        try:

            with open(path+'/'+filename, 'a') as txtfile:
                print(data, file=txtfile)
        except Exception as e:
            log("Error_History_addHistory"+str(e))
    def readJobHistory(path=__historyPath__,jobName="willdo"):
        try:
            with open(path+'/'+jobName+".txt", 'r') as txtfile:
                return txtfile.read()
        except Exception as e:
            log("Error_History_addHistory"+str(e))
