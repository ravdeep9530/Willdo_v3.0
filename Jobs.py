from include.Variable import __jobFile__,__stepsFile__,__connectionFile__,__jobQueue__,__jobCache__,__historyPath__,__guidePath__,__logPath__
from Generic import Generic
from Json_evaluation import Json_evaluation,log
from datetime import date,datetime,time
from operator import itemgetter
from ExecuteStep import ExecuteStep
from History import History

#job={{"name":"","conName":"","statement":"","interval":0,"scheuledTime":"","description":"","type":""}}
class Job:
    def setJob(job_dict,isNew=0,path=__guidePath__,histoyPath=__historyPath__,logPath=__logPath__):
        try:
            Json_evaluation.updateJson(job_dict,__jobFile__,path=path)
            if isNew==1:
                for x in job_dict.keys():
                    Json_evaluation.writeText(filename=str(x)+".txt",path=histoyPath,data=Generic.prefixTimeStamp("Job Created!!"))
                log("Adding "+str(job_dict.keys())+" Job",path=logPath)
            else:
                log("Update made on  "+str(job_dict.keys())+" Job",path=logPath)
                for x in job_dict.keys():
                    History.addJobHistory(filename=str(x+".txt"),path=histoyPath,data=Generic.prefixTimeStamp(str("Job has been updated!!")))


            pass
        except Exception as e:
            log("Error_Jobs_setJob@"+str(e),path=logPath)
    def addStep(jobName,step_dict,path=__guidePath__,logPath=__logPath__):
        try:
            Json_evaluation.updateJson(step_dict,__stepsFile__,path=path)
            log("Adding "+str(step_dict.keys())+" step under job "+jobName,path=logPath)
            pass
        except Exception as e:
            log("Error_Jobs_addStep@"+str(e))
    def evaluateJob():
        try:
            #step_data=Json_evaluation.readJSON(filename=__stepsFile__)
            return Json_evaluation.readJSON(filename=__jobFile__)
            #print(job_data["conName"])
            #con_data=Json_evaluation.readJSON(filename=__connectionFile__)
            #sjc_data={**step_data,**job_data,**con_data}
            #print(sjc_data)

            pass
        except Exception as e:
            log("Error_Job_evaluateJob@"+str(e))
    def prepareJobQueue():
        try:
            todayList={}
            data=Job.evaluateJob()
            #print(data)
            curDate=Generic.strToDate(Generic.getDate());
            curTime=Generic.strToTime(Generic.getTime());
            #print(curTime)
            for key in data.keys():
                timeKeyword=""
                lastRunDate=data[key]["lastRunDate"]
                if data[key]["lastRunDate"]=="-1":
                    timeKeyword="scheuledTime"
                else:
                    timeKeyword="nextRunTime"
                if Generic.strToDate(data[key]["startDate"])<=curDate and Generic.strToDate(data[key]["endDate"])>=curDate and (data[key]["isActive"]==1 or data[key]["isActive"]=="on")  and (lastRunDate=="-1" or Job.isJobEligibleToRun(int(data[key]["interval"]),curDate,curTime,data[key][timeKeyword])==1)  and Generic.strToTime(data[key][timeKeyword])>=curTime:
                    todayList[key]={"scheduledTime":data[key][timeKeyword],"remainingSec":Generic.timeDiff(Generic.getTime(),data[key][timeKeyword])}
                    #print(todayList)
            Json_evaluation.writeJSON(data=todayList,filename=__jobQueue__)
            log("Job Queue Prepared....")
        except Exception as e:
            log("Error_Jobs_prepareJobQueue@"+str(e))
    def getNearestJob():
        try:
            data=Json_evaluation.readJSON(filename=__jobQueue__)
            #print(data)
            jobCache=""
            curDate=Generic.strToDate(Generic.getDate());
            lesserTime=-1
            for key in data.keys():
                if lesserTime==-1 and  Generic.strToTime(data[key]["scheduledTime"])>=Generic.strToTime(Generic.getTime()):
                    lesserTime=data[key]["remainingSec"]
                    jobCache=key
                if lesserTime>int(data[key]["remainingSec"]) and Generic.strToTime(data[key]["scheduledTime"])>=Generic.strToTime(Generic.getTime()):
                    lesserTime=data[key]["remainingSec"]
                    jobCache=key
            return jobCache
        except Exception as e:
            log("Error_Jobs_getNearestJob@"+str(e))
    def getStepsByJob(job_name,path=__guidePath__):
        try:
            #print(job_name)
            steps=[]
            data=Json_evaluation.readJSON(filename=__stepsFile__,path=path)
            for key in data.keys():
                if str(key.split('|')[0]).strip()==str(job_name).strip():
                    steps.insert(int(data[key]["stepNo"]),key)
            return steps
        except Exception as e:
            log("Error_Jobs_getStepsByJob@"+str(e))
    def executeJob(job_name):
        try:
            steps=Job.getStepsByJob(job_name)
            for step in steps:
                #print(str(step))
                ExecuteStep.executeStep(str(step))
            Job.lastRunUpdate(job_name)
        except Exception as e:
            log("Error_Jobs_executeJob@"+str(e))
    def lastRunUpdate(jobName):
        try:
            data=Json_evaluation.getJsonByKey(filename=__jobFile__,key=jobName)
            data=Job.updateNextRun(data)
            data["lastRunDate"]=Generic.getDate()
            n_data={}
            n_data[jobName]=data#Next scheduled time update
            Json_evaluation.updateJson(dict=n_data,filename=__jobFile__)
            log("Job "+jobName+" last Run Updated!!")
        except Exception as e:
            log("Error_Jobs_lastRunUpdate@"+str(e))
    def validateJobName(jobName):
        try:
            data=Json_evaluation.getJsonByKey(filename=__jobFile__,key=jobName)

            if data!=-1:
                return 0
            return 1
            #log("Job "+jobName+" last Run Updated!!")
        except Exception as e:
            log("Error_Jobs_validateJobName@"+str(e))


    def isJobEligibleToRun(interval,curDate,curTime,lastRunDateTime):
        try:
            return 1 #Disabled this function in version 3.0!!
            if lastRunDateTime=="-1":
                return 1

            if interval<0:
                #print(Generic.strToTime(Generic.addTime(Generic.strToTime(lastRunDateTime),(-1*interval))))
                if Generic.strToTime(Generic.addTime(Generic.strToTime(lastRunDateTime),(-1*interval)))>=curTime:
                    return 1
            elif Generic.addDate(Generic.strToDate(lastRunDateTime),interval)>=curDate and interval>0:
                return 1
            else:
                return 0
        except Exception as e:
            log("Error_Jobs_isJobEligibleToRun@"+str(e)) 
            return 0

    def updateNextRun(jobData):
        try:
            interval=int(jobData["interval"])
            if jobData["lastRunDate"]=="-1":
                if interval<0:

                    jobData["nextRunTime"]=Generic.addTime(Generic.strToTime(jobData["scheuledTime"]),(-1*interval))
                    #print(jobData["nextRunTime"])
                    jobData["nextRunDate"]=Generic.getDate()

                else:
                    jobData["nextRunTime"]=jobData["scheuledTime"]
                    jobData["nextRunDate"]=Generic.dateToStr(Generic.addDate(Generic.strToDate(Generic.getDate()),interval))
            else:
                if interval<0:
    
                    jobData["nextRunTime"]=Generic.addTime(Generic.strToTime(jobData["nextRunTime"]),(-1*interval))
                    #print(jobData["nextRunTime"])
                    jobData["nextRunDate"]=Generic.getDate()
                else:
                    jobData["nextRunTime"]=jobData["scheuledTime"]
                    jobData["nextRunDate"]=Generic.dateToStr(Generic.addDate(Generic.strToDate(jobData["lastRunDate"]),interval))
            
            return jobData 
        except Exception as e:
            log("Error_Jobs_updateNextRun@"+str(e))
    


    #def prepareJobSteps(job_name):
        #steps[]

        #for job_data in data.keys():
            #if(data[job_name])



        #print(Generic.getDate())
