#a python script containing class that manages console based user inputs

import os
import log_config.py
import menu_config.py

from log_config import LogConfig
log_config = LogConfig()
logger = log_config.get_logger()

#the user input will provide the user with a left justified box with menu items
#exmple:
#--------------------------------
#| 1. Bike db                   |
#| 2. charging db               |
#| 3. expense db                |
#| 4. service db                |
#| 5. exit                      |
#--------------------------------
#the user will then enter a number to select the menu item
#
#
#
#

#A class that dynamicaly generates text based menus whose hierarchy is defined by a dictionary {menu_item: sub_menu, menu: {sub_menu: sub_menu}}
#for example
#menu = {
#    "1. Bike db": {
#        "1.1. Add bike": None,
#        "1.2. View bikes": None,
#        "1.3. Update bike": None,
#        "1.4. Delete bike": None
#    },
#The class will then generate a menu that looks like this:
#--------------------------------
#| 1. Bike db                   |
#| 2. charging db               |
#| 3. expense db                |
#| 4. service db                |
#| 5. exit                      |
#--------------------------------

class user_terminal_input:
    #initialise the class with a menu
    def __init__(self, menu):
        