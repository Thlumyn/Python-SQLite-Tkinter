from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
from Screens.screen import Screen

class LinkPedigreeScreen(Screen):

    class subRabbit:

        def __init__(self, id, x=0, y=0):
            self.id = id
            self.rabbitdata = {}
            self.rabbitdata['r_id'] = self.id
            self.name = 'Unknown'
            self.x = x 
            self.y = y
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

    def rabbits_dropdown(self):
        dropdown_list = ['Unknown', 'New Rabbit']
        vquery = "SELECT r_id, name FROM rabbits ORDER BY r_id ASC"
        rows = banco.dql(vquery)
        for eachrow in rows:
            dropdown_list.append(str(eachrow[0]) + ': ' + eachrow[1])
        return dropdown_list
    
    def display_dropdown(self, x, y):
        siredropdown = ttk.Combobox(self.app1, values = self.rabbits_dropdown())
        siredropdown.set("Select Rabbit")
        siredropdown.place(x = x, y = y)

    def open_link_pedigree_screen(self, id=0):
        if id == 0 or int(id) != id:
            messagebox.showinfo(title = "ERROR", message = "Unable to load rabbit")
            return

        self.app1 = Toplevel()
        self.app1.title("Pedigree Linkage")
        self.app1.geometry("380x400")
        quadUpdate = LabelFrame(self.app1, text = "Link Pedigree")
        quadUpdate.pack(fill = "both", expand = "yes", padx = 10, pady = 5)

        self.rabbits_dict = {}

        self.rabbits_dict['rabbit'] = self.subRabbit(id,5,180)

        self.rabbits_dict['sire'] = self.subRabbit(self.rabbits_dict['rabbit'].sire,50,85)
        self.rabbits_dict['dam'] = self.subRabbit(self.rabbits_dict['rabbit'].dam,50,260)

        self.rabbits_dict['ssire'] = self.subRabbit(self.rabbits_dict['sire'].sire,120,45)
        self.rabbits_dict['sdam'] = self.subRabbit(self.rabbits_dict['sire'].dam,120,125)
        self.rabbits_dict['dsire'] = self.subRabbit(self.rabbits_dict['dam'].sire,120,215)
        self.rabbits_dict['ddam'] = self.subRabbit(self.rabbits_dict['sire'].dam,120,305)

        self.rabbits_dict['sssire'] = self.subRabbit(self.rabbits_dict['ssire'].sire,210,15)
        self.rabbits_dict['ssdam'] = self.subRabbit(self.rabbits_dict['ssire'].dam,210,60)
        self.rabbits_dict['sdsire'] = self.subRabbit(self.rabbits_dict['sdam'].sire,210,105)
        self.rabbits_dict['sddam'] = self.subRabbit(self.rabbits_dict['ssire'].dam,210,150)
        self.rabbits_dict['dssire'] = self.subRabbit(self.rabbits_dict['dsire'].sire,210,195)
        self.rabbits_dict['dsdam'] = self.subRabbit(self.rabbits_dict['dsire'].dam,210,240)
        self.rabbits_dict['ddsire'] = self.subRabbit(self.rabbits_dict['ddam'].sire,210,285)
        self.rabbits_dict['dddam'] = self.subRabbit(self.rabbits_dict['dsire'].dam,210,330)

        for rabbitkey, rabbitvalue in self.rabbits_dict.items():
            self.rabbits_dict[rabbitkey].label =Label(quadUpdate, text = rabbitvalue.name)
            self.rabbits_dict[rabbitkey].label.place(x = rabbitvalue.x, y = rabbitvalue.y)
            self.rabbits_dict[rabbitkey].btn_modify = Button(quadUpdate, text = "Edit", command = lambda: self.display_dropdown(rabbitvalue.x, rabbitvalue.y+10))
            self.rabbits_dict[rabbitkey].btn_modify.place(x = rabbitvalue.x, y = rabbitvalue.y + 30)

        # rabbitlb =Label(quadUpdate, text = rabbit.name)
        # rabbitlb.place(x = 5, y = 180)

        # #1st gen
        # sirelb =Label(quadUpdate, text = sire.name)
        # sirelb.place(x = 50, y = 85)
        # btn_modify_sire = Button(quadUpdate, text = "Edit", command = lambda: self.display_dropdown(50, 110))
        # btn_modify_sire.place(x = 50, y = 115)
       
        # damlb =Label(quadUpdate, text = dam.name)
        # damlb.place(x = 50, y = 260)

        # #2nd gen
        # ssirelb =Label(quadUpdate, text = ssire.name)
        # ssirelb.place(x = 120, y = 45)
        # sdamlb =Label(quadUpdate, text = sdam.name)
        # sdamlb.place(x = 120, y = 125)

        # dsirelb =Label(quadUpdate, text = dsire.name)
        # dsirelb.place(x = 120, y = 215)
        # ddamlb =Label(quadUpdate, text = ddam.name)
        # ddamlb.place(x = 120, y = 305)

        # #3rd gen
        # sssirelb =Label(quadUpdate, text = sssire.name)
        # sssirelb.place(x = 210, y = 15)
        # ssdamlb =Label(quadUpdate, text = ssdam.name)
        # ssdamlb.place(x = 210, y = 60)

        # sdsirelb =Label(quadUpdate, text = sdsire.name)
        # sdsirelb.place(x = 210, y = 105)
        # sddamlb =Label(quadUpdate, text = sddam.name)
        # sddamlb.place(x = 210, y = 150)

        # dssirelb =Label(quadUpdate, text = dssire.name)
        # dssirelb.place(x = 210, y = 195)
        # dsdamlb =Label(quadUpdate, text = dsdam.name)
        # dsdamlb.place(x = 210, y = 240)

        # ddsirelb =Label(quadUpdate, text = ddsire.name)
        # ddsirelb.place(x = 210, y = 285)
        # dddamlb =Label(quadUpdate, text = dddam.name)
        # dddamlb.place(x = 210, y = 330)