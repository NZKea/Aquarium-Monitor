from w1thermsensor import W1ThermSensor
import sqlite3
import time
import Adafruit_CharLCD as LCD
import datetime
import os

# Raspberry Pi pin configuration:
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 21
lcd_d7        = 22
#No backlight pin

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2


# Initialize the LCD using the pins above.
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows)
#Run LCD
def printlcd(temperature):
        lcd.clear()
        lcd.message("Temperature Now:\n" +str(temperature)+" C")



def monthdeltab(date, delta):
    m, y= (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)

#Record Temp in database
def datarecord(temperature):
    conn = sqlite3.connect("main.db")
    c = conn.cursor()
    #c.execute('''CREATE TABLE main
     #       (date text,temp real)''')

    #Grabs Current Time and formats it
    finaldate=datetime.datetime.now()
    finaldate=monthdeltab(finaldate, -1)
    finaldate=finaldate.strftime('%Y,%m,%d,%H,%M')
    c.execute("INSERT INTO main VALUES (?,?)",(finaldate,temperature))
    conn.commit()
    conn.close()


def graph():
    x=0
    comma=""

    finaldate=datetime.datetime.now()
    finaldate=monthdeltab(finaldate, -1)
    d = finaldate - timedelta(days=1)
    w = finaldate - timedelta(days=7)
    d=d.strftime('%Y,%m,%d,%H,%M')
    w=w.strftime('%Y,%m,%d,%H,%M')
    
    conn = sqlite3.connect("main.db")
    c = conn.cursor()
    c.execute('SELECT * FROM main')
    alltime = c.fetchall()
    c.execute("SELECT * FROM main where Date >= ?",(d,))
    day= c.fetchall()
    c.execute("SELECT * FROM main where Date >= ?",(w,))
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
#Main Loop
while True:
    sensor = W1ThermSensor()
    temperature_in_celsius = sensor.get_temperature()
    temperature= round(temperature_in_celsius,2)
    datarecord(temperature)
    printlcd(temperature)
    graph()
    time.sleep(120)
