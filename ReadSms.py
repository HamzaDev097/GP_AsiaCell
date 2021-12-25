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

def GetPhoneNumber(sms): 
    a = ""
    for i in range(10, -1, -1):
        if(len(sms)==140):
            a+= sms[140-78-i]
        elif (len(sms)==139):
            a+= sms[140-79-i]
    return a
def GetAmount(sms):
    a = ""
    for i in range(14):
        if (sms[i]!=' '):
            a+= sms[i]
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

        for i in range(40):
            
            if (Musg["response"]["Messages"]["Message"][i]["Phone"] == "Asiacell"):
                #print(len(Musg["response"]["Messages"]["Message"][i]["Content"])==140 or  len((Musg["response"]["Messages"]["Message"][i]["Content"]))==139)
                if(len(Musg["response"]["Messages"]["Message"][i]["Content"])==140  or len((Musg["response"]["Messages"]["Message"][i]["Content"]))==139):
                    #print(Musg["response"]["Messages"]["Message"][i]["Content"]+"\n\n")
                    sms = Musg["response"]["Messages"]["Message"][i]["Content"]
                    amount = GetAmount(sms)
                    phone = GetPhoneNumber(sms)
                    ip = x[0]
                    date = Musg["response"]["Messages"]["Message"][i]["Date"]
                    mycursor = mydb.cursor()
                    mycursor.execute("SELECT * FROM  `transfer_sms` WHERE `mifi_ip` = " +str(ip)+" AND `date` = '"+str(date)+"'")
                    myresult = mycursor.fetchall()
                    
                    if(len(myresult)==0):
                        sql = "INSERT INTO `transfer_sms` (`phone`, `amount`, `date`, `mifi_ip`,`Content`) VALUES (%s, %s,%s, %s, %s)"
                        val = (phone, amount,date,ip,sms)
                        mycursor.execute(sql, val)
                        mydb.commit()
                        print("One Value Inserted")
