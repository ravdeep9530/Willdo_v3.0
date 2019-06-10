from Json_evaluation import Json_evaluation,log
from include.Variable import __syncFile__,__webServerStopCmd__,__webServerSeachCmd__,__webServerStartCmd__,__webServerStartFile__,__installationDirName__,__linuxInstallationPath__,__guidePath__,__logPath__,__storagePath__,__logFile__,__schedulerSeachCmd__,__schedulerStopCmd__,__schedulerStartCmd__,__schedulerServiceName__,__uninstallRemoteCmd__
from paramiko import SSHClient
import paramiko,socket
from Generic import Generic
import os
#from scp import SCPClient
pathConnector=Generic.getPathConnector()

class Sync:
    def addSync(sync_dict):
        try:
            Json_evaluation.updateJson(dict=sync_dict,filename=__syncFile__)
            log("Adding "+str(sync_dict.keys())+" Parameter ")
            pass
        except Exception as e:
            log("Error_Sync_addSync@"+str(e))
    def sshCall(remote_dict):
        try:
            log("SSH Connecting.....")
            ssh = SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            try:
                success=ssh.connect(hostname=remote_dict["ip"],port=int(remote_dict["syncPort"]),username=remote_dict["syncUser"], password=remote_dict["syncPassword"],timeout=20)
                if success==True:
                    log("SSH connected")
            except paramiko.AuthenticationException  as e:
                log("Error_Sync_AuthenticationException@"+str(e))
                #print("connected")

            return ssh
        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteSyncCall@"+str(e))

    def installRemoteSSH(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            ftp_client=ssh.open_sftp()
            log("Willdo Installation started.......")
            try:
                #stdin, stdout, stderr = ssh.exec_command("rm -r "+__installationDirName__+pathConnector+__guidePath__)
                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_Dir_already exists@"+str(e))
            thisdir = os.getcwd()
            dir_list=None
            tr_dir={}
            t=1
            f_t=0

            for r, d, f in os.walk(thisdir):
                
                #for file in f:
                #if ".docx" in file:
                #    print(os.path.join(r, file))
                if dir_list is None:
                    dir_list=d
                r_dir=r.split(pathConnector)
                s_dir=""
                if t==3 and f_t==0:
                    t-=1
                    f_t=1
                
                for a in range(1,t):
                    s_dir+=pathConnector+r_dir[len(r_dir)-(t-a)]


                #print(d)
                for dir in d:
                    try:
                        #tr_dir[dir]={t}
                        #print(tr_dir)
                        #print(__installationDirName__+s_dir+pathConnector+dir)
                        ftp_client.mkdir(__installationDirName__+s_dir+pathConnector+dir)
                        log(__installationDirName__+s_dir+pathConnector+dir+" is created")
                        flag=1
                    except IOError as e:
                        log("Error_Sync_Dir_already exists@"+str(e))
                if len(d)>0:
                    t+=1
                for file in f:
                #if ".docx" in file:
                    r_dir=r.split(pathConnector)
                    r_dir=r_dir[len(r_dir)-1]

                    if r_dir in dir_list:
                    #if r_dir=="scheduler_guide":
                        try:
                            #print(str(os.path.join(r, file)),__installationDirName__+pathConnector+r_dir+pathConnector+file)
                            ftp_client.put(str(os.path.join(r, file)),__installationDirName__+pathConnector+r_dir+pathConnector+file)
                            log(__installationDirName__+pathConnector+r_dir+pathConnector+file+" is created")
                        except IOError as e:
                            log("Error_Sync_File_already exists@"+str(e))
                    else:
                        try:
                            print(str(os.path.join(r, file)),__installationDirName__+s_dir+pathConnector+file)
                            ftp_client.put(str(os.path.join(r, file)),__installationDirName__+s_dir+pathConnector+file)
                            log(__installationDirName__+s_dir+pathConnector+file+" is created")
                        except IOError as e:
                            log("Error_Sync_File_already exists@"+str(e))
                        #print(str(os.path.join(r, file))+"-----------"+r_dir+"   "+__installationDirName__+pathConnector+file)

                    #ftp_client.put(os.path.join(r, file),"/var/www/pp.png")
            #ftp_client.put("/home/worldwiki/Desktop/willDO/FileStorage/2019-04-30_14.31.49.434702_2x92dp.png","/var/www/pp.png")
            #stdin, stdout, stderr = ssh.exec_command(__installationDirName__+"/setup.sh")
            #print ("stderr: "+stderr.readlines())
            #print ("pwd: "+stdout.readlines())
            print(tr_dir)
            ftp_client.close()
        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_connectRemoteSSH@"+str(e))
    def remoteSyncCall(remote_dict):
        try:
            remotePathConnector=Generic.getRemotePathConnector(remote_dict)
            ssh=Sync.sshCall(remote_dict)
            ftp_client=ssh.open_sftp()
            try:
                stdin, stdout, stderr = ssh.exec_command("rm -r "+__installationDirName__+remotePathConnector+__guidePath__)
                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_Dir_already exists@"+str(e))
            thisdir = os.getcwd()
            dir_list=None
            for r, d, f in os.walk(thisdir):
                #for file in f:
                #if ".docx" in file:
                #    print(os.path.join(r, file))
                if dir_list is None:
                    dir_list=d

                for dir in d:
                    try:
                        if dir=="scheduler_guide":
                            ftp_client.mkdir(__installationDirName__+remotePathConnector+dir)
                            log(__installationDirName__+remotePathConnector+dir+" is created")
                    except IOError as e:
                        log("Error_Sync_Dir_already exists@"+str(e))
                for file in f:
                #if ".docx" in file:
                    r_dir=r.split(pathConnector)
                    r_dir=r_dir[len(r_dir)-1]
                    log(r_dir)
                    #if r_dir in dir_list:
                    if r_dir=="scheduler_guide":
                        try:
                            ftp_client.put(str(os.path.join(r, file)),__installationDirName__+remotePathConnector+r_dir+remotePathConnector+file)
                            log(__installationDirName__+remotePathConnector+r_dir+remotePathConnector+file+" is created")
                        except IOError as e:
                            log("Error_Sync_File_already exists@"+str(e))

                        #print(str(os.path.join(r, file))+"-----------"+r_dir+"   "+__installationDirName__+pathConnector+file)

                    #ftp_client.put(os.path.join(r, file),"/var/www/pp.png")
            #ftp_client.put("/home/worldwiki/Desktop/willDO/FileStorage/2019-04-30_14.31.49.434702_2x92dp.png","/var/www/pp.png")
            #stdin, stdout, stderr = ssh.exec_command(__installationDirName__+"/setup.sh")
            #print ("stderr: "+stderr.readlines())
            #print ("pwd: "+stdout.readlines())
            ftp_client.close()
            return 1
        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteSyncCall@"+str(e))
            return -1
    def remoteSearchSchedulerCall(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            try:
                stdin, stdout, stderr = ssh.exec_command(__schedulerSeachCmd__)
                output=stdout.read().decode("utf-8")
                output=str(output).split('\n')
                return output


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_CmdError@"+str(e))
                return -1



        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteSearchSchedulerCall@"+str(e))
            return -1
    def uninstallRemote(remote_dict):
        try:
            Sync.stopScheduler(remote_dict)
            ssh=Sync.sshCall(remote_dict)
            try:
                stdin, stdout, stderr = ssh.exec_command(__uninstallRemoteCmd__)
                log("Sync_uninstallRemote@cmdResult_"+stdout.read().decode("utf-8"))

                return 1


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_CmdError@"+str(e))
                return -1



        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_uninstallRemote@"+str(e))
            return -1
    def stopScheduler(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            #ftp_client=ssh.open_sftp()
            try:

                for o in Sync.remoteSearchSchedulerCall(remote_dict):
                    stdin, stdout, stderr = ssh.exec_command(__schedulerStopCmd__.replace('#pid',o))


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
                return 1
            except (IOError,Exception) as e:
                log("Error_Sync_stopScheduler_CmdError@"+str(e))


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_stopScheduler@"+str(e))
            return -1
    def startScheduler(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            #ftp_client=ssh.open_sftp()

            try:
                stdin, stdout, stderr = ssh.exec_command(__schedulerStartCmd__.replace('#path',"./"+__schedulerServiceName__))
                #stdin, stdout, stderr =ssh.exec_command("ls")
                #print(stdout.read())



                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
                return 1
            except (IOError,Exception) as e:
                log("Error_Sync_stopScheduler_CmdError@"+str(e))


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_stopScheduler@"+str(e))
            return -1
    def startWebServer(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            #ftp_client=ssh.open_sftp()

            try:
                #print(__webServerStartCmd__.replace('#path',"./"+__webServerStartFile__))
                stdin, stdout, stderr = ssh.exec_command(__webServerStartCmd__.replace('#path',"./"+__webServerStartFile__))
                #stdin, stdout, stderr =ssh.exec_command("ls")
                #print(stdout.read())



                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
                return 1
            except (IOError,Exception) as e:
                log("Error_Sync_stopScheduler_CmdError@"+str(e))


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_stopScheduler@"+str(e))
            return -1
    def remoteSearchWebServerCall(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            try:
                stdin, stdout, stderr = ssh.exec_command(__webServerSeachCmd__)
                output=stdout.read().decode("utf-8")
                output=str(output).split('\n')
                return output


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_CmdError@"+str(e))
                return -1



        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteSearchSchedulerCall@"+str(e))
            return -1
    def stopWebServer(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            #ftp_client=ssh.open_sftp()
            try:

                for o in Sync.remoteSearchWebServerCall(remote_dict):
                    stdin, stdout, stderr = ssh.exec_command(__webServerStopCmd__.replace('#pid',o))


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
                return 1
            except (IOError,Exception) as e:
                log("Error_Sync_stopScheduler_CmdError@"+str(e))


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_stopScheduler@"+str(e))
            return -1
    def remoteSearchSchedulerCall(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            try:
                stdin, stdout, stderr = ssh.exec_command(__schedulerSeachCmd__)
                output=stdout.read().decode("utf-8")
                output=str(output).split('\n')
                return output


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_CmdError@"+str(e))
                return -1



        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteSearchSchedulerCall@"+str(e))
            return -1
    def uninstallRemote(remote_dict):
        try:
            Sync.stopScheduler(remote_dict)
            ssh=Sync.sshCall(remote_dict)
            try:
                stdin, stdout, stderr = ssh.exec_command(__uninstallRemoteCmd__)
                log("Sync_uninstallRemote@cmdResult_"+stdout.read().decode("utf-8"))

                return 1


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
            except IOError as e:
                log("Error_Sync_CmdError@"+str(e))
                return -1



        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_uninstallRemote@"+str(e))
            return -1
    def stopScheduler(remote_dict):
        try:
            ssh=Sync.sshCall(remote_dict)
            #ftp_client=ssh.open_sftp()
            try:

                for o in Sync.remoteSearchSchedulerCall(remote_dict):
                    stdin, stdout, stderr = ssh.exec_command(__schedulerStopCmd__.replace('#pid',o))


                #ftp_client.get(__installationDirName__+pathConnector+__logPath__+pathConnector+__logFile__,"log.txt")

                #ftp_client.mkdir(__installationDirName__)
                return 1
            except (IOError,Exception) as e:
                log("Error_Sync_stopScheduler_CmdError@"+str(e))


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_stopScheduler@"+str(e))
            return -1
    def getFileFromRemote(remote_dict,remoteFilePath,filename):
        try:
            ssh=Sync.sshCall(remote_dict)
            ftp_client=ssh.open_sftp()

            try:

                ftp_client.get(remoteFilePath,Generic.getCurrentPath()+pathConnector+__storagePath__+pathConnector+filename)

                #ftp_client.mkdir(__installationDirName__)
                return str(Generic.getCurrentPath()+pathConnector+__storagePath__+pathConnector+filename)
            except (IOError,Exception) as e:
                log("Error_Sync_getFileFromRemote_CmdError@"+str(e))


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteName@"+str(e))
            return -1

    def getFileFromRemoteAndSave(remote_dict,remoteFilePath,saveFilePath,filename):
        try:
            ssh=Sync.sshCall(remote_dict)
            ftp_client=ssh.open_sftp()

            try:

                ftp_client.get(remoteFilePath,saveFilePath)

                #ftp_client.mkdir(__installationDirName__)
                return str(Generic.getCurrentPath()+pathConnector+__storagePath__+pathConnector+filename)
            except (IOError,Exception) as e:
                log("Error_Sync_getFileFromRemote_CmdError@"+str(e))
                return -1


        except (Exception,paramiko.SSHException,paramiko.AuthenticationException,paramiko.BadHostKeyException,socket.error)  as e:
            log("Error_Sync_remoteName@"+str(e))
            return -1
