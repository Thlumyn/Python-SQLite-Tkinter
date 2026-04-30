from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
from Screens.screen import Screen

class LinkPedigreeScreen(Screen):

    class subRabbit:

        def __init__(self, id):
            self.id = id
            self.rabbitdata = {}
            self.rabbitdata['r_id'] = self.id
            self.name = 'Unknown'
            if int(self.id) == 0:
                self.sire = 0
                self.dam = 0
            else:
                vquery = "SELECT sire, dam, name FROM rabbits WHERE r_id = '" + str(id) + "'"
                rows = banco.dql(vquery)
                rows = rows[0]
                keydata = ['sire', 'dam', 'name']
                for eachcol in keydata:
                    self.rabbitdata[eachcol] = rows[keydata.index(eachcol)]
                self.sire = self.rabbitdata['sire']
                self.dam = self.rabbitdata['dam']
                self.name = self.rabbitdata['name']
                if self.sire is None:
                    self.sire = 0
                if self.dam is None:
                    self.dam = 0

            
            
        
        
    def __init__(self, mainscreen):
        self.mainscreen = mainscreen

    def on_closing(self):
        self.mainscreen.populate()
        self.app1.destroy()

    def open_link_pedigree_screen(self, id=0):
        if id == 0 or int(id) != id:
            messagebox.showinfo(title = "ERROR", message = "Unable to load rabbit")
            return

        self.app1 = Toplevel()
        self.app1.title("Pedigree Linkage")
        self.app1.geometry("240x380")
        quadUpdate = LabelFrame(self.app1, text = "Link Pedigree")
        quadUpdate.pack(fill = "both", expand = "yes", padx = 10, pady = 5)

        rabbit = self.subRabbit(id)

        sire = self.subRabbit(rabbit.sire)
        dam = self.subRabbit(rabbit.dam)

        ssire = self.subRabbit(sire.sire)
        sdam = self.subRabbit(sire.dam)
        dsire = self.subRabbit(dam.sire)
        ddam = self.subRabbit(sire.dam)

        sssire = self.subRabbit(ssire.sire)
        ssdam = self.subRabbit(ssire.dam)
        sdsire = self.subRabbit(sdam.sire)
        sddam = self.subRabbit(ssire.dam)
        dssire = self.subRabbit(dsire.sire)
        dsdam = self.subRabbit(dsire.dam)
        ddsire = self.subRabbit(ddam.sire)
        dddam = self.subRabbit(dsire.dam)

        rabbitlb =Label(quadUpdate, text = rabbit.name)
        rabbitlb.place(x = 5, y = 190)

        sirelb =Label(quadUpdate, text = sire.name)
        sirelb.place(x = 50, y = 100)
        damlb =Label(quadUpdate, text = dam.name)
        damlb.place(x = 50, y = 280)