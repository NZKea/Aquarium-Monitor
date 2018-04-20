import sqlite3
import time
import datetime
import os
import datetime
from datetime import timedelta
def monthdeltab(date, delta):
    m, y= (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)



def graph():
    x=0
    temperature=26
    comma=""
    finaldate=datetime.datetime.now()
    finaldate=monthdeltab(finaldate, -1)
    d = finaldate - timedelta(days=1)
    w = finaldate - timedelta(days=7)
    #finaldate=finaldate.strftime('%Y,%m,%d,%H,%M')
    # finaldate=str(finaldate)
    conn = sqlite3.connect("main.db")
    c = conn.cursor()
    c.execute("INSERT INTO main VALUES (?,?)",(finaldate,temperature))
    c.execute('SELECT * FROM main')
    alltime = c.fetchall()
    c.execute("SELECT * FROM main where datetime(Date) >= ?",(d,))
    day= c.fetchall()
    c.execute("SELECT * FROM main where datetime(Date) >= ?",(w,))
    week= c.fetchall()

    with open('chart1D.js','w') as chart:
        chart.write("var dataPointsA=[")
        for row in alltime:
            reading= alltime[x]
            time= reading[0]
            temp= reading[1]
            chart.write(comma+"{ x: new Date("+str(time)+"), y:"+str(temp)+" }")
            comma=","
            x= x+1
        chart.write("];")
        x=0
        comma=""
        chart.write("var dataPointsD=[")
        for row in day:
            reading= day[x]
            time= reading[0]
            temp= reading[1]
            chart.write(comma+"{ x: new Date("+str(time)+"), y:"+str(temp)+" }")
            comma=","
            x= x+1
        chart.write("];")
        x=0
        comma=""
        chart.write("var dataPointsW=[")
        for row in week:
            reading= week[x]
            time= reading[0]
            temp= reading[1]
            chart.write(comma+"{ x: new Date("+str(time)+"), y:"+str(temp)+" }")
            comma=","
            x= x+1
        chart.write("];")
        chart.closed
        conn.close()
    print("Reading Recorded")


graph()

#https://www.sqlite.org/lang_datefunc.html
