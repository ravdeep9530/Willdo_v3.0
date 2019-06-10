from PyQt5.QtWidgets import QApplication,  QAction, QMenu,QMainWindow,QMessageBox
class Menu:


    def loadMenu(self,w):
        self.w=w
        menubar = w.menuBar()
        jobMenu = menubar.addMenu('Jobs')
        newJob = QAction('New Job', w)
        newJob.setShortcut('Ctrl+N')
        newJob.setStatusTip('Create a new job.')
        newJob.triggered.connect(w.createNewJob)
        manageJobs = QAction('Manage Jobs', w)
        manageJobs.setShortcut('Ctrl+M')
        manageJobs.setStatusTip('Edit your jobs')
        manageJobs.triggered.connect(w.manageJobs)
        jobMenu.addAction(newJob)
        jobMenu.addAction(manageJobs)

        conMenu=menubar.addMenu("Connections")
        newCon=QAction("New Connection",w)
        newCon.setShortcut('ctrl+C')
        newCon.setStatusTip("Create a new connection")
        newCon.triggered.connect(w.showCreateNewCondialog)
        conMenu.addAction(newCon)
        manageCon=QAction("Manage Connection",w)
        manageCon.setShortcut('ctrl+D')
        manageCon.setStatusTip("Edit connections")
        manageCon.triggered.connect(w.manageCondialog)
        conMenu.addAction(manageCon)

        emailMenu = menubar.addMenu('Email')
        newSmpt = QAction('New SMPT', w)
        newSmpt.setShortcut('Ctrl+E')
        newSmpt.setStatusTip('Create new SMPT setup.')
        newSmpt.triggered.connect(w.createNewSmpt)
        emailMenu.addAction(newSmpt)

        paramMenu = menubar.addMenu('Parameters')
        newParam = QAction('New Parameter', w)
        newParam.setShortcut('Ctrl+P')
        newParam.setStatusTip('Create new Parameter.')
        newParam.triggered.connect(w.createNewParam)
        paramMenu.addAction(newParam)

        syncMenu = menubar.addMenu('Remote Sync')
        newRemote = QAction('New Remote', w)
        newRemote.setShortcut('Ctrl+R')
        newRemote.setStatusTip('Connect with new remote.')
        newRemote.triggered.connect(w.createNewSync)
        syncMenu.addAction(newRemote)
        syncRemote = QAction('Sync Remote', w)
        syncRemote.setShortcut('Ctrl+S')
        syncRemote.setStatusTip('Sync remote.')
        syncRemote.triggered.connect(w.manageRemote)
        syncMenu.addAction(syncRemote)

        #History menuBar
        historyMenu = menubar.addMenu('History')
        history = QAction('Review History', w)
        history.setShortcut('Ctrl+H')
        history.setStatusTip('Click here to Review History.')
        history.triggered.connect(w.reviewHistory)
        historyMenu.addAction(history)





        #impMenu = QMenu('Import', w)
        #impAct = QAction('Import mail', w)
        #impMenu.addAction(impAct)

        #newAct = QAction('New', w)

        #newJobMenu.addAction('',self.newJobMenuAction(w))
        #newJobMenu.triggered[QAction].connect(Menu().newJobMenuAction)
        #fileMenu.addMenu(impMenu)
    def newJobMenuAction(a):
        print("s")
