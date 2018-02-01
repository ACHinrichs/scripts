#!/usr/bin/env python
# -*- coding: utf-8 -*-
from subprocess import call
import datetime
import math
import config_private as config
import curses
from calendar import monthrange


monate = ["","Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober","November","Dezember"]
tage = ["","Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

      
print("Erstelle die Abrechnung")




stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(1)
curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_WHITE, -1)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
COLORPAIR_SELECTED=2
curses.init_pair(3, curses.COLOR_YELLOW, -1)
COLORPAIR_MARKED=3
curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)
COLORPAIR_MARKED_SELECTED=4
curses.init_pair(5, curses.COLOR_BLUE, -1)
COLORPAIR_CW=3
curses.init_pair(6, curses.COLOR_BLACK, curses.COLOR_BLUE)
COLORPAIR_CW_INV=4

class MonthSelector:
  def __init__(self):
    self.month=datetime.datetime.now().month
    self.year=datetime.datetime.now().year
    self.win_background = curses.newwin(40, 40, 1, 1)
    self.win_background.bkgd(curses.color_pair(1))
    self.win_background.box()
    self.win_background.addstr(1, 1, "Abrechnungsscript")
    self.drawUI()

  def drawUI(self, tly=3, tlx=1, normalCP=1):
    self.win_background.addstr(tly,tlx,"Monat im Duodezimalsystem Eingeben:")
    self.win_background.addstr(tly+1,tlx,"  - a=10, b=11, c=12")
    self.win_background.addstr(tly+2,tlx,"  - SPACE für auswahl")
    self.win_background.addstr(tly+3,tlx,"  - MINUS für das Vorjahr")
    self.win_background.addstr(tly+3,tlx,"  - PLUS für das nächste Jahr")
    self.win_background.addstr(tly+5,tlx+8,str(self.month)+" "+str(self.year))
    self.win_background.refresh()

  def select(self):    
    key_pressed = -1
    while key_pressed != ord(' '):
      key_pressed = stdscr.getch()
      if ord('-')==key_pressed:
        self.year = self.year - 1
      elif ord('+')==key_pressed:
        self.year = self.year + 1
      elif ord('a')<= key_pressed <= ord('c'):
        self.month=key_pressed-ord('a')+10
      elif ord('1')<= key_pressed <= ord('9'):
        self.month=key_pressed-ord('1')+1
      self.drawUI()
    return self.month

  
class DaySelector:
  
  def __init__(self,month=-1,year=-1):
    if month==-1:
      self.month = raw_input("Welcher Monat?(Zahl; Standard: %d) " %
                             datetime.datetime.now().month) or str(datetime.datetime.now().month)
      self.month= int(self.month)
    else:
      self.month=month

    if year==-1:
      self.year = raw_input("Welches Jahr?(Zahl; Standard: %d) " %
                          datetime.datetime.now().year) or datetime.datetime.now().year
    else:
      self.year=year
    self.win_background = curses.newwin(40, 40, 1, 1)
    self.win_background.bkgd(curses.color_pair(1))
    self.win_background.box()
    self.win_background.addstr(1, 1, str(monate[self.month])+" "+str(self.year))
    self.win_background.refresh()
    self.selectedDay=13
    
  def createDays(self, tly=3, tlx=1, normalCP=1):
    self.win_background.addstr(tly,tlx+5,"Mo  Di  Mi  Do  Fr  Sa  So")
    startCW=datetime.date(self.year,self.month,1).isocalendar()[1]
    self.daywins={}
    self.dayMarked={}
    for day in range(1,monthrange(self.year, self.month)[1]+1):
      ic=datetime.date(self.year,self.month,day).isocalendar()
      wd=ic[2]
      cw=ic[1]
      mw=int(math.floor((day+(7-wd))/7))
      self.daywins[day]=self.win_background.derwin(3,4,
                                                   4+(mw) * 3,
                                                   1+wd*4)
      self.daywins[day].bkgd(curses.color_pair(1))
      self.daywins[day].addstr(1,1,"%2d"%day)
      self.daywins[day].box()
      self.dayMarked[day]=False
      self.refreshDays()
    self.win_background.addstr(tly+3*5+5,1,"Bitte die abzurechnenden Tage waehlen")
    self.win_background.addstr(tly+3*5+6,1,"Pfeiltasten zur Navigation,")
    self.win_background.addstr(tly+3*5+7,1,"SPACE um die Markierung umzuschalten")
    self.win_background.addstr(tly+3*5+8,1,"q zum beenden")
    self.win_background.refresh()
    
  def refreshDays(self):
    for day in self.daywins:
      if day==self.selectedDay:
        if self.dayMarked[day]:
          self.daywins[day].bkgd(curses.color_pair(COLORPAIR_MARKED_SELECTED))
        else:
          self.daywins[day].bkgd(curses.color_pair(COLORPAIR_SELECTED))
      else:
        if self.dayMarked[day]:
          self.daywins[day].bkgd(curses.color_pair(COLORPAIR_MARKED))
        else:
          self.daywins[day].bkgd(curses.color_pair(1))
      self.daywins[day].refresh()


  def selectDays(self):
    self.createDays()      
    key_pressed = -1
    while key_pressed != ord('q'):
      key_pressed = stdscr.getch()
      
      if key_pressed == curses.KEY_UP:
        self.selectedDay=self.selectedDay-7
        if self.selectedDay<1:
          self.selectedDay=self.selectedDay+35
      if key_pressed == curses.KEY_DOWN:
        self.selectedDay=(self.selectedDay+7)
        if self.selectedDay>monthrange(self.year, self.month)[1]:
          self.selectedDay=self.selectedDay%7
          
      if key_pressed == curses.KEY_RIGHT:
        self.selectedDay=(self.selectedDay+1)
        if self.selectedDay>monthrange(self.year, self.month)[1]:
          self.selectedDay=self.selectedDay-monthrange(self.year, self.month)[1]
            
      if key_pressed == curses.KEY_LEFT:
        self.selectedDay=self.selectedDay-1
        if self.selectedDay<1:
          self.selectedDay=self.selectedDay+monthrange(self.year, self.month)[1]
              
      if key_pressed == ord(' '):
        self.dayMarked[self.selectedDay]=not self.dayMarked[self.selectedDay]
          
      if key_pressed == curses.KEY_RESIZE:
        stdscr.erase()
      self.refreshDays()

    # Ende
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()

    self.selectedDays=[]
    for day in self.dayMarked:
      if self.dayMarked[day]:
        self.selectedDays.append(day)
    return self.selectedDays
    
stdscr.bkgd(curses.color_pair(1))
stdscr.refresh()

ms=MonthSelector()
ds=DaySelector(ms.select(),ms.year)
selectedDays=ds.selectDays()

body = "Hallo "+config.name+",\n\nhier meine Abrechnung für "+monate[ds.month]+" %d:\n\n"%(ds.year)




moneyTotal = 0
lastKW = 0
for day in selectedDays:
  dayInfo = datetime.date(ds.year,ds.month,day).isocalendar()
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
  body =  body + tage[dayInfo[2]]+",\t%02d.%02d.%d\t%02d:%02d - %02d:%02d\t= %1.2f€\n"%(day,ds.month,ds.year,startTime.hour,startTime.minute,endTime.hour,endTime.minute, float(money))

body = body + "--------------------------------------------------------\n"
body = body + "\t\t\t\t\t\t=%1.2f€\n" % moneyTotal
body = body+"\nMit freundlichen Grüßen,\nAdrian Hinrichs"
print(body)
call(["thunderbird","-compose","""to='"""+config.email+"""',format=2,subject='Abrechnung Trainerassistenz """+monate[ds.month]+"""',body='""" + body + "'"""])
