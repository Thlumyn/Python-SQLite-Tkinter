from tkinter import * 
# from tkinter import ttk 
# from tkinter import messagebox 
import os
# import banco
# import Screens.addpedigree as addpedigree
from Screens.mainscreen import MainScreen

#set variables
pastaApp = os.path.dirname(__file__) #used for handling files

main_screen = MainScreen()

main_screen.open_main_screen()


#def atualizar():
#    exec(open(pastaApp+"\\atualizar.py").read())

