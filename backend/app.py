import pymysql
import uuid
import bcrypt

endpoint = "test-database.crkwdx8kqlsw.us-east-2.rds.amazonaws.com"
username = "admin"
password = "password6969"

database_name = "airpark"

connection = pymysql.connect(endpoint, user=username, passwd=password, db= database_name)

cursor = connection.cursor()
import datetime

def register(email, username, password):
    cursor.execute("SELECT * from users where email like \"" + email + "\"")
    results = list(cursor.fetchall())
    if results == []:
        try:
            hashp = str(bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()))
            userid = str(uuid.uuid1())
            cursor.execute("insert into users (id, email, username, pwd) values (\"" + userid + "\", \"" + email + "\", \"" + username + "\", \"" + hashp[2:len(hashp) - 1] + "\")")
            connection.commit()
            return {"status": "success"}

        except:
            return {"status":"unknown error"}
    else:
        return {"status":"failed", "error":"This email already exists."}

def login(email, password):
    try:
        cursor.execute("SELECT * from users where email like \"" + email + "\"")
        k = list(cursor.fetchall())[0]
        pwd = k[3]
        x = str(bcrypt.hashpw(password.encode('utf-8'), pwd.encode('utf-8')))
        x = x[2:len(x) - 1]

        if x == pwd:
            return {"status":"success", "userd":str(k[0])}
        else:
            return {"status":"failed"}
    except:
        return {"status":"failed"}

def create_spot(name, address, message, userid, price, lat, lon):
    try:
        spot_id = str(uuid.uuid1())
        command = "insert into spots (spotid, userid, spot_name, lat, lon, address, message, price) values (\"" + spot_id + "\", \"" + userid + "\", \"" + name + "\", " + str(lat) + ", " + str(lon) + ", \"" + address + "\", \"" + message + "\", " + str(price) + ");"
        cursor.execute(command)
        connection.commit()
        return {"status":"success"}
    except:
        return {"status":"failed"}
    

def get_spots(userid):
    try:
        command = "select * from spots where userid like \"" + userid + "\""
        cursor.execute(command)
        final = []
        for i in list(cursor.fetchall()):
            final.append(list(i))
        return {"status":"success", "spots":final}
    except:
        return {"status":"failed"}

def create_temp(spotid, date, start_time, end_time):
    try:
        rent_id = str(uuid.uuid1())
        command = "insert into temp (rent_id, spotid, rent_date, start_time, end_time, claimed, claimed_id) values (\"" + rent_id + "\" , \"" + spotid + "\", \"" +  date + "\", " + str(start_time) + ", " + str(end_time) + ", 0, \"\");"  
        cursor.execute(command)
        connection.commit()
        return {"status":"success"}

    except:
        return {"status":"failed"}

def create_weekly(spotid, day, start_time, end_time):
    try:
        rent_id = str(uuid.uuid1())
        command = "insert into weekly (rent_id, spotid, rent_day, start_time, end_time, claimed, claimed_id) values (\"" + rent_id + "\" , \"" + spotid + "\","  +  str(day) + ", " + str(start_time) + ", " + str(end_time) + ", 0, \"\");"  
        cursor.execute(command)
        connection.commit()
        return {"status":"success"}

    except:
        return {"status":"failed"}

def get_calendar(spot_id, date):
    try:
        k = list(map(int, date.split("-")))
        day = datetime.datetime(k[0], k[1], k[2]).weekday()
        final = []
        command = "select * from temp where rent_date = \"" + date + "\""
        cursor.execute(command)
        final += list(cursor.fetchall())
        command1 = "select * from weekly where rent_day = " + str(day) 
        cursor.execute(command1)
        final += list(cursor.fetchall())
        final = sorted(final,key=lambda l:l[3])
        ff = []
        for i in final:
            if i[1] == spot_id:
                ff.append(list(i))
        return {"status":"success", "data":ff}
    except:
        return {"status":"failed"}


def claim(userid, rentid):

    try:
        command = "select * from temp where rent_id = \"" + rentid + "\""
        cursor.execute(command)
        if list(cursor.fetchall()) != []:
            command = "update temp\nset claimed_id = \"" + userid + "\", claimed = 1\nwhere rent_id = \"" + rentid + "\""
            cursor.execute(command)
            connection.commit()
            return {"status":"success"}
        else:
            command = "update weekly\nset claimed_id = \"" + userid + "\", claimed = 1\nwhere rent_id = \"" + rentid + "\""
            cursor.execute(command)
            connection.commit()
            return {"status":"success"}
    except:
        return {"status":"failed"}
    
def checkout(rentid):

    try:
        command = "select * from temp where rent_id = \"" + rentid + "\""
        cursor.execute(command)
        if list(cursor.fetchall()) != []:
            command = "update temp\nset claimed_id = \"" + "\", claimed = 0\nwhere rent_id = \"" + rentid + "\""
            cursor.execute(command)
            connection.commit()
            return {"status":"success"}
        else:
            command = "update weekly\nset claimed_id = \"" + "\", claimed = 0\nwhere rent_id = \"" + rentid + "\""
            cursor.execute(command)
            connection.commit()
            return {"status":"success"}
    except:
        return {"status":"failed"}

def search(date, lat, lon):
    try:
        k = list(map(int, date.split("-")))
        day = datetime.datetime(k[0], k[1], k[2]).weekday()
        final = []
        command = "select * from temp where rent_date = \"" + date + "\""
        cursor.execute(command)
        final += list(cursor.fetchall())
        command1 = "select * from weekly where rent_day = " + str(day) 
        cursor.execute(command1)
        final += list(cursor.fetchall())
        ff = []
        for i in final:
            command2 = "select * from spots where spotid = \"" + str(i[1]) + "\""
            cursor.execute(command2)
            x = list(list(cursor.fetchall())[0])
            if abs(lat - x[3]) + abs(lon - x[4]) < 0.04:
                ff.append(list(i))
        
        return {"status":"success", "data":ff}
    except:
        return {"status":"failed"}

def textsearch(q, date):
    try:
        k = list(map(int, date.split("-")))
        day = datetime.datetime(k[0], k[1], k[2]).weekday()
        final = []
        command = "select * from temp where rent_date = \"" + date + "\""
        cursor.execute(command)
        final += list(cursor.fetchall())
        command1 = "select * from weekly where rent_day = " + str(day) 
        cursor.execute(command1)
        final += list(cursor.fetchall())
        ff = []
        for i in final:
            command2 = "select * from spots where spotid = \"" + str(i[1]) + "\""
            cursor.execute(command2)
            x = list(list(cursor.fetchall())[0])
            if q.lower() in x[5].lower():
                ff.append(list(i))
        
        return {"status":"success", "data":ff}
    except:
        return {"status":"failed"}

# print(claim("1234", "23dec50c-fa78-11ea-9211-00f48da26548"))

# print(get_calendar("1234", "2020-09-19"))

# print(create_temp("1234", "2020-09-19", 500, 1000))
# print(create_spot("Office parking spot", "Indiranagar, Bangalore", "Spot number 10", "1234", 1, 10.02, 10.3))