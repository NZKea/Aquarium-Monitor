import sqlite3
import time
import datetime
import os
def graph():
    x=0
    comma=""
    conn = sqlite3.connect("main.db")
    c = conn.cursor()
    c.execute('SELECT * FROM main')
    alltime = c.fetchall()
    c.execute("SELECT * FROM main where Date <= strftime('%d,%m,%Y,%H,%M,%S',datetime('now','-24 hours'))")
    day= c.fetchall()
    c.execute("SELECT * FROM main where Date <= strftime('%d,%m,%Y,%H,%M,%S',datetime('now','-20 days'))")
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
