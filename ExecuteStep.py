from Connections.sqlConn import connection,executeSql
import asyncio
import pymysql
from Json_evaluation import Json_evaluation,log
from include.Variable import __logPath__,__logFile__,__guidePath__,__connectionFile__,__stepsFile__,__jobFile__,__parameterFile__,__syncFile__
from History import History
from Generic import Generic
from Url import Url
from Email import Email
from Parameter import Parameter
from Sync import Sync
class ExecuteStep:
    def evaluateStep(step_name):
        try:
            step_data=Json_evaluation.getJsonByKey(key=step_name,filename=__stepsFile__)
            job_data=Json_evaluation.getJsonByKey(key=step_data["jobName"],filename=__jobFile__)
            con_data=Json_evaluation.getJsonByKey(key=job_data["conName"],filename=__connectionFile__)
            sjc_data={**step_data,**job_data,**con_data}
            #print(sjc_data)
            return sjc_data
            pass
        except Exception as e:
            log("Error_ExecuteStep_evaluateStep@"+str(e))

    async def executeStep(step_name):
        try:
            data=ExecuteStep.evaluateStep(step_name)
            
            try:
                params=[]
                try:
                    paramData,params=Parameter.getParamByStep(data)
                except Exception as e:
                    log("WARNING: Parameter is Empty with message ("+str(e)+")")
                if len(data)<1:
                    return ""
                #print(data)
                
                
                if int(data["stepType"])==1 or int(data["stepType"])==4:
                    if data["statement"]!="":
                        con=connection(data["conName"])
                        result=executeSql(con=con,q=str(data["statement"]),isProc=int(data["stepType"]))

                        if len(result)>0:
                            #print(result)
                            if len(paramData)>0:
                                param=Parameter.getParamValue(params,5)# store scalar value from resultset into parameter
                                if param!="-1":
                                    paramData[param]["paramValue"]=""
                                    for r in result:
                                        #print(r)
                                        paramData[param]["paramValue"]+=r[0]+"|"
                                    paramData_final={param[:-1]:paramData[param]}
                                    Json_evaluation.updateJson(dict=paramData_final,filename=__parameterFile__)
                                param=Parameter.getParamValue(params,6)# Store Row resultset into parameter
                                if param!="-1":
                                    paramData[param]["paramValue"]=""
                                    for r in result:
                                        for rr in r:
                                            paramData[param]["paramValue"]+=rr
                                        paramData[param]["paramValue"]+="|"
                                    paramData_final={param[:-1]:paramData[param]}
                                    Json_evaluation.updateJson(dict=paramData_final,filename=__parameterFile__)

                elif int(data["stepType"])==2:
                    #sprint(data["url"])
                    
                    url=data["url"]
                    
                    if len(paramData)>0:
                        param=str(Parameter.getParamValue(params,3))
                        if str(param)!="-1":
                            url=paramData[param]["paramValue"]
                            
                    filename=Url.callApi(url=url,filename="")
                    #print(filename)
                    if filename!="-1":
                        if len(paramData)>0:
                            param=Parameter.getParamValue(params,4)
                            if param!="-1":
                                paramData[param]["paramValue"]=filename
                                paramData_final={param[:-1]:paramData[param]}
                                Json_evaluation.updateJson(dict=paramData_final,filename=__parameterFile__)

                elif int(data["stepType"])==3:
                    emailAdditionMsgPart={"emailMsg":"","attachmentFilePath":""}
                    attachedFilePath=""
                    if len(paramData)>0:
                        param=Parameter.getParamValue(params,2)
                        #print(paramData[param])
                        if param!="-1":
                            attachedFilePath=paramData[param]["paramValue"]


                        param=Parameter.getParamValue(params,1)
                        if param!="-1":
                            paramVal=paramData[param]["paramValue"]
                            emailAdditionMsgPart["emailMsg"]=paramVal

                        #param=Parameter.getParamValue(params,9)
                        #if param!="-1":
                            #paramVal=paramData[param]["paramValue"]
                            #data["receiver_emails"]=paramVal

                    data={**data,**emailAdditionMsgPart}
                    for attach in Generic.removeLastSperator(attachedFilePath).split("|"):
                        data["attachmentFilePath"]=attach
                        Email.sendEmail(data)
                elif int(data["stepType"])==5:
                    #sprint(data["url"])
                    remoteName=data["remoteName"]
                    remotedict=Json_evaluation.getJsonByKey(filename=__syncFile__,key=remoteName)
                    if len(paramData)>0:
                        param=Parameter.getParamValue(params,7)
                        if param!="-1":
                            pData=paramData[param]["paramValue"]
                            intialFlag=0
                            for p in Generic.removeLastSperator(pData).split('|'):
                                #p=Generic.replaceConnectorInPath(p)
                                tempFileName=Sync.getFileFromRemote(remotedict,p,Generic.getFileNameFromPath(p))
                                #print(tempFileName)
                                param=Parameter.getParamValue(params,8)
                                if param!="-1":
                                    if intialFlag==0:
                                        paramData[param]["paramValue"]=""
                                        intialFlag=1
                                    paramData[param]["paramValue"]+=tempFileName+"|"
                                    paramData_final={param[:-1]:paramData[param]}
                                    Json_evaluation.updateJson(dict=paramData_final,filename=__parameterFile__)
                log("Execute Step "+step_name+" under JOB "+data["jobName"]+" With connection "+data["conName"])
                History.addJobHistory(filename=str(data["jobName"])+".txt",data=Generic.prefixTimeStamp(str("Success_Execute Step "+step_name+" under JOB "+data["jobName"]+" With connection "+data["conName"])))
            except Exception as e:
                History.addJobHistory(filename=str(data["jobName"])+".txt",data=Generic.prefixTimeStamp(str("Error_Execute Step "+step_name+" under JOB "+data["jobName"]+" With connection "+data["conName"])))
                log("Error_ExecuteStep_executeStep@"+str(e))
                pass
        except Exception as e:
            log("Error_ExecuteStep_executeStep@"+str(e))

    def validateStepName(jobName,stepName):
        try:
            data=Json_evaluation.getJsonByKey(filename=__stepsFile__,key=jobName+"|"+stepName)

            if int(data)!=-1:
                return 0
            return 1
            #log("Job "+jobName+" last Run Updated!!")
        except Exception as e:
            log("Error_ExecuteStep_validateJobName@"+str(e))
            return 0
