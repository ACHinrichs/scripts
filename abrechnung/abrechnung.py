#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call
import datetime

import config_private as config

print("Erstelle die Abrechnung")

monate = ["","Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober","November","Dezember"]
tage = ["","Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
month = int(float(raw_input("Welcher Monat?(Zahl; Standard: %d) " % datetime.datetime.now().month))) or datetime.datetime.now().month
year = raw_input("Welches Jahr?(Zahl; Standard: %d) " % datetime.datetime.now().year) or datetime.datetime.now().year
body = "Hallo Herr "+config.name+",\n\nhier meine Abrechnung für "+monate[month]+" %d:\n\n"%(year)
userInput = raw_input("Tag: ")
moneyTotal = 0
lastKW = 0
while not(userInput == ""):
  day = int(float(userInput))
  dayInfo = datetime.date(year,month,day).isocalendar()
  startTime=datetime.time(0, 0) 
  endTime=datetime.time(0, 0)
  if(dayInfo[2]==1):
    startTime=datetime.time(17, 00) 
    endTime=datetime.time(18, 30)
  if(dayInfo[2]==3):
    startTime=datetime.time(16, 30) 
    endTime=datetime.time(17, 45)
  if(dayInfo[2]==5):
    startTime=datetime.time(17, 00) 
    endTime=datetime.time(18, 30)
  deltaMinute = (endTime.minute-startTime.minute)
  deltaHour = (endTime.hour-startTime.hour)
  money = (deltaHour+deltaMinute/60.0)*6
  moneyTotal = moneyTotal + money

  if(lastKW < dayInfo[1]):
    body = body + "KW %02d:\n" % dayInfo[1]
    lastKW = dayInfo[1]
  body =  body + tage[dayInfo[2]]+",\t%02d.%02d.%d\t%02d:%02d - %02d:%02d\t= %1.2f€\n"%(day,month,year,startTime.hour,startTime.minute,endTime.hour,endTime.minute, float(money))

  print(money)
  userInput = raw_input("Tag (oder leer zum beenden): ")

body = body + "------------------------------------------------\n"
body = body + " = %1.2f\n" % moneyTotal
body = body+"\nMit freundlichen Grüßen,\nAdrian Hinrichs"
print body
call(["thunderbird","-compose","""to='"""+config.email+"""',subject='Abrechnung ',body='""" + body + "'"""])
