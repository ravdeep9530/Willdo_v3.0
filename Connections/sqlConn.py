#!/usr/bin/python3
import sys
sys.path.insert(0,'../')
import pymysql
import pymssql
import xml.sax
from include.Variable import __guidePath__,__connectionFile__
from Json_evaluation import Json_evaluation,log

#con=pymysql.connect('94.156.144.217','hotel',
#    'indian12',
#    'hotels',charset='utf8',
 #  use_unicode=True
#)
def connection(con_name=""):
    data=Json_evaluation.readJSON(__guidePath__,__connectionFile__)
    if data[con_name]["connType"]=="MySql":

        try:
            con=pymysql.connect(data[con_name]["server"],data[con_name]["user"],data[con_name]["password"],data[con_name]["database"],charset=data[con_name]["charset"],use_unicode=data[con_name]["use_unicode"],
            port=data[con_name]["port"])
        except Exception as e:
            log("Error_sqlConn_mySQLCon@"+e)
        return con
    elif data[con_name]["connType"]=="MS Sql Server":
        data=Json_evaluation.readJSON(__guidePath__,__connectionFile__)
        try:
            con=pymssql.connect(data[con_name]["server"],data[con_name]["user"],data[con_name]["password"],data[con_name]["database"],
            port=data[con_name]["port"])
        except Exception as e:
            log("Error_sqlConn_msSQLCon@"+e)
        return con
def executeSql(con,q="Select 'Willdo'",isProc=0):
    try:
        result=[]
        #con.execute('EXEC S_Daily_Executeshell_workspace')
        #con.execute_(q)
        con.autocommit(True)
        cur = con.cursor()
        #cur.execute('EXEC S_Daily_Executeshell_workspace;')

        #con.execute_row('EXEC S_Daily_Executeshell_workspace;')

        if isProc==4:
            q=q.split(' ')
            if len(q)>1:
                procName=q[0]
                parm=tuple(q[1].split(','))
                cur.callproc(procName,parm)
            else:
                cur.execute(q[0])
        else:
            #print('here')
            result=cur.execute(q)
        try:
            row = cur.fetchone()
            while row is not None:
                result.insert(0,row)
                row = cur.fetchone()
        except Exception as e:
            log("WARNING: "+str(e))
        con.commit()
        cur.close()
        con.close()
        #print(result)

        return result
    except Exception as e:
        log("Error_sqlConn_executeSql@"+e)
        return -1
