from Json_evaluation import Json_evaluation,log
from include.Variable import __parameterFile__,__guidePath__,__logPath__,__stepsFile__,__paramOptionFile__
import smtplib, ssl
class Parameter:
    def addParam(param_dict,path=__guidePath__,logPath=__logPath__):
        try:
            Json_evaluation.updateJson(dict=param_dict,filename=__parameterFile__,path=path)
            log("Adding "+str(param_dict.keys())+" Parameter ",path=logPath)
            pass
        except Exception as e:
            log("Error_Parameter_addParam@"+str(e))
    def getParamByJob(jobName,path=__guidePath__):
        try:
            data=Json_evaluation.readJSON(filename=__parameterFile__,path=path)
            params=[]
            for key in data.keys():
                if data[key]["jobName"]==jobName:
                    params.insert(0,key)
            return params
        except Exception as e:
            log("Error_Parameter_getParamByJob@"+str(e))
    def updateParamValue(paramName="Willdo",value=""):
        try:
            data=Json_evaluation.getJsonByKey(key=paramName,filename=__parameterFile__)
            data["paramValue"]=value
            data={paramName:data}
            Json_evaluation.updateJson(dict=data,filename=__parameterFile__)
        except Exception as e:
            log("Error_Parameter_updateParamValue@"+str(e))
    def getParamByStep(data):
        try:
            paramData={}
            if len(data["parameter"])>0:
                params=data["parameter"].split('|')

                paramFlag=1
                if len(params)>1:
                    for key in params:
                        paramDataTemp=Json_evaluation.getJsonByKey(filename=__parameterFile__,key=key[:-1])
                        paramData[key]=paramDataTemp

                else:
                    paramDataTemp=Json_evaluation.getJsonByKey(filename=__parameterFile__,key=params[0][:-1])
                    paramData={params[0]:paramDataTemp}
            return paramData,params

        except Exception as e:
            log("Error_Parameter_getParamByStep@"+str(e))
    def getParamValue(data,subType):
        try:

            for key in data:

                if int(key[-1:])==subType:
                    return key
            return "-1"
        except Exception as e:
            log("Error_Parameter_getParamValue@"+str(e))
    def getParamOptions(stepName,path=__guidePath__,logPath=__logPath__):
        try:
            #data=Json_evaluation.getJsonByKey(key=stepName,filename=__stepsFile__,path=path)
            optionData={}
            paramOptionData=Json_evaluation.readJSON(filename=__paramOptionFile__,path=path)
            stepData=Json_evaluation.getJsonByKey(key=stepName,filename=__stepsFile__,path=path)
            stepType=stepData['stepType']
            for paramKey in paramOptionData.keys():
                if str(paramOptionData[paramKey]['stepType']) in stepType:
                    optionData[paramOptionData[paramKey]['name']]=paramKey


            
            return optionData
        except Exception as e:
            log("Error_Parameter_getParamOptions@"+str(e))
            return "-1"
