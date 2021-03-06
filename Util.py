import os

ENDC = '\033[0m' 
RED = '\033[91m'
GREEN = '\033[92m'
BLUE = '\033[94m'
CYAN = '\033[96m'
WHITE = '\033[97m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'
GREY = '\033[90m'
BLACK = '\033[90m'
DEFAULT = '\033[99m'

LOCKED = "locked"
UNLOCKED = "unlocked"
IN_PROGRESS = "in progress"
COMPLETE = "complete"

MENU_MAIN = "main"
MENU_CHARACTER = "character"
MENU_REGION = "region"
MENU_STATUSLOG = "status"
MENU_MAP = "map"

SAVEPATH = "Save.obj"

def clearScreen():
   os.system('cls' if os.name == 'nt' else 'clear')

def printTitle(title):
   print CYAN + "*" * (len(title)+4)
   print "* %s *" % title
   print "*" * (len(title)+4) + ENDC
