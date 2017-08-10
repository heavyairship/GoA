import os
import sys
import atexit
import pickle
from Types import *
from Util import *

gameState = None
def save():
   if gameState is None:
      return
   gameState.save()
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
   global gameState
   if ans == "c":
      with open("Save.obj","rb") as saveFile:
         gameState = pickle.load(saveFile)
   elif ans == "n":
      playerName = raw_input("Welcome! What is your name? ")
      gameState = GameState(playerName)
   else:
      sys.exit(0)
   displayMapMenu()

def displayCharacterMenu():
   clearScreen()
   global gameState
   gameState.player.prettyPrint()
   ans = raw_input("(Any key to continue) ") 
         
def displayLevelMenu(level):
   while True:
      clearScreen()
      printTitle("Level %d Menu" % level.levelId)
      for leg in level.legs.itervalues():
         leg.prettyPrint()
      try:
         ans = raw_input("Select Leg (0-%d) Map Menu (m) Character (c) Quit (q): " 
            % (len(level.legs)-1))
         if ans == "m":
            displayMapMenu()
            break
         if ans == "c":
            displayCharacterMenu()
            continue
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
   levelMap = gameState.levelMap
   while True:
      clearScreen()
      printTitle("Map Menu")
      for level in levelMap.levels.itervalues():
         level.prettyPrint()
      try:
         ans = raw_input("Select Level (0-%d) Main Menu (m) Character (c) Quit (q): " 
            % (len(levelMap.levels)-1))
         if ans == "m":
            displayMainMenu()
            break
         if ans == "c":
            displayCharacterMenu()
            continue
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
