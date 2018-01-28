import pickle
import datetime
import collections
import time
import sys
import threading
from Util import *

mapTemplate = collections.OrderedDict()
mapTemplate["Greece"] = ["Sparta","Athens","Medusa"]
mapTemplate["China"] = ["Bejing","Shanghai","The Red Dragon"]
threadMap = {}
globalLock = threading.Lock()

class Leg(object):
   def __init__(self,legId,name,region):
      self.legId = legId
      self.name = name
      self.region = region
      self.status = UNLOCKED if region.regionId == 0 and legId == 0 else LOCKED
      self.progress = 0
      self.length = 2
      self.thread = None

   def globe(self):
      return self.region.globe
   
   def player(self):
      return self.region.globe.gameState.player

   def gameState(self):
      return self.region.globe.gameState

   def prettyPrint(self):
      globalLock.acquire()
      if self.status == LOCKED:
         prefix = RED
      elif self.status == UNLOCKED:
         prefix = BLUE
      elif self.status == IN_PROGRESS:
         prefix = YELLOW
      else:
         prefix = GREEN
      print prefix + "%d - %s (%s)" % (self.legId, self.name, self.status) + ENDC
      globalLock.release()

   def changeStatus(self):
      globalLock.acquire()
      self.gameState().statusLog.add("%s complete!" % self.name)
      self.status = COMPLETE
      if self.legId+1 in self.region.legs:
         nextLeg = self.region.legs[self.legId+1]
         if nextLeg.status == LOCKED:
            self.gameState().statusLog.add("%s unlocked!" % nextLeg.name)
            nextLeg.status = UNLOCKED
      elif self.region.regionId+1 in self.globe().regions:
         self.gameState().statusLog.add("%s complete!" % self.region.name)
         self.region.status = COMPLETE 
         nextRegion = self.globe().regions[self.region.regionId+1]
         if nextRegion.status == LOCKED:
            self.gameState().statusLog.add("%s unlocked!" % nextRegion.name)
            nextRegion.status = UNLOCKED
         nextLeg = nextRegion.legs[0]
         if nextLeg.status == LOCKED:
            self.gameState().statusLog.add("%s unlocked!" % nextLeg.name)
            nextLeg.status = UNLOCKED
      else:
         self.gameState().statusLog.add("%s complete!" % self.region.name)
         self.region.status = COMPLETE 
         if self.gameState().status != COMPLETE:
            self.gameState().statusLog.add(GREEN + "Game complete! Congrats!" + ENDC)
            self.gameState().status = COMPLETE
      globalLock.release()

   def run(self):
      while self.progress < self.length:
         time.sleep(1)
         self.progress += 1
      self.progress = 0
      self.changeStatus()

   def resume(self):
      globalLock.acquire()
      global threadMap
      if self.status == IN_PROGRESS and self.name not in threadMap:
         threadMap[self.name] = threading.Thread(target=self.run)
         threadMap[self.name].daemon = True
         threadMap[self.name].start()
      globalLock.release()
         
   def begin(self):
      globalLock.acquire()
      global threadMap
      clearScreen()
      if self.name in threadMap and threadMap[self.name].isAlive():
         raw_input("Trek in progress (Any key to continue) ")
      else:
         self.status = IN_PROGRESS
         raw_input("Started trek! (Any key to continue) ")
         threadMap[self.name] = threading.Thread(target=self.run)
         threadMap[self.name].daemon = True
         threadMap[self.name].start()
      globalLock.release()

class Boss(Leg):
   def begin(self):
      globalLock.acquire()
      global threadMap
      clearScreen()
      if self.name in threadMap and threadMap[self.name].isAlive():
         raw_input(RED + "Boss fight in progress (Any key to continue) " + ENDC)
      else:
         self.status = IN_PROGRESS
         raw_input(RED + "Started boss fight! (Any key to continue) " + ENDC)
         threadMap[self.name] = threading.Thread(target=self.run)
         threadMap[self.name].daemon = True
         threadMap[self.name].start()
      globalLock.release()

class Region(object):
   def __init__(self,regionId,name,globe):
      self.regionId = regionId
      self.name = name
      self.globe = globe
      self.status = UNLOCKED if regionId == 0 else LOCKED
      self.legs = {}
      for i,legName in enumerate(mapTemplate[name]):
         if i == len(mapTemplate[name]) - 1:
            self.legs[i] = Boss(i,legName,self)
         else:
            self.legs[i] = Leg(i,legName,self)

   def prettyPrint(self):
      globalLock.acquire()
      if self.status == LOCKED:
         prefix = RED
      elif self.status == UNLOCKED:
         prefix = YELLOW
      else:
         prefix = GREEN
      print prefix + "%d - %s (%s)" % (self.regionId, self.name, self.status) + ENDC
      globalLock.release()

   def player(self):
      return self.globe.gameState.player
   
class Globe(object):
   def __init__(self,gameState):
      global mapTemplate
      self.gameState = gameState
      self.regions = {}
      for i,regionName in enumerate(mapTemplate.keys()):
         self.regions[i] = Region(i,regionName,self)

   def player(self):
      return self.gameState.player

class Player(object):
   def __init__(self,name,gameState):
      self.name = name
      self.gameState = gameState
      self.helm = None
      self.chest = None
      self.gloves = None
      self.legs = None
      self.boots = None
      self.walkingStick = None

   def prettyPrint(self):
      printTitle(self.name)
      print "Helm: "+str(self.helm)
      print "Chest: "+str(self.chest)
      print "Gloves: "+str(self.gloves)
      print "Legs: "+str(self.legs)
      print "Boots: "+str(self.boots)
      print "Walking Stick: "+str(self.walkingStick)

class StatusLog(object):
   def __init__(self,gameState):
      self.gameState = gameState
      self.data = []

   def add(self,status):
      self.data.append(status)

   def prettyPrint(self):
      printTitle("Status Log")
      if not len(self.data):
         print "<No log entries>"
      for d in self.data:
         print d

class GameState(object):
   def __init__(self,playerName):
      self.player = Player(playerName,self)
      self.globe = Globe(self)
      self.statusLog = StatusLog(self)
      self.save()
      self.status = IN_PROGRESS
      self.menu = MAIN
      self.prevMenu = None

   def save(self):
      with open(SAVEPATH,"wb") as saveFile:
         pickle.dump(self,saveFile)
