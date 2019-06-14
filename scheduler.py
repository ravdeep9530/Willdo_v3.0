import sys
sys.path.insert(0,'Connetions')
import sched, time
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Connections.sqlConn import connection
import asyncio
import pymysql
from include.Variable import __guidePath__
from Json_evaluation import Json_evaluation,log
from InsertConnection import insertConnection
from Jobs import Job
from Sync import Sync
from include.Variable import __stepsFile__,__jobCache__,__jobQueue__,__schedulerTimeStampFile__
from ExecuteStep import ExecuteStep
from Url import Url
import threading
from Generic import Generic 
email_template = []

nearestJobName={}
def send_report(filename=""):

    server = None

    # Send the mail
    if email_template.__len__() > 0:
        try:
            print(email_template[0][1])
            #server = smtplib.SMTP(email_template[0][4], email_template[0][5],None, 30)
            #try:
             #   server.connect(email_template[0][4], email_template[0][5],None, 30)
            #except smtplib.SMTPAuthenticationError as e:
             #   print(str(e))
            #print(email_template[0][1])

            import traceback
            traceback.print_exc()
            #server.connect()


            #server.starttls()
            # Next, log in to the server
            #server.login(email_template[0][1], email_template[0][2])

            msg = MIMEMultipart()
            msg['From'] = "ravdeeps3@gmail.com"
            msg['To'] = email_template[0][9]
            msg['Subject'] = email_template[0][6]
            body = email_template[0][7]
            msg.attach(MIMEText(body, 'plain'))
            attachment = ""

            if email_template[0][8] == 1:
                part = MIMEBase('application', 'octet-stream')
                try:
                    attachment = open("./" + filename, "rb")
                except Exception as ee:
                    print("" + str(ee))
                if attachment != "":
                    part.set_payload((attachment).read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
                    msg.attach(part)
            text = msg.as_string()

            #server.sendmail("ravdeeps3@gmail.com",email_template[0][9].split(','), text)

            print('sent' + str(email_template[0][10]) + str('1'))
            getResult("UPDATE EMAIL_HISTORY SET status=1 WHERE history_id=" + str(email_template[0][10]));
        except pymysql.InternalError as e:
            print ('SMTP Exception:' + str(e))
            getResult("INSERT INTO `JOB_ERROR`(`job_id`, `error_description`) VALUES (1,'SMTP Exception:" + str(e)+"')")
        except smtplib.SMTPException as e:
            print ('SMTP Exception:' + str(e))
            import traceback
            traceback.print_exc()
        except Exception as e:
            print ('SMTP Exception:' + str(e))
            import traceback
            traceback.print_exc()
            # c = con.cursor()
            # print("CALL updateMessageQueue('" + str(row[0]) + "');")
            # c.callproc("updateEmailHistory", [int(email_template[0][10]),int('2')])

            # c.close()


def getResult(q):
    con=connection("con_3")
    cur = con.cursor()
    cur.execute(q)
    del email_template[:]
    row = cur.fetchone()
    while row is not None:
        email_template.append(row)
        #print(email_template)

        row = cur.fetchone()

    # with open('music1.json', 'w') as f:
    #    json.dump(rs,f,cls=DatetimeEncoder)

    # for r in cur:
    #   print(r)
    con.commit()
    cur.close()
    # con.close()

    return 1

def executeJob(nearestJobName,nearestJob):
    try:
        print(nearestJobName,nearestJob)
        if int(nearestJob[nearestJobName]["remainingSec"])==0:
            log(nearestJobName+" Job Execution has been started!!")
            Job.executeJob(nearestJobName)
    except Exception as e:
        log(" Warning: Scheduler is free- No job for this instance"+str(e))

async def check_pending_notifications():
    try:

        #con_dict={"con_4":{"server": "94.156.144.217", "user": "hotel", "password": "indian12", "database": "hotels", "charset": "utf8", "port": 3306, "use_unicode": "True","connType":"mysql"}}
        #insertConnection(con_dict)
        #job={"JOB3":{"conName":"","jobStatement":"","interval":0,"scheuledTime":"","description":"","type":"","startDate":"","endDate":"17/04/2019","isActive":1,"lastRunDate":"-1"}}
        #Job.setJob(job)
        #step={"step1":{"jobName":"","stepNo":1,"statement":"","interval":"","stepType":"urlDownload","isActive":1,"parameter":"p1=2|p2=5|p3='ddsd'"}}
        #addStep("JOB1",step)
        #print()
        #getResult("CALL `getEmailTemplate`();")
        #ExecuteStep.executeStep("Willdo|step1")
        #Url.callApi()

        Job.prepareJobQueue()
        #Job.getNearestJob()
        #Job.executeJob(Job.getNearestJob())
        #nearestJob=Job.getNearestJob() #Disabled in v3.0
        #nearestJobName=Json_evaluation.getJsonByKey(filename=__jobQueue__,key=nearestJob) #Disabled in v3.0
        readyQueue=Json_evaluation.readJSON(filename=__jobQueue__)
        for nearestJobName in readyQueue.keys():
            if readyQueue[nearestJobName]['remainingSec']==0:
                jobThread=threading.Thread(target=executeJob,args=(nearestJobName,readyQueue,))
                jobThread.daemon=True
                jobThread.start()
        #print(data)
        #print(data["remainingSec"])

            #Job.lastRunUpdate(nearestJob)

        #filename=""
        #if email_template[0][8] == 1:
        #    filename = getFilename(email_template[0][11])
        #send_report(filename)
        pass
    except Exception as e:
        print("#Warning: No Job  is Pending." + str(e))
        #if str(e).__contains__("index out")!=1:
            #getResult("INSERT INTO `JOB_ERROR`(`job_id`, `error_description`) VALUES (1,'SMTP Exception:" + str(e) + "')")


s = sched.scheduler(time.time, time.sleep)

def setSchedulerTimeStap():
    try:
        dateTime=Generic.getDateTime()
        Json_evaluation.updateJson({"schedulerTimeStamp":str(dateTime),"schedulerStatus":"ON"},filename=__schedulerTimeStampFile__)
        log("Scheduler Restarted at "+str(dateTime))
        
    except Exception as e:
        log("Error_setSchedulerTimeStap"+str(e))



setSchedulerTimeStap()

def do_something(sc):
    log("Looping in another cycle....")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(check_pending_notifications())

    s.enter(60, 1, do_something, (sc,))


s.enter(1, 1, do_something, (s,))
s.run()
