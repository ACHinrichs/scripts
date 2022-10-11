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

BEGRUESSUNG = f"Moin moin,\n"
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

  @property
  def woche(self):
    ic=datetime.date(self.year,self.month,self.day).isocalendar()
    cw=ic[1]
    return cw
    
  def lohn(self):
    return self.slot.duration * GEHALT

  def __str__(self):
    ic=datetime.date(self.year,self.month,self.day).isocalendar()
    wd=ic[2]
    cw=ic[1]
    return f"KW {cw} {tage[wd]},\t{self.day}.{self.month}\t{self.slot.description}\t={(self.lohn()):.2f}€"

wochen_trainings = [{TrainingsSlot("17:00 - 18:30 Uhr", 1.5, True), # Montag
                     TrainingsSlot("18:30 - 20:00 Uhr", 1.5), # Montag
                     #TrainingsSlot("20:00 - 21:00 Uhr (Online)", 1)
                     },
                    {}, # Dienstag
                    {TrainingsSlot("16:30 - 17:45 Uhr", 1.25, True), #Mittwoch
                     TrainingsSlot("17:45 - 19:15 Uhr", 1.5, True ),
                     #TrainingsSlot("18:00 - 19:00 Uhr (Online)",1)
                     },
                    {TrainingsSlot("17:00 - 18:15 Uhr", 1.25), # Donnerstag
                     TrainingsSlot("18:30 - 20:00 Uhr", 1.5)}, # Donnerstag
                    {TrainingsSlot("17:00 - 18:30 Uhr", 1.5),
                     TrainingsSlot("18:30 - 19:30 Uhr", 1, True), # 
                     #TrainingsSlot("19:00 - 20:00 Uhr", 1)
                     }, #Freitag
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
    print(self.result)

if __name__ == "__main__":
  args=parser.parse_args()
  print(args.month)
  print(f"Erstelle Abrechnung für {monate[args.month]} {args.year}")
  App = AbrechnerApp(args.month, args.year)
  App.run()
  print(App.result)

  print("====== ABRECHNUNG ======")
  lohn_ges = 0
  stunden_ges = 0
  body = BEGRUESSUNG
  body = body + "\nhier meine Abrechnung für "+monate[args.month]+" %d:\n\n"%(args.year)
  body += "Woche\tgel. Stunden à 12,00 €/h\t€\n"
  first_week = datetime.date(App.year,App.month,1).isocalendar()[1]
  last_week = datetime.date(App.year,App.month,monthrange(App.year, App.month)[1]).isocalendar()[1]
  print(monthrange(App.year, App.month)[1])
  weeks = {}
  for week in range(first_week, last_week+1):
    weeks[week] = 0
  
  for training in App.result:
    if training.woche in weeks:
      weeks[training.woche] += training.slot.duration
    else:
      weeks[training.woche] = training.slot.duration
    print(str(training))
  for (kw,stunden) in weeks.items():
    geld_kw = stunden * GEHALT
    body += f"{kw}\t{stunden}\t\t\t\t{geld_kw:.2f}€\n"
    lohn_ges += geld_kw
    stunden_ges += stunden
  body = body + "--------------------------------------------------------\n"
  body = body + f"Summe\t{stunden_ges}\t\t\t\t{(lohn_ges):.2f}€\n"
  body = body + SCHLUSSFORMEL
  print(body)
  #call(["thunderbird","-compose",f"""format=2,to={config.email},subject='Abrechnung Training """+monate[args.month]+"""',body='""" + body + "'"""])
