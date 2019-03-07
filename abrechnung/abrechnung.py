#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import argparse
import npyscreen


from subprocess import call
import math
import config_private as config
import curses
from calendar import monthrange


monate = ["","Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August", "September", "Oktober","November","Dezember"]
tage = ["",
        "Montag",
        "Dienstag",
        "Mittwoch",
        "Donnerstag",
        "Freitag",
        "Samstag",
        "Sonntag"]

now = datetime.datetime.now()

parser = argparse.ArgumentParser(description='Generiert die Abrechnung für erteilte Trainings')
parser.add_argument('-m', '--month',
                    type=int,
                    help="Der Monat für den Abrechnungszeitraum",
                    required=False,
                    default=now.month)
parser.add_argument('-y','--year',
                    type=int,
                    help="Das Jahr des Abrechnungszeitraumes",
                    required=False,
                    default=now.year)

BEGRUESSUNG = "Hallo Volker,\n"
SCHLUSSFORMEL = "Alles Gute,\nAdrian"
GEHALT = 12
class TrainingsSlot:
  def __init__(self,
               descr,
               duration,
               default=False):
    """
    Initialises the Training

    Arguments:
    wd      -- The weekday of the Trianing (Monday = 1, Sunday=7)
    descr   -- Description of the Training (e.g. Start/End-Time)
    time    -- The duration in hours
    default -- if it shall be selected by default (default is fase)
    """
    self.description = descr
    self.duration=duration
    self.default=default

class Training:
  def __init__(self,
               slot,
               day,
               month,
               year):
    self.slot=slot
    self.day=day
    self.month=month
    self.year=year

  def lohn(self):
    return self.slot.duration * GEHALT

  def __str__(self):
    ic=datetime.date(self.year,self.month,self.day).isocalendar()
    wd=ic[2]
    cw=ic[1]
    return f"KW {cw} {tage[wd]},\t{self.day}.{self.month}\t{self.slot.description}\t={(self.lohn()):.2f}€"

wochen_trainings = [{TrainingsSlot("17:00 - 18:30 Uhr", 1.5)}, # Montag
                    {}, # Dienstag
                    {TrainingsSlot("16:30 - 17:45 Uhr", 1.25,True), #Mittwoch
                     TrainingsSlot("17:45 - 19:15 Uhr", 1.5 ,True)},
                    {TrainingsSlot("17:00 - 18:15 Uhr", 1.25)}, # Donnerstag
                    {TrainingsSlot("17:00 - 18:30 Uhr", 1.5)}, # Freitag
                    {},{}] # WE



class AbrechnerApp(npyscreen.NPSApp):
  def __init__(self, month, year):
    self.month=month
    self.year=year
    pass
  
  def main(self):

    trainings = []
    trainings_sel = []
    training_num = 0
    for day in range(1,monthrange(self.year, self.month)[1]+1):
      ic=datetime.date(self.year,self.month,day).isocalendar()
      wd=ic[2]
      cw=ic[1]
      for slot in wochen_trainings[wd-1]:
        training_num = training_num+1
        trainings.append(Training(slot,day,self.month,self.year))
        if slot.default:
          trainings_sel.append(training_num-1)

    F  = npyscreen.Form(name = f"Abrechnung {monate[args.month]} {args.year}",)
    t  = F.add(npyscreen.TitleText, name = "Bitte wählen:",)   
    ms2= F.add(npyscreen.MultiSelect, value = trainings_sel,
               values = trainings, scroll_exit=True)
    F.edit()
    self.result=sorted([ms2.values[i] for i in ms2.value], key=lambda t: t.day)
      

if __name__ == "__main__":
  args=parser.parse_args()
  print(args.month)
  print(f"Erstelle Abrechnung für {monate[args.month]} {args.year}")
  App = AbrechnerApp(args.month, args.year)
  App.run()
  print(App.result)

  print("====== ABRECHNUNG ======")
  lohn_ges = 0
  body = BEGRUESSUNG
  body = body + "\nhier meine Abrechnung für "+monate[args.month]+" %d:\n\n"%(args.year)
  for training in App.result:
    body = body + str(training) + "\n"
    lohn_ges=lohn_ges + (training.lohn())
  body = body + "--------------------------------------------------------\n"
  body = body + f"\t\t\t\t\t\t={(lohn_ges):.2f}€\n"
  body = body + SCHLUSSFORMEL
  print(body)
  call(["thunderbird","-compose","""format=2,subject='Abrechnung Training """+monate[args.month]+"""',body='""" + body + "'"""])
