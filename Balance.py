import huaweisms.api.user
import huaweisms.api.wlan
import huaweisms.api.sms
import time
from time import strftime,gmtime
import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="asiacell-gp"
)


def ReFormat(msg):
    a = ""
    for i in range (20):
        if msg[i+16]!= ' ':
            if msg[i+16]!=',':
                a+= msg[i+16]
        else:
            break
    return a

while True:
    time.sleep(1)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM sims")
    myresult = mycursor.fetchall()
    for x in myresult:
        ctx = huaweisms.api.user.quick_login("asiacell", "asiacell",modem_host='192.168.'+str(x[0])+'.1')
        Musg = huaweisms.api.sms.get_sms(ctx,qty=40)
        for i in range(len(Musg)):
            if (Musg["response"]["Messages"]["Message"][i]["Phone"] == "Asiacell"):
                if(len(Musg["response"]["Messages"]["Message"][i]["Content"])>45 and len((Musg["response"]["Messages"]["Message"][i]["Content"]))<53):
                    strdate = Musg["response"]["Messages"]["Message"][i]["Date"]
                    datetimeobj=datetime.datetime.strptime(strdate, "%Y-%m-%d %H:%M:%S")
                    if(x[3]<datetimeobj):
                        new_balece = ReFormat(Musg["response"]["Messages"]["Message"][i]["Content"])
                        sql = "UPDATE sims SET `balance` = "+str(new_balece)+" , `last_update_for_balance` =  '"+str(strdate)+"'  WHERE ip = "+str(x[0])
                        print(Musg["response"]["Messages"]["Message"][i]["Content"])
                        mycursor.execute(sql)
                        mydb.commit()