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
        job={self.t_jobName.text():{"conName":self.c_conName.currentText(),"jobStatement":"","interval":self.c_interval.currentData(),"scheuledTime":self.t_scheduledTime.time().toString("HH:mm"),"description":self.t_description.text(),"type":"","startDate":self.t_startDate.date().toString("dd/MM/yyyy"),"endDate":self.t_endDate.date().toString("dd/MM/yyyy"),"isActive":1,"lastRunDate":"-1"}}
        Job.setJob(job)
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
