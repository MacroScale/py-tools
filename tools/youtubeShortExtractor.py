from config.db import DB

db = DB();

def grabData():
    print("grabbing data")

def processData():
    print("processing data")

def saveToDb():
    print("saving data to db")

def dbTest():
    result = db.execute("select * from \"beam-demo\".users")
    print(result)

dbTest()
