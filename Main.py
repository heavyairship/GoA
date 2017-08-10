import os
import sys
import atexit
import pickle
from Types import *
from Util import *

levelMap = None
def save():
   if levelMap is None:
      return
   levelMap.save()
atexit.register(save)

def displayMainMenu():
   clearScreen()
   printTitle("Welcome to Guild of Adventurers!")
   if os.path.exists("Save.obj"):
      validAns = ["c","n","q"]
      prompt = "Continue (c) New Game (n) Quit (q)? "
   else:
      validAns = ["n","q"]
      prompt = "New Game (n) Quit (q)? "
   while True:
      ans = raw_input(prompt)
      if ans in validAns:
         break
      else:
         print "Invalid answer"
   global levelMap
   if ans == "c":
      with open("Save.obj","rb") as saveFile:
         levelMap = pickle.load(saveFile)
   elif ans == "n":
      levelMap = LevelMap()
   else:
      sys.exit(0)
   displayMapMenu()
         
def displayLevelMenu(level):
   while True:
      clearScreen()
      printTitle("Level %d Menu" % level.levelId)
      for leg in level.legs.itervalues():
         leg.prettyPrint()
      try:
         ans = raw_input("Select Leg or Map Menu (m) Quit (q): ")
         if ans == "m":
            displayMapMenu()
            break
         if ans == "q":
            sys.exit(0) 
         ans = int(ans)
      except ValueError:
         raw_input("Unknown leg! (Any key to continue) ")
         continue
      if ans not in level.legs:
         raw_input("Unknown leg! (Any key to continue) ")
      elif level.legs[ans].status == LOCKED:
         raw_input("%s is locked! (Any key to continue) " % level.legs[ans].name)
      else: 
         level.legs[ans].begin()
      
def displayMapMenu():
   global levelMap
   while True:
      clearScreen()
      printTitle("Map Menu")
      for level in levelMap.levels.itervalues():
         level.prettyPrint()
      try:
         ans = raw_input("Select Level or Main Menu (m) Quit (q): ")
         if ans == "m":
            displayMainMenu()
            break
         if ans == "q":
            sys.exit(0) 
         ans = int(ans)
      except ValueError:
         raw_input("Unknown level! (Any key to continue) ")
         continue
      if ans not in levelMap.levels:
         raw_input("Unknown level! (Any key to continue) ")
      elif levelMap.levels[ans].status == LOCKED:
         raw_input("%s is locked! (Any key to continue) " % levelMap.levels[ans].name)
      else: 
         displayLevelMenu(levelMap.levels[ans])
         break

def main():
   try:
      displayMainMenu()
   except KeyboardInterrupt:
      print

if __name__ == "__main__":
   main()
