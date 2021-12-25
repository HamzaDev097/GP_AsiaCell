import huaweisms.api.user
import huaweisms.api.sms
from flask import Flask,request
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  database="asiacell-gp"
)

app = Flask(__name__)

@app.route('/buy',methods=["GET"])
def Buy():
    arges = dict(request.args)
    if len(arges) ==3:
        amount = str(arges.get("amount"))
        phone = str(arges.get("phone"))
        ip = str(arges.get("ip"))
        ctx = huaweisms.api.user.quick_login("asiacell", "asiacell",modem_host='192.168.'+ip+'.1')
        a = huaweisms.api.sms.send_sms(ctx, "222", amount+','+phone)
        return "Done"
    else:
        return "Error"

@app.route('/get_sms',methods=["GET"])
def GetSms():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM  `transfer_sms`")
    myresult = mycursor.fetchall()
    return str(myresult)

@app.route('/get_device',methods=["GET"])
def GetDevice():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM  `Sims`")
    myresult = mycursor.fetchall()
    return str(myresult)



if __name__ == '__main__':
    app.run()