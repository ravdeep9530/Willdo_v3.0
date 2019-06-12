import sys
sys.path.insert(0,'../../')
import json
from flask import Flask,render_template,jsonify,request
from Json_evaluation import Json_evaluation,clearLog
from Jobs import Job
from include.Variable import __jobQueue__,__connectionFile__,__intervalFile__,__jobFile__,__driverFile__,__parameterFile__,__emailFile__,__syncFile__,__stepsFile__
from InsertConnection import insertConnection
from Parameter import Parameter
from Email import Email
from History import History
#from flask.ext.triangle import Triangle
app = Flask(__name__)
__path__="../../scheduler_guide"
__historyPath__="../../History"
__logPath__="../../Log"
#Triangle(app)
#jinja_options = app.jinja_options.copy()

#jinja_options.update(dict(
#    block_start_string='<%',
#    block_end_string='%>',
#    variable_start_string='%%',
#    variable_end_string='%%',
#    comment_start_string='<#',
#    comment_end_string='#>'
#))
#app.jinja_options = jinja_options

@app.route('/home')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
            return str(e), 500
@app.route('/getJobQueue')
def getJobQueue():
    #return ""
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__jobQueue__))
    except Exception as e:
            return str(e), 500
@app.route('/getActiveJobs')
def getActiveJobs():
    #return ""
    try:
        return jsonify(Job.getActiveJobs(path=__path__))
    except Exception as e:
            return str(e), 500
@app.route('/getConList')
def getConList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__connectionFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getIntervalList')
def getIntervalList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__intervalFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getDriverList')
def getDriverList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__driverFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getJobList')
def getJobList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__jobFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getParamList')
def getParamList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__parameterFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getEmailList')
def getEmailList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__emailFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getRemoteList')
def getRemoteList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__syncFile__))
    except Exception as e:
            return str(e), 500
@app.route('/clearLog')
def clearLog():
    try:
        clearLog(path=__logPath__)
        return "Log has been crealed!!!"
    except Exception as e:
            return str(e), 500
@app.route('/getStepList/<jobName>')
def getStepList(jobName):
    try:
        return jsonify(Job.getStepsByJob(jobName,path=__path__))
    except Exception as e:
            return str(e), 500
@app.route('/getStepParamList/<jobName>/<stepName>')
def getStepParamList(jobName,stepName):
    try:
        paramDetail=Parameter.getParamByJob(jobName,path=__path__)
        paramOption=Parameter.getParamOptions(stepName,path=__path__,logPath=__logPath__)
        data={}
        data['paramDetail']=paramDetail
        data['paramOption']=paramOption
        return jsonify(data)
    except Exception as e:
            return str(e), 500
@app.route('/getJson/<file>/<key>')
def getJson(file,key):
    try:
    #return ""
    #if file=='Jobs':
        if file=='history':
            return jsonify(History.readJobHistory(path=__historyPath__,jobName=key))
        elif file=='Log':
            return jsonify(Json_evaluation.readFile(path=__logPath__+"/log.txt"))
        else:
            return jsonify(Json_evaluation.getJsonByKey(key=str(key),path=__path__,filename=file+".json"))
    except Exception as e:
            return str(e), 500
@app.route('/submitForm/<formName>/<masterName>', methods=['POST'])
def submitForm(formName,masterName):
    if request.method=='POST':
        result_dict=request.form.to_dict(flat=True)
        for k in result_dict.keys():
            data=k.replace("'", "\"")
        data=json.loads(data)
        masterKey=data[masterName]
        data={masterKey:data}
        try:
            if formName=='Jobs':
                Job.setJob(data,isNew=1,path=__path__,histoyPath=__historyPath__,logPath=__logPath__)
                return "Job Added Successfully!!"
            elif formName=='JobUpdate':
                Job.setJob(data,isNew=0,path=__path__,histoyPath=__historyPath__,logPath=__logPath__)
                return "Job updated Successfully!!"
            elif formName=='newCon':
                insertConnection(data,path=__path__,logPath=__logPath__)
                return "Connection Created Successfully!!"
            elif formName=='updateCon':
                insertConnection(data,path=__path__,logPath=__logPath__)
                return "Connection updated Successfully!!"
            elif formName=='newParam':
                Parameter.addParam(data,path=__path__,logPath=__logPath__)
                return "Parameter created Successfully!!"
            elif formName=='updateParam':
                Parameter.addParam(data,path=__path__,logPath=__logPath__)
                return "Parameter updated Successfully!!"
            elif formName=='newEmail':
                Email.addSmpt(data,path=__path__,logPath=__logPath__)
                return "Email created Successfully!!"
            elif formName=='updateEmail':
                Email.addSmpt(data,path=__path__,logPath=__logPath__)
                return "Email updated Successfully!!"
            elif formName=='newStep':

                jobName=data[masterKey]["jobName"]
                data={str(data[masterKey]["jobName"]+"|"+data[masterKey]['stepName']):data[masterKey]}
                Job.addStep(str(jobName),data,path=__path__,logPath=__logPath__)
                return "Step updated Successfully under "+jobName+" !!"
            elif formName=='assigneParam':
                stepData=Json_evaluation.getJsonByKey(key=masterKey,filename=__stepsFile__,path=__path__)
                print(stepData)
                if str(stepData["parameter"])=="":
                    stepData["parameter"]=str(data[masterKey]['paramName'])+str(data[masterKey]['paramOption'])
                else:
                    stepData["parameter"]+="|"+str(data[masterKey]['paramName'])+str(data[masterKey]['paramOption'])
                stepData={masterKey:stepData}
                Json_evaluation.updateJson(dict=stepData,filename=__stepsFile__,path=__path__)
                return "Parameter Assined Successfully!!"
        except Exception as e:
            print(str(e))
        return "<h2>Success</h2>"

@app.route('/deleteJson/<fileName>/<key>')
def deleteJson(fileName,key):
    try:
        if fileName=='Jobs':
            Json_evaluation.removeJson(key=key,filename=__jobFile__,path=__path__)
            return "Job deleted Successfully!!"
        elif fileName=='Connections':
            Json_evaluation.removeJson(key=key,filename=__connectionFile__,path=__path__)
            return "Connection deleted Successfully!!"
        elif fileName=='Parameters':
            Json_evaluation.removeJson(key=key,filename=__parameterFile__,path=__path__)
            return "Parameter deleted Successfully!!"
        elif fileName=='Email':
            Json_evaluation.removeJson(key=key,filename=__emailFile__,path=__path__)
            return "Email SMTP deleted Successfully!!"
        elif fileName=='Step':
            Json_evaluation.removeJson(key=key,filename=__stepsFile__,path=__path__)
            return key+" Step deleted Successfully!!"
    except Exception as e:
            return str(e), 500

@app.route('/hello/<user>')
def hello_name(user):

   return render_template('index.html', name = user)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8000)
