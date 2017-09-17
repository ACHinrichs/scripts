#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call
import datetime
import math
import config_private as config
import curses
from calendar import monthrange


def TUICalendar:

  def printDays(win, year, month, active, tly=3, tlx=1, normalCP=1):
    win.bkgd(curses.color_pair(normalCP))
    
    startCW=datetime.date(year,month,1).isocalendar()[1]
    
    win.addstr(tly,tlx+3,"Mo Di Mi Do Fr Sa So")
    for day in range(1,monthrange(year, month)[1]):
      ic=datetime.date(year,month,day).isocalendar()
      cw=ic[1]
      wd=ic[2]
      win.addstr(tly+2+(cw-startCW) * 2,
                 tlx+wd*3,
                 "%2d"%day)
      
      win.move(tly,tly)
      win.refresh()

print("Erstelle die Abrechnung")

monate = ["","Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober","November","Dezember"]
tage = ["","Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

month = raw_input("Welcher Monat?(Zahl; Standard: %d) " % datetime.datetime.now().month) or str(datetime.datetime.now().month)
month= int(month)
year = raw_input("Welches Jahr?(Zahl; Standard: %d) " % datetime.datetime.now().year) or datetime.datetime.now().year


body = "Hallo Herr "+config.name+",\n\nhier meine Abrechnung für "+monate[month]+" %d:\n\n"%(year)


stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.start_color()
curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLUE)

stdscr.bkgd(curses.color_pair(1))
stdscr.refresh()

curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)

win = curses.newwin(15, 25, 1, 1,)
win.bkgd(curses.color_pair(1))
win.box()
win.addstr(1, 1, str(monate[month])+" "+str(year))

win.refresh()

printDays(win,year,month,-1)

day=1
dayInfo = datetime.date(year,month,day).isocalendar()

# Warten auf Tastendruck
c = stdscr.getch()

# Ende
curses.nocbreak()
stdscr.keypad(0)
curses.echo()
curses.endwin()

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
print(body)
call(["thunderbird","-compose","""to='"""+config.email+"""',subject='Abrechnung ',body='""" + body + "'"""])
