import pickle
import collections
import time
import sys
from Util import *

mapTemplate = collections.OrderedDict()
mapTemplate["Greece"] = ["Sparta","Athens","Medusa"]
mapTemplate["China"] = ["Bejing","Shanghai","The Red Dragon"]

class Leg(object):
   def __init__(self,legId,name,level):
      self.legId = legId
      self.name = name
      self.level = level
      self.status = UNLOCKED if level.levelId == 0 and legId == 0 else LOCKED

   def levelMap(self):
      return self.level.levelMap
   
   def player(self):
      return self.level.levelMap.gameState.player

   def prettyPrint(self):
      if self.status == LOCKED:
         prefix = RED
      elif self.status == UNLOCKED:
         prefix = YELLOW
      else:
         prefix = GREEN
      print prefix + "%d - %s (%s)" % (self.legId, self.name, self.status) + ENDC

   def changeStatus(self):
      raw_input("%s complete! (Any key to continue) " % self.name)
      self.status = COMPLETE
      if self.legId+1 in self.level.legs:
         nextLeg = self.level.legs[self.legId+1]
         if nextLeg.status == LOCKED:
            raw_input("%s unlocked! (Any key to continue) " % nextLeg.name)
            nextLeg.status = UNLOCKED
      elif self.level.levelId+1 in self.levelMap().levels:
         raw_input("%s complete! (Any key to continue) " % self.level.name)
         self.level.status = COMPLETE 
         nextLevel = self.levelMap().levels[self.level.levelId+1]
         if nextLevel.status == LOCKED:
            raw_input("%s unlocked! (Any key to continue) " % nextLevel.name)
            nextLevel.status = UNLOCKED
         nextLeg = nextLevel.legs[0]
         if nextLeg.status == LOCKED:
            raw_input("%s unlocked! (Any key to continue) " % nextLeg.name)
            nextLeg.status = UNLOCKED
      else:
         print GREEN + "Game complete! Congrats!" + ENDC
         sys.exit(0)

   def begin(self):
      clearScreen()
      printTitle("%s, %s" % (self.name, self.level.name))
      print "Starting trek!"
      for i in range(2):
         time.sleep(1) 
         sys.stdout.write("...")
         sys.stdout.flush()
      sys.stdout.write("\n")
      sys.stdout.flush()
      self.changeStatus()

class Boss(Leg):
   def begin(self):
      clearScreen()
      printTitle("%s, %s" % (self.name, self.level.name))
      print RED + "Fighting boss!" + ENDC
      for i in range(2):
         time.sleep(1) 
         sys.stdout.write("...")
         sys.stdout.flush()
      sys.stdout.write("\n")
      sys.stdout.flush()
      self.changeStatus()

class Level(object):
   def __init__(self,levelId,name,levelMap):
      self.levelId = levelId
      self.name = name
      self.levelMap = levelMap
      self.status = UNLOCKED if levelId == 0 else LOCKED
      self.legs = {}
      for i,legName in enumerate(mapTemplate[name]):
         if i == len(mapTemplate[name]) - 1:
            self.legs[i] = Boss(i,legName,self)
         else:
            self.legs[i] = Leg(i,legName,self)

   def prettyPrint(self):
      if self.status == LOCKED:
         prefix = RED
      elif self.status == UNLOCKED:
         prefix = YELLOW
      else:
         prefix = GREEN
      print prefix + "%d - %s (%s)" % (self.levelId, self.name, self.status) + ENDC

   def player(self):
      return self.levelMap.gameState.player
   
class LevelMap(object):
   def __init__(self,gameState):
      global mapTemplate
      self.gameState = gameState
      self.levels = {}
      for i,levelName in enumerate(mapTemplate.keys()):
         self.levels[i] = Level(i,levelName,self)

   def player(self):
      return self.gameState.player

class Player(object):
   def __init__(self,name,gameState):
      self.name = name
      self.gameState = gameState

class GameState(object):
   def __init__(self,playerName):
      self.player = Player(self,playerName)
      self.levelMap = LevelMap(self)

   def save(self):
      with open("Save.obj","wb") as saveFile:
         pickle.dump(self,saveFile)
