from Json_evaluation import Json_evaluation,log
from include.Variable import __emailFile__,__logPath__,__guidePath__
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from Generic import Generic
import smtplib, ssl,time
class Email:
    def addSmpt(smpt_dict,path=__guidePath__,logPath=__logPath__):
        try:
            Json_evaluation.updateJson(dict=smpt_dict,filename=__emailFile__,path=path)
            log("Adding "+str(smpt_dict.keys())+" smpt ",path=logPath)
            pass
        except Exception as e:
            log("Error_Email_addSmpt@"+str(e),path=logPath)

    def sendEmail(step_data):
        #context = ssl.create_default_context()

# Try to log in to server and send email
        try:
            data=Json_evaluation.getJsonByKey(filename=__emailFile__,key=step_data["emailProfilerName"])

            #print(step_data[data["attachmentFilePath"]])
            server = smtplib.SMTP(data["emailServer"],int(data["emailPort"]),None, 30)
            #import traceback
            #traceback.print_exc()

            msg = MIMEMultipart()
            msg['From'] = data["emailUser"]
            msg['To'] = step_data["receiver_emails"]
            msg['Subject'] = "Willdo-Automated generated email!!"
            body = str(step_data["emailMsg"])
            msg.attach(MIMEText(body, 'html'))
            attachment=""
            #for attachPath in Generic.removeLastSperator(step_data["attachmentFilePath"]).split('|'):
            attachPath=step_data["attachmentFilePath"]
            part = MIMEBase('application', 'octet-stream')
            try:
                attachment = open(attachPath, "rb")
            except Exception as ee:
                log("Attachment block" + str(ee))

            if attachment!="":
                #print(attachPath)
                part.set_payload(attachment.read())
                attachment.close()
                part.add_header('Content-Disposition', "attachment; filename= %s" % Generic.getFileNameFromPath(attachPath))
                encoders.encode_base64(part)
                msg.attach(part)


            text = msg.as_string()

            server.ehlo() # Can be omitted
            server.starttls() # Secure the connection
            server.ehlo() # Can be omitted
            server.login(data["emailUser"], data["emailPassword"])
            server.sendmail(data["emailUser"],str(step_data["receiver_emails"]).split(','),text)
        except smtplib.SMTPException as e:
            log("Error_Email_sendEmail@SMTPException_"+str(e)) # Didn't make an instance.
        except smtplib.socket.error:
            log("Error_Email_sendEmail@Socket_"+str(e))
        finally:
            server.quit()
