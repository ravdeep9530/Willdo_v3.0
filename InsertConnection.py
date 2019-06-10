import sys
sys.path.insert(0,'include')
from include.Variable import __connectionFile__,__guidePath__,__logPath__
from Json_evaluation import Json_evaluation,log



def  insertConnection(con_dict,path=__guidePath__,logPath=__logPath__):
    try:
        Json_evaluation.updateJson(con_dict,filename=__connectionFile__,path=path)
        #data=Json_evaluation.readJSON(filename=__connectionFile__,path=path)
        #data = {"Con_1":{"server":"94.156.144.217","user":"hotel","password":"indian12","database":"hotels","charset":"utf8","port":3306,"use_unicode":"True"}}

        #data.update(con_dict)

        #Json_evaluation.writeJSON(data=data,filename=__connectionFile__,path=path)
        log("Adding "+str(con_dict.keys())+" Connetions",path=logPath)
        pass
    except Exception as e:
        print("Error_insertConnection_insertConnection@"+str(e))
def validateConName(conName):
    try:
        data=Json_evaluation.getJsonByKey(filename=__connectionFile__,key=conName)

        if int(data)!=-1:
            return 0
        return 1
        #log("Job "+jobName+" last Run Updated!!")
    except Exception as e:
        log("Error_insertConnection_validateJobName@"+str(e))
        return 0
