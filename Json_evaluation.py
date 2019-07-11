import json
from include.Variable import __logPath__,__logFile__,__guidePath__,__connectionFile__
import datetime
class Json_evaluation:
    def writeJSON(data,path=__guidePath__,filename='text.json'):
        try:
            with open(path+'/'+filename, 'w') as txtfile:
                json.dump(data, txtfile)
        except Exception as e:
            log("Error_C_Json_evaluation_writeJson"+str(e))
    def writeText(data,path=__guidePath__,filename='text.txt'):
        try:
            with open(path+'/'+filename, 'w') as txtfile:
                print(data, file=txtfile)

        except Exception as e:
            log("Error_C_Json_evaluation_writeText"+str(e))
    def readJSON(path=__guidePath__,filename='text.json'):
        try:
            with open(path+'/'+filename, encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                return data
        except Exception as e:
            log("Error_C_Json_evaluation_readJson"+str(e))
            return -1
    def readFile(path=__logFile__):
        try:
            with open(path, 'r') as txtfile:
                return txtfile.read()
        except Exception as e:
            log("Error_History_addHistory"+str(e))
    def updateJson(dict,filename,path=__guidePath__):
        try:
            data=Json_evaluation.readJSON(filename=filename,path=path)
            #data = {"Con_1":{"server":"94.156.144.217","user":"hotel","password":"indian12","database":"hotels","charset":"utf8","port":3306,"use_unicode":"True"}}
            data.update(dict)
            Json_evaluation.writeJSON(data=data,filename=filename,path=path)

        except Exception as e:
            log("Error_C_Json_evaluation_updateJson@"+str(e))
    def removeJson(key,filename,path=__guidePath__):
        try:
            data=Json_evaluation.readJSON(filename=filename,path=path)
            #data = {"Con_1":{"server":"94.156.144.217","user":"hotel","password":"indian12","database":"hotels","charset":"utf8","port":3306,"use_unicode":"True"}}
            data.pop(key)
            Json_evaluation.writeJSON(data=data,filename=filename,path=path)

        except Exception as e:
            log("Error_C_Json_evaluation_removeJson@"+str(e))

    def getJsonByKey(path=__guidePath__,filename='text.json',key="Willdo"):
        try:

            data=Json_evaluation.readJSON(path=path,filename=filename)
            return data[key]
        except Exception as e:
            log("Error_C_Json_evaluation_getJsonKey"+str(e))
            return -1
    def rt():
        try:
            return "test"
        except Exception as e:
            log("Error_C_Json_evaluation_getJsonKey"+str(e))
            return -1

def log(data,path=__logPath__,filename=__logFile__):
    try:
        data=str(datetime.datetime.now())+"=>"+data
        with open(path+'/'+filename, 'a') as txtfile:
            print(data, file=txtfile)
    except Exception as e:
        log("Error_C_Json_evaluation_log"+str(e))

def clearLog(data="",path=__logPath__,filename=__logFile__):
    try:
        print(data,path)
        #data=str(datetime.datetime.now())+"=>"+data
        with open(path+'/'+filename, 'w') as txtfile:
            print(data, file=txtfile)
    except Exception as e:
        log("Error_C_clearLog"+str(e))
def getErrorLog(path=__logPath__,filename=__logFile__):
    try:
        
        #data=str(datetime.datetime.now())+"=>"+data
        resultDir={}
        fileData=Json_evaluation.readFile(path+"/"+filename)
        jobName=''
        for line in fileData.split('\n'):
            if 'Execution' in line:
                tJob=line.split('=>')
                jobName=tJob[1].split(' ')[0]

            if 'Error' in str(line):
                tempLine=line.split('=>')
                resultDir[tempLine[0]]={"jobName":jobName,"desp":tempLine[1]}
                jobName=''

        
        return resultDir
    except Exception as e:
        
        return {"":"None"}
        
        log("Error_C_getErrorLog"+str(e))
def getCurrentLog(path=__logPath__,filename=__logFile__):
    try:
        
        #data=str(datetime.datetime.now())+"=>"+data
        resultDir={}
        fileData=open(path+"/"+filename, "r")
        lines=fileData.readlines()
        fileData.close()
        fileLen=len(lines)
        for line in range(fileLen-5,fileLen):
            
            resultDir.update({lines[line]:""})
            
        
        return resultDir
    except Exception as e:
        
        return {"":"None"}
        
        log("Error_C_getErrorLog"+str(e))