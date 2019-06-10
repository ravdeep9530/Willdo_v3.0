import sys
from PyQt5.QtWidgets import *#QMainWindow, QApplication,QMessageBox,QHBoxLayout,QDialog,QPushButton
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from functools import partial
from Menu import Menu
from InsertConnection import insertConnection,validateConName
from Connections.sqlConn import connection,executeSql
from Json_evaluation import log,Json_evaluation
from include.Variable import __connectionFile__,__jobFile__,__stepsFile__,__emailFile__,__parameterFile__,__syncFile__,__jobQueue__,__installationDirName__,__logPath__,__logFile__,__storagePath__,__guidePath__

from Generic import Generic
from Jobs import Job
from Email import Email
from Parameter import Parameter
from Sync import Sync
from ExecuteStep import ExecuteStep
from History import History
import threading,time
globalRemoteName="susServer"
class Second(QMainWindow):
    def __init__(self, parent=None):
        super(Second, self).__init__(parent)
class Window(QMainWindow):

    def __init__(self):
        super().__init__()
        self.top=10
        self.bottom=10
        self.left=100
        self.right=100
        self.width=700
        self.hight=500


        self.initUI()


    def initUI(self):

        self.statusBar().showMessage('Ready')
        #Adding Menu class
        Menu().loadMenu(self)
        mainFram=QFrame(self)
        mainFram.setGeometry(0, 0, 300, 0)
        mainHbox=QHBoxLayout()
        hbox=QFormLayout()
        fbox=QFormLayout()
        jobCurrentQueueHeaderList=['Job Name','Scheduled Time','Remaining Minutes']
        self.l_jobQueue = QLabel(self)
        self.l_jobQueue.setText("Current Job Queue")
        self.l_jobQueue.setGeometry(20,30, 150,15)
        self.jobQueueList = QTableWidget(self)
        self.jobQueueList.setColumnCount(3)
        self.jobQueueList.setHorizontalHeaderLabels( jobCurrentQueueHeaderList )


        self.jobQueueList.setGeometry(20,50, 400, 200)
        #self.loadCurrentJobQueueMainFrame(self.jobQueueList)

        self.executeLoader(delay=5)
        #hbox.addRow(self.jobQueueList)
        hbox.addWidget(mainFram)
        hbox.addWidget(self.l_jobQueue)
        mainHbox.addLayout(hbox)
        self.setLayout(mainHbox)





        #fileMenu.addAction(exitAct)

        self.setGeometry(self.left, self.right, self.top, self.bottom)
        self.resize(self.width,self.hight)
        self.setWindowTitle('Willdo')
        self.show()
    def executeLoader(self,delay):
        execThread=threading.Thread(target=self.loadCurrentJobQueueMainFrame,args=(delay,))
        execThread.daemon=True
        execThread.start()

    def loadCurrentJobQueueMainFrame(self,delay):
        #Parameter.getParamOptions('Willdo|fffffgf')
        path=Generic.replaceConnectorInPath(__installationDirName__+"/"+__guidePath__+"/"+__jobQueue__)

        savePath=Generic.replaceConnectorInPath(Generic.getCurrentPath()+"/"+__guidePath__+"/"+__jobQueue__)
        remote_dict=Json_evaluation.getJsonByKey(filename=__syncFile__,key=globalRemoteName)
        Sync.getFileFromRemoteAndSave(remote_dict,path,savePath,Generic.getFileNameFromPath(path))
        time.sleep(delay)
        list=self.jobQueueList

        jobQueue=Json_evaluation.readJSON(filename=__jobQueue__)
        self.jobQueueList.setRowCount(len(jobQueue))
        i=0
        for data in jobQueue.keys():
            j=0
            list.setItem(i,j,QTableWidgetItem(str(data)))
            j+=1
            list.setItem(i,j,QTableWidgetItem(str(jobQueue[data]["scheduledTime"])))
            j+=1
            list.setItem(i,j,QTableWidgetItem(str(jobQueue[data]["remainingSec"]/60)))
            i+=1
            #print(data)
        self.executeLoader(delay=60)



    def createNewJob(self):

        self.showCreateNewJobdialog()
    def manageJobs(self):
        self.manageJobs()
    def manageCondialog(self):
        self.manageCon()
    def createNewSmpt(self):
        self.showCreateNewSmptdialog()
    def createNewParam(self):
        self.showCreateNewParamdialog()
    def createNewSync(self):
        self.showCreateNewSyncdialog()
        #Sync.connectRemoteSSH()
    def manageRemote(self):
        self.manageRemoteSync()
    def reviewHistory(self):
        self.showhistoryReviewDialog()

    def showCreateNewJobdialog(self):
        self.newJobDialog = QDialog()
        fbox = QFormLayout()
        l_conName=QLabel("Connection")
        self.c_conName=QComboBox()
        for key in Json_evaluation.readJSON(filename=__connectionFile__):
            self.c_conName.addItem(key)
        fbox.addRow(l_conName,self.c_conName)
        self.l_jobName = QLabel("Name")
        self.t_jobName = QLineEdit()
        fbox.addRow(self.l_jobName,self.t_jobName)
        self.l_description = QLabel("Description")
        self.t_description = QLineEdit()
        fbox.addRow(self.l_description,self.t_description)
        l_startDate=QLabel("Start Date")
        self.t_startDate=QDateEdit()
        self.t_startDate.setDate(QDate.currentDate())
        fbox.addRow(l_startDate,self.t_startDate)
        l_endDate=QLabel("End Date")
        self.t_endDate=QDateEdit()
        self.t_endDate.setDate(QDate.currentDate())
        fbox.addRow(l_endDate,self.t_endDate)
        l_scheduledTime=QLabel("Schedule Time")
        self.t_scheduledTime=QTimeEdit()

        fbox.addRow(l_scheduledTime,self.t_scheduledTime)
        l_interval=QLabel("Interval")
        self.c_interval=QComboBox()
        self.c_interval.addItem("After 1 Minutes",-1)
        self.c_interval.addItem("After 5 Minutes",-5)
        self.c_interval.addItem("After 10 Minutes",-10)
        self.c_interval.addItem("After 20 Minutes",-20)
        self.c_interval.addItem("After 30 Minutes",-30)
        self.c_interval.addItem("After 40 Minutes",-40)
        self.c_interval.addItem("After 50 Minutes",-50)
        self.c_interval.addItem("After 60 Minutes",-60)
        self.c_interval.addItem("Daily",1)
        self.c_interval.addItem("After One Day",2)
        self.c_interval.addItem("After Two Day",3)
        self.c_interval.addItem("After Three Day",4)
        self.c_interval.addItem("Weekly",7)
        self.c_interval.addItem("Month",30)
        fbox.addRow(l_interval,self.c_interval)
        b_create=QPushButton("Create")
        b_cancel=QPushButton("Cancel")
        fbox.addRow(b_create,b_cancel)
        b_cancel.clicked.connect(self.newJobDialog.close)
        b_create.clicked.connect(partial(self.submitJob,dialog=self.newJobDialog,response="Job created successfully!!!"))

        self.newJobDialog.setLayout(fbox)
        #b1.move(50,50)
        self.newJobDialog.setWindowTitle("Create New Job")
        self.newJobDialog.setWindowModality(Qt.ApplicationModal)
        self.newJobDialog.exec_()
    def submitJob(self,dialog,closeDialog=1,response=""):
        try:

            if self.t_jobName.text()=="":
                self.testConAlert(response="Firstly enter Job name!!!!")
                return 0
            if Job.validateJobName(self.t_jobName.text())!=1 and closeDialog==1:
                self.testConAlert(response="Job name already exists in system!!")
                return
            job={self.t_jobName.text():{"conName":self.c_conName.currentText(),"jobStatement":"","interval":self.c_interval.currentData(),"scheuledTime":self.t_scheduledTime.time().toString("HH:mm"),"description":self.t_description.text(),"type":"","startDate":self.t_startDate.date().toString("dd/MM/yyyy"),"endDate":self.t_endDate.date().toString("dd/MM/yyyy"),"isActive":1,"lastRunDate":"-1"}}
            Job.setJob(job,isNew=closeDialog)
            if response!="":
                self.testConAlert(response=response)
            if closeDialog==1:
                dialog.close()
        except Exception as e:
            self.testConAlert(response="Something went wrong!!!!")
            log("Error_Window_submitJob@"+str(e))

    #*******************Manage Job Starts***********
    def manageJobs(self):
        try:
            self.manageJobDialog = QDialog()
            lbox = QFormLayout()
            fbox=QFormLayout()
            vbox = QHBoxLayout()
            self.jobList = QListWidget(self)
            #items = ['Item %s' % (i + 1) for i in range(10)]
            data=Json_evaluation.readJSON(filename=__jobFile__)
            for con in data.keys():
                self.jobList.addItem(str(con))
            lbox.addRow(self.jobList)
            self.jobList.itemClicked.connect(self.getJobBykey)
            fbox = QFormLayout()
            l_conName=QLabel("Connection")
            self.c_conName=QComboBox()
            for key in Json_evaluation.readJSON(filename=__connectionFile__):
                self.c_conName.addItem(key)
            fbox.addRow(l_conName,self.c_conName)
            self.l_jobName = QLabel("Name")
            self.t_jobName = QLineEdit()
            self.t_jobName.setReadOnly(True)
            fbox.addRow(self.l_jobName,self.t_jobName)
            self.l_description = QLabel("Description")
            self.t_description = QLineEdit()
            fbox.addRow(self.l_description,self.t_description)
            l_startDate=QLabel("Start Date")
            self.t_startDate=QDateEdit()
            self.t_startDate.setDate(QDate.currentDate())
            fbox.addRow(l_startDate,self.t_startDate)
            l_endDate=QLabel("End Date")
            self.t_endDate=QDateEdit()
            self.t_endDate.setDate(QDate.currentDate())
            fbox.addRow(l_endDate,self.t_endDate)
            l_scheduledTime=QLabel("Schedule Time")
            self.t_scheduledTime=QTimeEdit()

            fbox.addRow(l_scheduledTime,self.t_scheduledTime)
            l_interval=QLabel("Interval")
            self.c_interval=QComboBox()
            self.c_interval.addItem("After 1 Minutes",-1)
            self.c_interval.addItem("After 5 Minutes",-5)
            self.c_interval.addItem("After 10 Minutes",-10)
            self.c_interval.addItem("After 20 Minutes",-20)
            self.c_interval.addItem("After 30 Minutes",-30)
            self.c_interval.addItem("After 40 Minutes",-40)
            self.c_interval.addItem("After 50 Minutes",-50)
            self.c_interval.addItem("After 60 Minutes",-60)
            self.c_interval.addItem("Daily",1)
            self.c_interval.addItem("After One Day",2)
            self.c_interval.addItem("After Two Day",3)
            self.c_interval.addItem("After Three Day",4)
            self.c_interval.addItem("Weekly",7)
            self.c_interval.addItem("Month",30)
            fbox.addRow(l_interval,self.c_interval)
            b_create=QPushButton("Update")
            b_cancel=QPushButton("Delete")
            self.b_addStep=QPushButton("Add Step")
            self.b_addStep.setEnabled(False)
            self.b_addStep.clicked.connect(partial(self.newStepDialog_m,self.t_jobName))
            fbox.addRow(self.b_addStep)
            fbox.addRow(b_create,b_cancel)
            b_cancel.clicked.connect(self.deleteJob)
            b_create.clicked.connect(partial(self.submitJob,dialog=self.manageJobDialog,closeDialog=0,response="Job updated successfully!!!"))
            fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

            vbox.addLayout(lbox)
            vbox.addLayout(fbox)
            self.manageJobDialog.setLayout(vbox)
            self.manageJobDialog.setWindowModality(Qt.ApplicationModal)
            self.manageJobDialog.setWindowTitle("Manage Jobs")
            self.manageJobDialog.exec_()
        except Exception as e:
            log("Error_Window_manageJob@"+str(e))
    def deleteJob(self):
        try:
            key=str(self.t_jobName.text())
            if key!="":
                Json_evaluation.removeJson(key=key,filename=__jobFile__)
                self.manageJobDialog.close()
                self.manageJobs()
        except Exception as e:
            self.testConAlert(response="Something went wrong!!!!")
            log("Error_Window_deleteJob@"+str(e))
    def getJobBykey(self):
        try:
            key=self.jobList.currentItem().text()
            data=Json_evaluation.getJsonByKey(key=key,filename=__jobFile__)
            self.t_jobName.setText(key)
            self.c_conName.setCurrentIndex(self.c_conName.findText((data["conName"])))
            self.t_description.setText(data["description"])
            self.t_startDate.setDate(QDate.fromString(str(data["startDate"]),"dd/MM/yyyy"))
            self.t_endDate.setDate(QDate.fromString(data["endDate"],"dd/MM/yyyy"))
            self.c_interval.setCurrentIndex(self.c_interval.findData((data["interval"])))
            self.t_scheduledTime.setTime(QTime.fromString(data["scheuledTime"],"HH:mm"))
            self.b_addStep.setEnabled(True)

        except Exception as e:
            log("Error_Window_getJobBykey@"+str(e))




    #*******************Manage Conection End**************
    #********************New Connection Module Start********
    def showCreateNewCondialog(self):
        self.newConDialog = QDialog()
        fbox = QFormLayout()
        self.l_driver=QLabel("Driver")
        self.c_driver=QComboBox()
        self.c_driver.addItem("MySql")
        self.c_driver.addItem("MS Sql Server")
        fbox.addRow(self.l_driver,self.c_driver)
        self.l_conName = QLabel("Name")
        self.t_conName = QLineEdit()
        fbox.addRow(self.l_conName,self.t_conName)
        self.l_server = QLabel("Server")
        self.t_server = QLineEdit()
        fbox.addRow(self.l_server,self.t_server)
        self.l_user = QLabel("User Name")
        self.t_user = QLineEdit()
        fbox.addRow(self.l_user,self.t_user)
        self.l_password = QLabel("Password")
        self.t_password = QLineEdit()
        fbox.addRow(self.l_password,self.t_password)
        self.l_port = QLabel("Port")
        self.t_port = QLineEdit()
        fbox.addRow(self.l_port,self.t_port)
        self.l_database = QLabel("Database")
        self.t_database = QLineEdit()
        fbox.addRow(self.l_database,self.t_database)

        self.l_uniCode=QLabel("Use Unicode")
        self.c_uniCode=QComboBox()
        self.c_uniCode.addItem("True")
        self.c_uniCode.addItem("False")
        fbox.addRow(self.l_uniCode,self.c_uniCode)
        self.l_charset=QLabel("Charset")
        self.c_charset=QComboBox()
        self.c_charset.addItem("utf8")
        fbox.addRow(self.l_charset,self.c_charset)
        b_testButton=QPushButton("Test Conection")
        fbox.addRow(b_testButton)
        b_create=QPushButton("Create")
        b_cancel=QPushButton("Cancel")
        fbox.addRow(b_create,b_cancel)
        b_cancel.clicked.connect(self.newConDialog.close)
        b_create.clicked.connect(partial(self.submitConForm,self.newConDialog))
        b_testButton.clicked.connect(partial(self.testCon,removeJsonFlag=1))
        fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.newConDialog.setLayout(fbox)
        #b1.move(50,50)s
        self.newConDialog.setWindowTitle("Create New Connection")
        self.newConDialog.setWindowModality(Qt.ApplicationModal)
        self.newConDialog.exec_()
    def submitConForm(self,dialog,closeDialog=1,response=""):
        try:
            con_dict={self.t_conName.text():{"server": self.t_server.text(), "user": self.t_user.text(), "password": self.t_password.text(), "database": self.t_database.text(), "charset":self.c_charset.currentText() , "port": int(self.t_port.text()), "use_unicode": self.c_uniCode.currentText(),"connType":self.c_driver.currentText()}}
            insertConnection(con_dict)
            con=connection(self.t_conName.text())
            r=executeSql(con,"SELECT @@version")
            if closeDialog==1:
                dialog.close()
            if response!="":
                self.testConAlert(response=response)
        except Exception as e:
            self.testConAlert("Something Went Wrong. Please verify Credentials!!")
            log("Error_Window_submitConForm@"+str(e))

    def testCon(self,removeJsonFlag=0):
        try:
            con_dict={self.t_conName.text():{"server": self.t_server.text(), "user": self.t_user.text(), "password": self.t_password.text(), "database": self.t_database.text(), "charset":self.c_charset.currentText() , "port": int(self.t_port.text()), "use_unicode": self.c_uniCode.currentText(),"connType":self.c_driver.currentText()}}

            insertConnection(con_dict)
            con=connection(self.t_conName.text())
            r=executeSql(con,"SELECT @@version;")
            #print(r)
            self.testConAlert("Connection Successfully Connected!!")
            if removeJsonFlag==1:
                Json_evaluation.removeJson(key=self.t_conName.text(),filename=__connectionFile__)
        except Exception as e:
            self.testConAlert("Something Went Wrong. Please verify Credentials!!")
            log("Error_Window_testCon@"+str(e))

    def testConAlert(self,response):
        d = QDialog()
        d.setWindowTitle("Alert")
        l_response=QLabel(response)
        fbox = QFormLayout()
        fbox.addRow(l_response)
        b_OK=QPushButton("OK");
        b_OK.setMaximumSize(QSize(40, 40))
        b_OK.clicked.connect(d.close)
        fbox.addRow(b_OK)
        d.setLayout(fbox)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()
    #********************New Connection End*******************
    #*******************Manage Connection Starts***********
    def manageCon(self):
        try:
            self.manageConDialog = QDialog()
            lbox = QFormLayout()
            fbox=QFormLayout()
            vbox = QHBoxLayout()
            self.list = QListWidget(self)
            #items = ['Item %s' % (i + 1) for i in range(10)]
            data=Json_evaluation.readJSON(filename=__connectionFile__)
            for con in data.keys():
                self.list.addItem(str(con))
            lbox.addRow(self.list)
            self.list.itemClicked.connect(self.getConBykey)
            fbox = QFormLayout()
            self.l_driver=QLabel("Driver")
            self.c_driver=QComboBox()
            self.c_driver.addItem("MySql")
            self.c_driver.addItem("MS Sql Server")
            fbox.addRow(self.l_driver,self.c_driver)
            self.l_conName = QLabel("Name")
            self.t_conName = QLineEdit()
            self.t_conName.setEnabled(False)
            fbox.addRow(self.l_conName,self.t_conName)
            self.l_server = QLabel("Server")
            self.t_server = QLineEdit()
            fbox.addRow(self.l_server,self.t_server)
            self.l_user = QLabel("User Name")
            self.t_user = QLineEdit()
            fbox.addRow(self.l_user,self.t_user)
            self.l_password = QLabel("Password")
            self.t_password = QLineEdit()
            fbox.addRow(self.l_password,self.t_password)
            self.l_port = QLabel("Port")
            self.t_port = QLineEdit()
            fbox.addRow(self.l_port,self.t_port)
            self.l_database = QLabel("Database")
            self.t_database = QLineEdit()
            fbox.addRow(self.l_database,self.t_database)

            self.l_uniCode=QLabel("Use Unicode")
            self.c_uniCode=QComboBox()
            self.c_uniCode.addItem("True")
            self.c_uniCode.addItem("False")
            fbox.addRow(self.l_uniCode,self.c_uniCode)
            self.l_charset=QLabel("Charset")
            self.c_charset=QComboBox()
            self.c_charset.addItem("utf8")
            fbox.addRow(self.l_charset,self.c_charset)
            b_testButton=QPushButton("Test Conection")
            fbox.addRow(b_testButton)
            b_create=QPushButton("Update")
            b_delete=QPushButton("Delete")
            fbox.addRow(b_create,b_delete)
            b_delete.clicked.connect(self.deleteConnection)
            b_create.clicked.connect(partial(self.submitConForm,self.manageConDialog,0,"Update Successfully!!"))
            b_testButton.clicked.connect(self.testCon)
            fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

            vbox.addLayout(lbox)
            vbox.addLayout(fbox)
            self.manageConDialog.setLayout(vbox)
            self.manageConDialog.setWindowModality(Qt.ApplicationModal)
            self.manageConDialog.setWindowTitle("Manage Connections")
            self.manageConDialog.exec_()
        except Exception as e:
            log("Error_Window_manageCon@"+str(e))
    def deleteConnection(self):
        key=str(self.t_conName.text())
        if key!="":
            Json_evaluation.removeJson(key=key,filename=__connectionFile__)
            self.manageConDialog.close()
            self.manageCon()
    def getConBykey(self):
        try:
            key=self.list.currentItem().text()
            data=Json_evaluation.getJsonByKey(key=key,filename=__connectionFile__)
            self.t_conName.setText(key)
            self.c_driver.setCurrentIndex(self.c_driver.findText((data["connType"])))
            self.t_server.setText(data["server"])
            self.t_user.setText(data["user"])
            self.t_password.setText(data["password"])
            self.t_database.setText(data["database"])
            self.t_port.setText(str(data["port"]))
            self.c_uniCode.setCurrentIndex(self.c_uniCode.findText((data["use_unicode"])))
            self.c_charset.setCurrentIndex(self.c_charset.findText((data["charset"])))
        except Exception as e:
            log("Error_Window_getConBykey@"+str(e))
    def submitConForm(self,dialog,closeDialog=1,response=""):
        try:
            con_dict={self.t_conName.text():{"server": self.t_server.text(), "user": self.t_user.text(), "password": self.t_password.text(), "database": self.t_database.text(), "charset":self.c_charset.currentText() , "port": int(self.t_port.text()), "use_unicode": self.c_uniCode.currentText(),"connType":self.c_driver.currentText()}}
            insertConnection(con_dict)
            con=connection(self.t_conName.text())
            r=executeSql(con,"SELECT @@version")
            if closeDialog==1:
                dialog.close()
            if response!="":
                self.testConAlert(response=response)
        except Exception as e:
            self.testConAlert("Something Went Wrong. Please verify Credentials!!")
            log("Error_Window_submitConForm@"+str(e))



    #*******************Manage Conection End**************

    def newStepDialog_m(self,step_jobName=""):
        try:
            self.cols=["Steps"]
            self.newStepDialog = QDialog()
            lbox = QFormLayout()
            fbox=QFormLayout()
            vbox = QHBoxLayout()
            self.tree =QTreeWidget()
            self.tree.setColumnCount(len(self.cols))
            self.tree.setHeaderLabels(self.cols)
            self.tree.header().setStyleSheet('QWidget { font: bold italic large "Times New Roman" }')

            data=Job.getStepsByJob(step_jobName.text())
            #print(data)
            no=1
            if data is not None:
                for i in data:
                    parent = QTreeWidgetItem(self.tree)
                    parent.setText(0, "Step {}".format(no)+" ("+i.split("|")[1]+")")
                    parent.setToolTip(0, "Step {}".format(no)+" ("+i.split("|")[1]+")")

                    parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
                    no+=1
                    step_data=Json_evaluation.getJsonByKey(key=i,filename=__stepsFile__)
                    #print(step_data)

                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    if int(step_data["stepType"])==1 :
                        child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                        child.setText(0,"Sql Statement=>"+step_data["statement"])
                        child.setToolTip(0,"Sql Statement=>"+step_data["statement"])
                        for param in step_data["parameter"].split('|'):
                            if param!="":
                                child1 = QTreeWidgetItem(parent)

                                child1.setText(0,"Parameter("+param[:-1]+"-"+self.paramSubItem(param[-1:])+")")
                                child1.setToolTip(0,"Parameter("+param[:-1]+"->"+self.paramSubItem(param[-1:])+")")
                                child1.setCheckState(0, Qt.Unchecked)

                    elif int(step_data["stepType"])==2:
                        child.setText(0,"Url=>"+step_data["url"])
                        child.setToolTip(0,"Url=>"+step_data["url"])
                        for param in step_data["parameter"].split('|'):
                            if param!="":
                                child1 = QTreeWidgetItem(parent)

                                child1.setText(0,"Parameter("+param[:-1]+"-"+self.paramSubItem(param[-1:])+")")
                                child1.setToolTip(0,"Parameter("+param[:-1]+"->"+self.paramSubItem(param[-1:])+")")
                                child1.setCheckState(0, Qt.Unchecked)
                    elif int(step_data["stepType"])==3:
                        child.setText(0,"Email =>"+step_data["emailProfilerName"])
                        child.setToolTip(0,"Email =>"+step_data["emailProfilerName"])
                        for param in step_data["parameter"].split('|'):
                            if param!="":
                                child2 = QTreeWidgetItem(parent)
                                child2.setText(0,"Parameter("+param[:-1]+"-"+self.paramSubItem(param[-1:])+")")
                                child2.setToolTip(0,"Parameter("+param[:-1]+"->"+self.paramSubItem(param[-1:])+")")
                                child2.setCheckState(0, Qt.Unchecked)

                    elif int(step_data["stepType"])==4:
                        child.setText(0,"Sql Procedure =>"+step_data["statement"])
                        child.setToolTip(0,"Sql Procedure =>"+step_data["statement"])
                        for param in step_data["parameter"].split('|'):
                            if param!="":
                                child1 = QTreeWidgetItem(parent)

                                child1.setText(0,"Parameter("+param[:-1]+"-"+self.paramSubItem(param[-1:])+")")
                                child1.setToolTip(0,"Parameter("+param[:-1]+"->"+self.paramSubItem(param[-1:])+")")
                                child1.setCheckState(0, Qt.Unchecked)
                    elif int(step_data["stepType"])==5:
                        child.setText(0,"Sql Procedure =>"+step_data["statement"])
                        child.setToolTip(0,"Sql Procedure =>"+step_data["statement"])
                        for param in step_data["parameter"].split('|'):
                            if param!="":
                                child1 = QTreeWidgetItem(parent)

                                child1.setText(0,"Parameter("+param[:-1]+"-"+self.paramSubItem(param[-1:])+")")
                                child1.setToolTip(0,"Parameter("+param[:-1]+"->"+self.paramSubItem(param[-1:])+")")
                                child1.setCheckState(0, Qt.Unchecked)
                    child.setCheckState(0, Qt.Unchecked)


            #self.tree.itemDoubleClicked.connect(self.find_checked)
            b_deleteStep=QPushButton("Delete Step")
            b_assigneParam=QPushButton("Parameter Assignment ")
            b_deleteStep.clicked.connect(partial(self.deleteStep,step_jobName.text(),dialog=self.newStepDialog))
            b_assigneParam.clicked.connect(partial(self.assignParamToStep,step_jobName.text(),dialog=self.newStepDialog))

            l_step_jobName=QLabel("Job Name")
            self.t_step_jobName=QLineEdit()
            self.t_step_jobName.setEnabled(False)
            self.t_step_jobName.setText(step_jobName.text())
            fbox.addRow(l_step_jobName,self.t_step_jobName)
            self.l_step_name=QLabel("Step Name")
            self.t_step_name=QLineEdit()
            fbox.addRow(self.l_step_name,self.t_step_name)
            l_stepType=QLabel("Select Type")
            self.c_stepType=QComboBox()
            self.c_stepType.addItem("Sql Statement",1)
            self.c_stepType.addItem("Sql Procedure",4)
            self.c_stepType.addItem("Url Call",2)
            self.c_stepType.addItem("Email Call",3)
            self.c_stepType.addItem("File Access",5)
            self.c_stepType.currentIndexChanged.connect(self.stepType_func)
            fbox.addRow(l_stepType,self.c_stepType)
            l_selectRemote=QLabel("Select Remote")
            self.c_remoteList=QComboBox()
            for rdata in Json_evaluation.readJSON(filename=__syncFile__).keys():
                self.c_remoteList.addItem(rdata)
            self.c_remoteList.setEnabled(False);
            fbox.addRow(l_selectRemote,self.c_remoteList)
            l_step_sqlStm=QLabel("Sql Statement")
            self.t_step_sqlStm=QTextEdit()
            self.t_step_sqlStm.setMinimumHeight(10)
            fbox.addRow(l_step_sqlStm,self.t_step_sqlStm)
            l_step_url=QLabel("Url")
            self.t_step_url=QTextEdit()
            fbox.addRow(l_step_url,self.t_step_url)
            l_stepEmailSetup=QLabel("Choose smpt server")
            self.c_stepEmailSetup=QComboBox()
            email_data=Json_evaluation.readJSON(filename=__emailFile__)
            for key in email_data.keys():
                self.c_stepEmailSetup.addItem(key)
            fbox.addRow(l_stepEmailSetup,self.c_stepEmailSetup)
            l_receiver=QLabel("Receiver Emails")
            self.t_receiverEmails=QTextEdit()
            fbox.addRow(l_receiver,self.t_receiverEmails)
            b_addStep=QPushButton("Add Step")
            b_addStep.clicked.connect(partial(self.submitStep,no=no,dialog=self.newStepDialog))
            fbox.addRow(b_addStep)
            self.tree.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            #self.tree.setHorizontalScrollMode(QAbstractItemView.ResizeToContents)
            lbox.addRow(self.tree)
            lbox.addRow(b_deleteStep,b_assigneParam)
            vbox.addLayout(lbox)
            vbox.addLayout(fbox)
            vbox.setSpacing(10)
            self.stepType_func()
            #vbox.setContentsMargins(0, 0, 0, 0)
            self.newStepDialog.setLayout(vbox)
            self.newStepDialog.setWindowModality(Qt.ApplicationModal)
            self.newStepDialog.setWindowTitle("Add Step")
            self.newStepDialog.exec_()
        except Exception as e:
            log("Error_Window_newStepDialog@"+str(e))
    def paramSubItem(self,item):
        item=int(item)
        if item==1:
            return "Input-Email Message"
        elif item==2:
            return "Input-Email file attachment"
        elif item==3:
            return "Input-Url Ping"
        elif item==4:
            return "Output-Downloaded File"
        elif item==5:
            return "Output-Sql Scalar Resultset"
        elif item==6:
            return "Output-Sql Row Resultset"
        else:
            return "Other"
    def stepType_func(self):
        if self.c_stepType.currentData()==1:
            self.c_stepEmailSetup.setEnabled(False)
            self.t_receiverEmails.setEnabled(False)
            self.t_step_url.setEnabled(False)
            self.t_step_sqlStm.setEnabled(True)
            self.c_remoteList.setEnabled(False)
        elif self.c_stepType.currentData()==2:
            self.c_stepEmailSetup.setEnabled(False)
            self.t_receiverEmails.setEnabled(False)
            self.t_step_url.setEnabled(True)
            self.t_step_sqlStm.setEnabled(False)
            self.c_remoteList.setEnabled(False)
        elif self.c_stepType.currentData()==3:
            self.c_stepEmailSetup.setEnabled(True)
            self.t_receiverEmails.setEnabled(True)
            self.t_step_url.setEnabled(False)
            self.t_step_sqlStm.setEnabled(False)
            self.c_remoteList.setEnabled(False)
        elif self.c_stepType.currentData()==5:
            self.c_stepEmailSetup.setEnabled(False)
            self.t_receiverEmails.setEnabled(False)
            self.t_step_url.setEnabled(False)
            self.t_step_sqlStm.setEnabled(False)
            self.c_remoteList.setEnabled(True)
    def stepTypeValidation_func(self):
        if self.c_stepType.currentData()==1:
            if self.t_step_sqlStm.toPlainText()=="":
                self.testConAlert(response="Firstly enter valid sql statement!!!!!!")
                return False

        elif self.c_stepType.currentData()==2:
            if self.t_step_url.toPlainText()=="":
                self.testConAlert(response="Firstly enter valid Url!!!!!!")
                return False
        #elif self.c_stepType.currentData()==3:
        #    self.b_stepEmailSetup.setEnabled(True)
        if self.t_step_name.text()=="":
            self.testConAlert(response="Firstly enter valid Step name !!!!!!")
            return False

        if ExecuteStep.validateStepName(self.t_step_jobName.text(),self.t_step_name.text())==0:
            self.testConAlert(response="Step name is already exists in system!!!")
            return False
        return True



    def submitStep(self,dialog,no=1):
        try:
            if self.stepTypeValidation_func()==True:
                step={self.t_step_jobName.text()+"|"+self.t_step_name.text():{"jobName":self.t_step_jobName.text(),"stepNo":no,"statement":self.t_step_sqlStm.toPlainText(),"interval":"","stepType":self.c_stepType.currentData(),"isActive":1,"url":self.t_step_url.toPlainText(),"emailProfilerName":self.c_stepEmailSetup.currentText(),"receiver_emails":self.t_receiverEmails.toPlainText(),
                "remoteName":self.c_remoteList.currentText(),"parameter":""}}
                #print(step)
                Job.addStep(str(self.t_step_jobName.text()),step)
                self.testConAlert(response="Step added successfully!!")
                dialog.close()
                self.newStepDialog_m(step_jobName=self.t_step_jobName)
        except Exception as e:
            log("Error_Window_submitStep@"+str(e))

    def deleteStep(self,jobName,dialog):
        try:
            checked=self.find_checked()
            seq=self.stepSeq()
            deleteQueue=[]
            for key in checked.keys():
                if len(checked[key])>0:
                    deleteQueue.insert(0,key)
            closeDialogFlag=0
            for delQ in deleteQueue:
                #str(key.replace(' ','').replace('Step',''))[:1])
                if int(str(delQ.replace(' ','').replace('Step',''))[:1])==seq:
                    self.testConAlert(response="Step deleted successfully!!")
                    stepName=jobName+"|"+str(key[key.find('(')-len(key):]).replace('(','').replace(')','')
                    #self.testConAlert(response=stepName)
                    Json_evaluation.removeJson(filename=__stepsFile__,key=stepName)
                    seq-=1
                    closeDialogFlag=1
                else:
                    closeDialogFlag=0
            if closeDialogFlag==1:
                dialog.close()
                self.newStepDialog_m(step_jobName=self.t_step_jobName)
            else:
                self.testConAlert(response="You Cannot remove step without follow sequence. Please start remove from  large step number or follow sequence large to small step!!  ")

        except Exception as e:
            log("Error_Window_deleteStep@"+str(e))
    def assignParamToStep(self,jobName,dialog):
        try:
            checked=self.find_checked()
            #print(checked)
            seq=self.stepSeq()
            deleteQueue=[]
            stepName=""
            IsEligible=0
            for key in checked.keys():
                if len(checked[key])>0:
                    IsEligible+=1
                    stepName=key


            if IsEligible==1:
                stepName=jobName+"|"+str(stepName[stepName.find('(')-len(stepName):]).replace('(','').replace(')','')
                self.showAddNewParamdialog(jobName=jobName,stepName=stepName)
            else:
                self.testConAlert(response="Please select individual step!!")
                return

        except Exception as e:
            log("Error_Window_assignParamToStep@"+str(e))

    def find_checked(self):

        checked = dict()
        root = self.tree.invisibleRootItem()
        signal_count = root.childCount()

        for i in range(signal_count):
            signal = root.child(i)
            checked_sweeps = list()
            num_children = signal.childCount()

            for n in range(num_children):
                child = signal.child(n)

                if child.checkState(0) == Qt.Checked:
                    checked_sweeps.append(child.text(0))

            checked[signal.text(0)] = checked_sweeps

        return checked
    def stepSeq(self):
        checked = dict()
        root = self.tree.invisibleRootItem()
        signal_count = root.childCount()
        return signal_count



    #********************New Smpt Module Start********
    def showCreateNewSmptdialog(self):
        self.newSmptDialog = QDialog()
        fbox = QFormLayout()

        self.l_smptName = QLabel("SMPT Name")
        self.t_smptName = QLineEdit()
        fbox.addRow(self.l_smptName,self.t_smptName)
        self.l_server = QLabel("Server")
        self.t_smptServer = QLineEdit()
        fbox.addRow(self.l_server,self.t_smptServer)
        self.l_smptUser = QLabel("User Name")
        self.t_smptUser = QLineEdit()
        fbox.addRow(self.l_smptUser,self.t_smptUser)
        self.l_smptPassword = QLabel("Password")
        self.t_smptPassword = QLineEdit()
        fbox.addRow(self.l_smptPassword,self.t_smptPassword)
        self.l_smptPort = QLabel("Port")
        self.t_smptPort = QLineEdit()
        fbox.addRow(self.l_smptPort,self.t_smptPort)
        self.l_smptEmailName = QLabel("Email name")
        self.t_smptEmailName = QLineEdit()
        fbox.addRow(self.l_smptEmailName,self.t_smptEmailName)


        b_create=QPushButton("Create")
        b_cancel=QPushButton("Cancel")
        fbox.addRow(b_create,b_cancel)
        b_cancel.clicked.connect(self.newSmptDialog.close)
        b_create.clicked.connect(partial(self.submitEmailForm,dialog=self.newSmptDialog))
        fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.newSmptDialog.setLayout(fbox)
        #b1.move(50,50)s
        self.newSmptDialog.setWindowTitle("Create New Email SMTP")
        self.newSmptDialog.setWindowModality(Qt.ApplicationModal)
        self.newSmptDialog.exec_()
    def submitEmailForm(self,dialog,closeDialog=1,response=""):
        try:
            smpt_dict={self.t_smptName.text():{"emailServer": self.t_smptServer.text(), "emailUser": self.t_smptUser.text(), "emailPassword": self.t_smptPassword.text() , "emailPort": int(self.t_smptPort.text()), "emailTitle": self.t_smptEmailName.text()}}

            Email.addSmpt(smpt_dict)

            if closeDialog==1:
                dialog.close()
            if response!="":
                self.testConAlert(response=response)
        except Exception as e:
            self.testConAlert("Something Went Wrong. Please verify Credentials!!")
            log("Error_Window_submitSmptForm@"+str(e))
##********************End of Email Module**********************

#********************New Parameter Module Start********
    def showCreateNewParamdialog(self):
        self.newParamDialog = QDialog()
        fbox = QFormLayout()

        self.l_paramName = QLabel("Parameter Name")
        self.t_paramName = QLineEdit()
        fbox.addRow(self.l_paramName,self.t_paramName)
        self.l_paramJobName = QLabel("Select Job Name")
        self.c_paramJobName=QComboBox()
        for key in Json_evaluation.readJSON(filename=__jobFile__).keys():
            self.c_paramJobName.addItem(key)
        fbox.addRow(self.l_paramJobName,self.c_paramJobName)
        self.l_paramInputType = QLabel("Parameter Type")
        self.c_paramInputType = QComboBox()
        self.c_paramInputType.addItem("Input Tpye",1)
        self.c_paramInputType.addItem("Output Tpye",2)
        fbox.addRow(self.l_paramInputType,self.c_paramInputType)
        self.l_paramValue = QLabel("Default Value")
        self.t_paramValue = QLineEdit()
        fbox.addRow(self.l_paramValue,self.t_paramValue)



        b_create=QPushButton("Create")
        b_cancel=QPushButton("Cancel")
        fbox.addRow(b_create,b_cancel)
        b_cancel.clicked.connect(self.newParamDialog.close)
        b_create.clicked.connect(partial(self.submitParamForm,dialog=self.newParamDialog,response="Parameter added successfully!!"))
        fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.newParamDialog.setLayout(fbox)
        #b1.move(50,50)s
        self.newParamDialog.setWindowTitle("Create New Parameter")
        self.newParamDialog.setWindowModality(Qt.ApplicationModal)
        self.newParamDialog.exec_()
    def submitParamForm(self,dialog,closeDialog=1,response=""):
        try:
            smpt_dict={self.t_paramName.text():{"stepName":"","jobName":self.c_paramJobName.currentText(),"paramType":self.c_paramInputType.currentData(),"paramValue":self.t_paramValue.text(),"paramSubType":-1}}

            Parameter.addParam(smpt_dict)

            if closeDialog==1:
                dialog.close()
            if response!="":
                self.testConAlert(response=response)
        except Exception as e:
            self.testConAlert("Something Went Wrong. Please verify Credentials!!")
            log("Error_Window_submitParamForm@"+str(e))



    def showAddNewParamdialog(self,jobName,stepName):
        self.addParamDialog = QDialog()
        fbox = QFormLayout()
        l_paramJobName = QLabel("Job Name|Step Name")
        self.t_paramJobName = QLineEdit()
        fbox.addRow(l_paramJobName,self.t_paramJobName)
        self.t_paramJobName.setText(stepName)
        self.t_paramJobName.setEnabled(False)




        self.l_addParamName = QLabel("Select Parameter")
        self.c_addParamName=QComboBox()
        self.getParamByJobAndType(jobName)
        fbox.addRow(self.l_addParamName,self.c_addParamName)
        self.l_paramOtherType = QLabel("Parameter Options")
        self.c_paramOtherType = QComboBox()
        stepType_data=Json_evaluation.getJsonByKey(key=stepName,filename=__stepsFile__)
        if int(stepType_data["stepType"])==3:
            self.c_paramOtherType.addItem("Input-Email Message",1)
            self.c_paramOtherType.addItem("Input-Email file attachment",2)
        elif int(stepType_data["stepType"])==2:
            self.c_paramOtherType.addItem("Input-Url Ping",3)
            self.c_paramOtherType.addItem("Output-Downloaded File",4)
        elif int(stepType_data["stepType"])==1 or stepType_data["stepType"]==4:
            self.c_paramOtherType.addItem("Output-Save Sql Scalar Result",5)
            self.c_paramOtherType.addItem("Output-Save Sql Row Resultset",6)
        elif int(stepType_data["stepType"])==5:
            self.c_paramOtherType.addItem("Input-File Path",7)
            self.c_paramOtherType.addItem("Output-File Path",8)


        fbox.addRow(self.l_paramOtherType,self.c_paramOtherType)





        b_create=QPushButton("Assigne")
        b_cancel=QPushButton("Cancel")
        fbox.addRow(b_create,b_cancel)
        b_cancel.clicked.connect(self.addParamDialog.close)
        b_create.clicked.connect(partial(self.updateParamStep,dialog=self.addParamDialog,response="Parameter assinged successfully!!",stepName=stepName,paramSubType=self.c_paramOtherType.currentData()))
        fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.addParamDialog.setLayout(fbox)
        #b1.move(50,50)s
        self.addParamDialog.setWindowTitle("Assigning Parameter Step")
        self.addParamDialog.setWindowModality(Qt.ApplicationModal)
        self.addParamDialog.exec_()

    def getParamByJobAndType(self,jobName):
        self.c_addParamName.clear()
        #paramType=self.c_paramInputType.currentData()
        for key in Parameter.getParamByJob(jobName):
            #print(key)
            self.c_addParamName.addItem(key)
    def updateParamStep(self,dialog,closeDialog=1,response="",stepName="Willdo",paramSubType=-1):
        #***************param update**************
        data=Json_evaluation.getJsonByKey(key=self.c_addParamName.currentText(),filename=__parameterFile__)

        if data["stepName"]=="" or data["stepName"]=="-1":
            data["stepName"]=stepName
        else:
            data["stepName"]+="#"+stepName
        if str(data["paramSubType"])=="-1":
            data["paramSubType"]=stepName+"@"+str(self.c_paramOtherType.currentData())
        else:
            data["paramSubType"]+="#"+stepName+"@"+str(self.c_paramOtherType.currentData())
        data={self.c_addParamName.currentText():data}
        Json_evaluation.updateJson(dict=data,filename=__parameterFile__)

        #******************* step Update********************

        data=Json_evaluation.getJsonByKey(key=stepName,filename=__stepsFile__)
        if str(data["parameter"])=="":
            data["parameter"]=self.c_addParamName.currentText()+str(self.c_paramOtherType.currentData())
        else:
            data["parameter"]+="|"+self.c_addParamName.currentText()+str(self.c_paramOtherType.currentData())
        data={stepName:data}
        Json_evaluation.updateJson(dict=data,filename=__stepsFile__)




        if response!="":
            self.testConAlert(response=response)
        if closeDialog==1:
            dialog.close()




####**************** End of Parameter module******************

#******************Sync Module **********


    def showCreateNewSyncdialog(self):
        self.newSyncDialog = QDialog()
        fbox = QFormLayout()
        self.l_driver=QLabel("OS")
        self.c_syncOS=QComboBox()
        self.c_syncOS.addItem("Windows")
        self.c_syncOS.addItem("Liniux")
        fbox.addRow(self.l_driver,self.c_syncOS)
        self.l_syncName = QLabel("Name")
        self.t_syncName = QLineEdit()
        fbox.addRow(self.l_syncName,self.t_syncName)
        self.l_syncServer = QLabel("Server")
        self.t_syncServer = QLineEdit()
        fbox.addRow(self.l_syncServer,self.t_syncServer)
        self.l_syncUser = QLabel("User Name")
        self.t_syncUser = QLineEdit()
        fbox.addRow(self.l_syncUser,self.t_syncUser)
        self.l_syncPassword = QLabel("Password")
        self.t_syncPassword = QLineEdit()
        fbox.addRow(self.l_syncPassword,self.t_syncPassword)
        self.l_syncPort = QLabel("Port")
        self.t_syncPort = QLineEdit()
        self.t_syncPort.setText("22")
        fbox.addRow(self.l_syncPort,self.t_syncPort)
        self.l_remotePath = QLabel("Remote Path")
        self.t_remotePath = QLineEdit()
        fbox.addRow(self.l_remotePath,self.t_remotePath)

        b_create=QPushButton("Create")
        b_cancel=QPushButton("Cancel")
        fbox.addRow(b_create,b_cancel)
        b_cancel.clicked.connect(self.newSyncDialog.close)
        b_create.clicked.connect(partial(self.submitSyncForm,dialog=self.newSyncDialog,response="Sync created Successfully!!"))
        fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.newSyncDialog.setLayout(fbox)
        #b1.move(50,50)s
        self.newSyncDialog.setWindowTitle("Create New Connection")
        self.newSyncDialog.setWindowModality(Qt.ApplicationModal)
        self.newSyncDialog.exec_()
    def submitSyncForm(self,dialog,closeDialog=1,response=""):
        try:
            if self.t_syncName.text()=="" or self.t_syncName.text()==" ":
                self.testConAlert("Firstly fill name field!!")
                return

            sync_dict={self.t_syncName.text():{"ip":self.t_syncServer.text(),"syncUser":self.t_syncUser.text(),"syncPassword":self.t_syncPassword.text(),"syncPort":int(self.t_syncPort.text()),"lastSyncTime":"-1","remotePath":self.t_remotePath.text(),"os":self.c_syncOS.currentText()}}

            Sync.addSync(sync_dict)

            if closeDialog==1:
                dialog.close()
            if response!="":
                self.testConAlert(response=response)
        except Exception as e:
            self.testConAlert("Something Went Wrong. Please verify Credentials!!")
            log("Error_Window_submitParamForm@"+str(e))
    def manageRemoteSync(self):
          try:
              self.manageRemoteDialog = QDialog()
              lbox = QFormLayout()
              fbox=QFormLayout()
              vbox = QHBoxLayout()
              self.remoteList = QListWidget(self)
              #items = ['Item %s' % (i + 1) for i in range(10)]
              data=Json_evaluation.readJSON(filename=__syncFile__)
              for con in data.keys():
                  self.remoteList.addItem(str(con))
              lbox.addRow(self.remoteList)
              self.remoteList.itemClicked.connect(self.getRemoteBykey)
              fbox = QFormLayout()
              l_conName=QLabel("Remote Connection")
              self.t_remoteConName=QLineEdit()
              self.t_remoteConName.setEnabled(False)

              fbox.addRow(l_conName,self.t_remoteConName)
              self.b_installWilldo = QPushButton("Install over remote")
              self.b_uninstalWilldo = QPushButton("uninstall over remote")
              self.b_installWilldo.clicked.connect(partial(self.execRemoteCmd,cmd=4))
              self.b_uninstalWilldo.clicked.connect(partial(self.execRemoteCmd,cmd=5))
              fbox.addRow(self.b_installWilldo,self.b_uninstalWilldo)
              self.b_startScheduler = QPushButton("Start Scheduler")
              self.b_stopScheduler = QPushButton("Stop Scheduler")

              fbox.addRow(self.b_startScheduler,self.b_stopScheduler)
              self.b_startWebServer = QPushButton("Start Web Server")
              self.b_stopWebServer = QPushButton("Stop Web Server")

              fbox.addRow(self.b_startWebServer,self.b_stopWebServer)
              self.b_remoteSync = QPushButton("Remote Sync")
              self.b_remoteSync.clicked.connect(partial(self.execRemoteCmd,cmd=1))

              self.b_startScheduler.clicked.connect(partial(self.execRemoteCmd,cmd=2))
              self.b_stopScheduler.clicked.connect(partial(self.execRemoteCmd,cmd=3))
              
              self.b_startWebServer.clicked.connect(partial(self.execRemoteCmd,cmd=7))
              self.b_stopWebServer.clicked.connect(partial(self.execRemoteCmd,cmd=8))
              self.b_remoteLog = QPushButton("View remote log")

              fbox.addRow(self.b_remoteSync,self.b_remoteLog)
              self.b_remoteLog.clicked.connect(partial(self.execRemoteCmd,cmd=6))
              self.l_status=QLabel("Status")
              self.l_cmdStatus=QLabel("Idle")
              fbox.addRow(self.l_status,self.l_cmdStatus)

              b_create=QPushButton("Update")
              b_cancel=QPushButton("Delete")
              self.b_addStep=QPushButton("Add Step")
              self.b_addStep.setEnabled(False)
              #self.b_addStep.clicked.connect(partial(self.newStepDialog_m,self.t_jobName))
              fbox.addRow(self.b_addStep)
              fbox.addRow(b_create,b_cancel)
              b_cancel.clicked.connect(self.deleteJob)
              b_create.clicked.connect(partial(self.submitJob,dialog=self.manageRemoteDialog,closeDialog=0,response="Job updated successfully!!!"))
              fbox.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)

              vbox.addLayout(lbox)
              vbox.addLayout(fbox)
              self.manageRemoteDialog.setLayout(vbox)
              self.manageRemoteDialog.setWindowModality(Qt.ApplicationModal)
              self.manageRemoteDialog.setWindowTitle("Remote Sync")
              self.manageRemoteDialog.exec_()
          except Exception as e:
              log("Error_Window_manageJob@"+str(e))
    def getRemoteBykey(self):
        key=self.remoteList.currentItem().text()
        data=Json_evaluation.getJsonByKey(key=key,filename=__syncFile__)
        self.t_remoteConName.setText(key)
    def execRemoteCmd(self,cmd):
        data=Json_evaluation.getJsonByKey(key=self.t_remoteConName.text(),filename=__syncFile__)
        status=-1
        self.l_cmdStatus.setText("It will take a while. Please wait...... ")

        if cmd==1:
            status=Sync.remoteSyncCall(remote_dict=data)
            if status==1:
                self.testConAlert(response="Remote Syncronization complete successfully!!!")
        elif cmd==2:
            status=Sync.startScheduler(remote_dict=data)
            if status==1:
                self.testConAlert(response="Scheduler started successfully!!!")
        elif cmd==3:
            status=Sync.stopScheduler(remote_dict=data)
            if status==1:
                self.testConAlert(response="Scheduler stopped successfully!!!")
        elif cmd==4:
            status=Sync.installRemoteSSH(remote_dict=data)
            if status==1:
                self.testConAlert(response="Willdo installed successfully!!!")
        elif cmd==5:
            status=Sync.uninstallRemote(remote_dict=data)
            if status==1:
                self.testConAlert(response="Willdo uninstalled successfully!!!")
        elif cmd==6:
            #self.logReviewDialog(remote_dict=data)
            self.showLogReviewDialog(data)
        elif cmd==7:
            status=Sync.startWebServer(remote_dict=data)
            if status==1:
                self.testConAlert(response="WillDo Web Server started successfully!!!")
        elif cmd==8:
            status=Sync.stopWebServer(remote_dict=data)
            if status==1:
                self.testConAlert(response="WillDo Web Server stoped successfully!!!")




        if status==-1:
            self.testConAlert(response="Action abort due to any exception !!!")
    ###End Remote Syncronization

    ##Start Histoy # REVIEW:

    def showhistoryReviewDialog(self):
          self.historyReviewDialog = QDialog()
          lbox = QFormLayout()
          fbox=QFormLayout()
          vbox = QHBoxLayout()
          self.historyDock = QDockWidget("Job Name", self)
          self.jobListReview = QListWidget(self)
          #items = ['Item %s' % (i + 1) for i in range(10)]
          data=Json_evaluation.readJSON(filename=__jobFile__)
          for con in data.keys():
              self.jobListReview.addItem(str(con))


          self.historyDock.setWidget(self.jobListReview)
          self.historyDock.setFloating(True)
          self.historyReviewtext=QTextEdit()
          self.historyReviewtext.setReadOnly( True )
          #self.setCentralWidget(self.historyReviewtext)
          #self.historyReviewDialog.addDockWidget(Qt.LeftDockWidgetArea, self.historyDock)
          self.jobListReview.itemClicked.connect(self.getHistoryByJob)
          self.historyReviewtext.setMinimumHeight(700)
          self.historyReviewtext.setMinimumWidth(650)
          self.historyReviewtext.setText("<b>No Job is Selected!!</b>")
          lbox.addRow(self.historyReviewtext)
          vbox.addLayout(lbox)
          vbox.addWidget(self.historyDock)
          self.historyReviewDialog.setLayout(vbox)
          #b1.move(50,50)s
          #self.historyReviewDialog.setGeometry(100, 100, 750, 750)
          self.historyReviewDialog.setWindowTitle("Review Job's History")
          self.historyReviewDialog.setWindowModality(Qt.ApplicationModal)
          self.historyReviewDialog.exec_()


    def getHistoryByJob(self):
        #print(History.readJobHistory(self.jobListReview.currentItem().text()))
        self.historyReviewtext.setText(History.readJobHistory(jobName=self.jobListReview.currentItem().text()))


#*******End of historyDock

#****** Start of Remote Log ****************# IDEA:

    def showLogReviewDialog(self,remote_dict):
        self.logReviewDialog = QDialog()
        lbox = QFormLayout()
        fbox=QFormLayout()
        vbox = QHBoxLayout()

        self.historyDock = QDockWidget("Job Name", self)
        self.jobListReview = QListWidget(self)
        self.historyReviewtext=QTextEdit()
        self.historyReviewtext.setReadOnly( True )
        #items = ['Item %s' % (i + 1) for i in range(10)]

        path=Generic.replaceConnectorInPath(__installationDirName__+"/"+__logPath__+"/"+__logFile__)
        self.historyReviewtext.setText("Please Wait we are fetching from server...")
        savePath=Generic.replaceConnectorInPath(Generic.getCurrentPath()+"/"+__logPath__+"/"+__logFile__)
        remote_dict=Json_evaluation.getJsonByKey(filename=__syncFile__,key=globalRemoteName)
        logThread=threading.Thread(target=Sync.getFileFromRemoteAndSave,args=(remote_dict,path,savePath,Generic.getFileNameFromPath(path),))
        logThread.daemon=True
        logThread.start()
        time.sleep(15)
        #d=self.customAlert(response="Please Wait........"),

        #print(Json_evaluation.readFile(savePath))
        self.historyReviewtext.setText(Json_evaluation.readFile(savePath))



        #self.setCentralWidget(self.historyReviewtext)
        #self.logReviewDialog.addDockWidget(Qt.LeftDockWidgetArea, self.historyDock)

        self.historyReviewtext.setMinimumHeight(650)
        self.historyReviewtext.setMinimumWidth(800)
        lbox.addRow(self.historyReviewtext)
        vbox.addLayout(lbox)

        self.logReviewDialog.setLayout(vbox)
        #b1.move(50,50)s
        #self.logReviewDialog.setGeometry(100, 100, 750, 750)
        self.logReviewDialog.setWindowTitle("Willdo Log Review")
        self.logReviewDialog.setWindowModality(Qt.ApplicationModal)
        self.logReviewDialog.exec_()
        d.close()
#********************************* End of Remote Log ****************# IDEA

    def customAlert(self,response):

        d = QDialog()
        d.setWindowTitle("Alert")
        l_response=QLabel(response)
        fbox = QFormLayout()
        fbox.addRow(l_response)
        #b_OK=QPushButton("OK");
        #b_OK.setMaximumSize(QSize(40, 40))
        #b_OK.clicked.connect(d.close)
        #fbox.addRow(b_OK)
        d.setLayout(fbox)
        d.setWindowModality(Qt.ApplicationModal)
        d.exec_()
        return d





if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
