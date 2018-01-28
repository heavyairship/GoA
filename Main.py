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

def loadGameState():
   global gameState
   try:
      with open(SAVEPATH,"rb") as saveFile:
         gameState = pickle.load(saveFile)
   except: 
      raw_input("Corrupted save file was detected and deleted (Any key to continue) ")
           
def displayMainMenu():
   global gameState
   clearScreen()
   printTitle("Welcome to Guild of Adventurers!")
   if os.path.exists(SAVEPATH) and not gameState:
      loadGameState()
   if gameState: 
      validAns = ["c","n","q"]
      prompt = ("Continue %s's game (c) New Game (n) Quit (q)? " 
         % gameState.player.name)
   else:
      validAns = ["n","q"]
      prompt = "New Game (n) Quit (q)? "
   while True:
      ans = raw_input(prompt)
      if ans in validAns:
         break
      else:
         print "Invalid answer"
   if ans == "c":
      pass
   elif ans == "n":
      playerName = raw_input("Welcome! What is your name? ")
      gameState = GameState(playerName)
   else:
      sys.exit(0)
   for region in gameState.globe.regions.itervalues():
      for leg in region.legs.itervalues():
         leg.resume()

def displayCharacterMenu():
   clearScreen()
   gameState.player.prettyPrint()
   raw_input("(Any key to continue) ") 
         
def displayRegionMenu(region):
   clearScreen()
   printTitle("Region %d Menu" % region.regionId)
   for leg in region.legs.itervalues():
      leg.prettyPrint()
   try:
      ans = raw_input("Select Leg (0-%d) Map Menu (m) Character (c) "
         "Status Log (s) Refresh (r) Quit (q): " % (len(region.legs)-1))
      if ans == "m":
         gameState.menu = MENU_MAP
      if ans == "c":
         gameState.menu = MENU_CHARACTER
      if ans == "s":
         gameState.menu = MENU_STATUSLOG
      if ans == "r":
         pass
      if ans == "q":
         sys.exit(0) 
      ans = int(ans)
   except ValueError:
      raw_input("Unknown leg! (Any key to continue) ")
   if ans not in region.legs:
      raw_input("Unknown leg! (Any key to continue) ")
   elif region.legs[ans].status == LOCKED:
      raw_input("%s is locked! (Any key to continue) " % region.legs[ans].name)
   else: 
      region.legs[ans].begin()
      
def displayStatusLog():
   clearScreen()
   gameState.statusLog.prettyPrint()
   raw_input("(Any key to continue) ")
   
def displayMapMenu():
   globe = gameState.globe
   while True:
      clearScreen()
      printTitle("Map Menu")
      for region in globe.regions.itervalues():
         region.prettyPrint()
      try:
         ans = raw_input("Select Region (0-%d) Main Menu (m) Character (c) "
            "Status Log (s) Refresh (r) Quit (q): " % (len(globe.regions)-1))
         if ans == "m":
            displayMainMenu()
            break
         if ans == "c":
            displayCharacterMenu()
            continue
         if ans == "s":
            displayStatusLog()
            continue
         if ans == "r":
            continue
         if ans == "q":
            sys.exit(0) 
         ans = int(ans)
      except ValueError:
         raw_input("Unknown region! (Any key to continue) ")
         continue
      if ans not in globe.regions:
         raw_input("Unknown region! (Any key to continue) ")
      elif globe.regions[ans].status == LOCKED:
         raw_input("%s is locked! (Any key to continue) " % globe.regions[ans].name)
      else: 
         displayRegionMenu(globe.regions[ans])
         break

def display():
   menu = MENU_MAIN if not gameState else gameState.menu
   if menu == MENU_MAIN:
      displayMainMenu()
   elif menu == MENU_CHARACTER:
      displayCharacterMenu()
   elif menu == MENU_REGION:
      displayRegionMenu()
   elif menu == MENU_STATUSLOG:
      displayStatusMenu()
   elif menu == MENU_MAP:
      displayMapMenu()

def run():
   try:
      display()
   except KeyboardInterrupt:
      print

def main():
   run()

if __name__ == "__main__":
   main()
