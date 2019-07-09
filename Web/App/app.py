import sys
sys.path.insert(0,'../../')
import json
from flask import Flask,render_template,jsonify,request,redirect,make_response,url_for
from Json_evaluation import Json_evaluation,clearLog
from Jobs import Job
from include.Variable import __jobQueue__,__connectionFile__,__schedulerTimeStampFile__,__intervalFile__,__jobFile__,__driverFile__,__parameterFile__,__emailFile__,__syncFile__,__stepsFile__
from InsertConnection import insertConnection
from Parameter import Parameter
from Email import Email
from History import History
from Sync import Sync
from Url import Url
import urllib.request
from flask_jwt import JWT, jwt_required, current_identity
#from flask.ext.triangle import Triangle
app = Flask(__name__)
__path__="../../scheduler_guide"
__historyPath__="../../History"
__logPath__="../../Log"
app.config['JWT_AUTH_HEADER_PREFIX']="JWT"
app.config["Authorization"]=""
app.config['SECRET_KEY'] = 'super-secret'
USER_DATA = {
    "masnun": "abc123"
}


class User(object):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return "User(id='%s')" % self.id

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

@app.route('/authenticateSSO')
def authenticateSSO():
    hash=request.args.get('hash') 
    validateUrl=request.args.get('validateUrl') 
    #return  validateUrl 
    data=json.loads(Url.urlRequest(validateUrl).read())
    
    if data["data"][0]["isLive"]==False:
        return redirect('http://localhost:8080/getNextPage/0/?toast=SSO Session is expired. Please Login again.')
    
    else:
        newConditions = {"username":"masnun","password":"abc123"} 
        params = json.dumps(newConditions).encode('utf8')
        req = urllib.request.Request("http://localhost:8000/auth", data=params,
                             headers={'content-type': 'application/json'})
        response = urllib.request.urlopen(req)
        data=response.read().decode('utf-8')
        data=json.loads(data)
        resp=jsonify()
        #return data["access_token"]
        #resp.headers("Authorization","JWT "+data["access_token"])
        #resp.location(url_for('protected'))
        r=make_response(redirect('/home'))
        #app.config["Authorization"]="JWT "+data["access_token"].strip()
        #r.headers["Content-Type"]="application/json"
        #r.headers["Authorization"]=app.config["Authorization"].encode('utf-8')
        r.set_cookie('Authorization', str('JWT '+data["access_token"].strip()))#.encode('utf-8'))
        #r.headers["Cdd"]="applicatio"
        return r#edirect('/protected',code=302)
    return jsonify(data["data"][0]["isLive"])
    pass
@app.after_request
def apply_caching(response):
    #response.headers["Content-Type"]="application/json"
    #response.headers["Authorization"]=app.config["Authorization"].encode('utf-8')
    #response.headers['Access-Control-Allow-Origin'] = '*'
    return response




def verify(username, password):
    if not (username and password):
        return False
    if USER_DATA.get(username) == password:
        return User(id=123)
def identity(payload):
    user_id = payload['identity']
    print(user_id)
    return {"id": user_id}
jwt = JWT(app, verify, identity)
@app.route('/protected')
#@jwt_required()
def protected():
    
    return '%s' % current_identity
@app.route('/home')

def home():
    try:
        print(request.headers.get('Authorization'))
        return render_template('index.html')
    except Exception as e:
            return str(e), 500
@app.route('/getJobQueue')
@jwt_required()
def getJobQueue():
    #return ""
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__jobQueue__))
    except Exception as e:
            return str(e), 500
@app.route('/getActiveJobs')
@jwt_required()
def getActiveJobs():
    #return ""
    try:
        return jsonify(Job.getActiveJobs(path=__path__))
    except Exception as e:
            return str(e), 500
@app.route('/getConList')
@jwt_required()
def getConList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__connectionFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getIntervalList')
@jwt_required()
def getIntervalList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__intervalFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getDriverList')
@jwt_required()
def getDriverList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__driverFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getJobList')
@jwt_required()
def getJobList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__jobFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getParamList')
@jwt_required()
def getParamList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__parameterFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getEmailList')
@jwt_required()
def getEmailList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__emailFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getRemoteList')
@jwt_required()
def getRemoteList():
    try:
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__syncFile__))
    except Exception as e:
            return str(e), 500
@app.route('/getSchedulerDetail')
@jwt_required()
def getSchedulerDetail():
    try:
        remoteDict=Json_evaluation.getJsonByKey(filename=__syncFile__,key="susServer",path=__path__)
        Sync.getSchedulerStatus(remoteDict,path=__path__,logPath=__logPath__)
        return jsonify(Json_evaluation.readJSON(path=__path__,filename=__schedulerTimeStampFile__))
    except Exception as e:
            return str(e), 500
@app.route('/clearLog')
@jwt_required()
def clearLog():
    try:
        clearLog(path=__logPath__)
        return "Log has been crealed!!!"
    except Exception as e:
            return str(e), 500
@app.route('/getStepList/<jobName>')
@jwt_required()
def getStepList(jobName):
    try:
        return jsonify(Job.getStepsByJob(jobName,path=__path__))
    except Exception as e:
            return str(e), 500
@app.route('/getStepParamList/<jobName>/<stepName>')
@jwt_required()
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
@app.route('/getInbuitParamList/<stepName>')
@jwt_required()
def getInbuitParamList(stepName):
    try:
        return jsonify(Parameter.getInbuiltParam(stepName,path=__path__))
    except Exception as e:
            return str(e), 500
@app.route('/getJson/<file>/<key>')
@jwt_required()
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
@jwt_required()
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
                return "Step Created Successfully under "+jobName+" !!"
            elif formName=='manageStep':

                jobName=data[masterKey]["jobName"]
                data={str(data[masterKey]["jobName"]+"|"+data[masterKey]['stepName']):data[masterKey]}
                #print(data)
                Job.addStep(str(jobName),data,path=__path__,logPath=__logPath__)
                return "Step Updated Successfully under "+jobName+" !!"
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
@jwt_required()
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

@app.route('/logout')
def logout():
    resp=make_response(redirect('http://localhost:8080/admin'))
    resp.delete_cookie('Authorization')
    return resp

@app.route('/hello/<user>')
def hello_name(user):

   return render_template('index.html', name = user)
#app.debug=True;
if __name__ == '__main__':
   app.run(host='0.0.0.0',port=8000)
