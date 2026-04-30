from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
from Screens.screen import Screen

class LinkPedigreeScreen(Screen):

    class subRabbit:

        def __init__(self, id, sireof, damof, x=0, y=0):
            self.id = id
            self.rabbitdata = {}
            self.rabbitdata['r_id'] = self.id
            self.name = 'Unknown'
            self.x = x 
            self.y = y
            self.sireof = sireof
            self.damof = damof
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

        def assign_id(self, id):
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

            if self.sireof != 0 and self.sireof != None and self.id != None:
                updatestring = "UPDATE rabbits SET sire = '" + str(id) + "' WHERE r_id = '" + str(self.sireof) + "'"
                try:
                    banco.dml(updatestring)
                except:
                    messagebox.showinfo(title = "ERROR", message = "Error saving data")
    

            if self.damof != 0 and self.damof != None and self.id != None:
                updatestring = "UPDATE rabbits SET dam = '" + str(id) + "' WHERE r_id = '" + str(self.damof) + "'"
                try:
                    banco.dml(updatestring)
                except:
                    messagebox.showinfo(title = "ERROR", message = "Error saving data")
            
            
        
        
    def __init__(self, mainscreen):
        self.mainscreen = mainscreen
        self.id = 0

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
    
    def display_dropdown(self, rabbitkey):
        rabbitobject = self.rabbits_dict[rabbitkey]
        rabbitobject.rabbitdropdown = ttk.Combobox(self.app1, values = self.rabbits_dropdown())
        rabbitobject.rabbitdropdown.set("New Rabbit")
        rabbitobject.rabbitdropdown.place(x = rabbitobject.x, y = rabbitobject.y + 20)
        rabbitobject.btn_modify.config(text="Save", command = lambda rabbitkey=rabbitkey: self.save_dropdown(rabbitkey))

    def save_dropdown(self, rabbitkey):
        rabbitobject = self.rabbits_dict[rabbitkey]
        newrabbitid = rabbitobject.rabbitdropdown.get()
        if newrabbitid == 'Unknown':
            newrabbitid = 0
        elif newrabbitid == 'New Rabbit':
            self.mainscreen.addpedigree.add_pedigree(0, 0, rabbitkey)
            self.app1.wait_window(self.mainscreen.addpedigree.app1)
        else: 
            newrabbitid = newrabbitid.split(':')[0]
        rabbitobject.rabbitdropdown.place_forget()
        rabbitobject.label.config(text='')
        rabbitobject.label.place_forget()
        rabbitobject.btn_modify.place_forget()
        rabbitobject.assign_id(newrabbitid)
        #rabbitobject.btn_modify.config(text = "Edit", command = lambda rabbitkey=rabbitkey: self.display_dropdown(rabbitkey))
        self.refresh_pedigree_screen(self.rabbits_dict['rabbit'].id)

    def add_new_finalized(self, rabbitkey):
        vquery2 = "SELECT r_id FROM rabbits ORDER BY r_id DESC LIMIT 1"
        rows = banco.dql(vquery2)
        nextid = int(rows[0][0])
        newrabbitid = nextid
        rabbitobject = self.rabbits_dict[rabbitkey]
        rabbitobject.rabbitdropdown.place_forget()
        rabbitobject.label.config(text='')
        rabbitobject.label.place_forget()
        rabbitobject.btn_modify.place_forget()
        rabbitobject.assign_id(newrabbitid)
        #rabbitobject.btn_modify.config(text = "Edit", command = lambda rabbitkey=rabbitkey: self.display_dropdown(rabbitkey))
        self.refresh_pedigree_screen(self.rabbits_dict['rabbit'].id)
        

    def refresh_pedigree_screen(self, id=0):

        if id == 0:
            id = self.id
        else:
            self.id = id

        self.rabbits_dict = {}

        for label in self.labelslist:
            label.destroy()

        self.labelslist = []

        self.rabbits_dict['rabbit'] = self.subRabbit(id,0,0,5,180)

        self.rabbits_dict['sire'] = self.subRabbit(self.rabbits_dict['rabbit'].sire,self.rabbits_dict['rabbit'].id,0,50,85)
        self.rabbits_dict['dam'] = self.subRabbit(self.rabbits_dict['rabbit'].dam,0,self.rabbits_dict['rabbit'].id,50,260)

        self.rabbits_dict['ssire'] = self.subRabbit(self.rabbits_dict['sire'].sire,self.rabbits_dict['sire'].id,0,120,45)
        self.rabbits_dict['sdam'] = self.subRabbit(self.rabbits_dict['sire'].dam,0,self.rabbits_dict['sire'].id,120,125)
        self.rabbits_dict['dsire'] = self.subRabbit(self.rabbits_dict['dam'].sire,self.rabbits_dict['dam'].id,0,120,215)
        self.rabbits_dict['ddam'] = self.subRabbit(self.rabbits_dict['dam'].dam,0,self.rabbits_dict['dam'].id,120,305)

        self.rabbits_dict['sssire'] = self.subRabbit(self.rabbits_dict['ssire'].sire,self.rabbits_dict['ssire'].id,0,210,15)
        self.rabbits_dict['ssdam'] = self.subRabbit(self.rabbits_dict['ssire'].dam,0,self.rabbits_dict['ssire'].id,210,60)
        self.rabbits_dict['sdsire'] = self.subRabbit(self.rabbits_dict['sdam'].sire,self.rabbits_dict['sdam'].id,0,210,105)
        self.rabbits_dict['sddam'] = self.subRabbit(self.rabbits_dict['sdam'].dam,0,self.rabbits_dict['sdam'].id,210,150)
        self.rabbits_dict['dssire'] = self.subRabbit(self.rabbits_dict['dsire'].sire,self.rabbits_dict['dsire'].id,0,210,195)
        self.rabbits_dict['dsdam'] = self.subRabbit(self.rabbits_dict['dsire'].dam,0,self.rabbits_dict['dsire'].id,210,240)
        self.rabbits_dict['ddsire'] = self.subRabbit(self.rabbits_dict['ddam'].sire,self.rabbits_dict['ddam'].id,0,210,285)
        self.rabbits_dict['dddam'] = self.subRabbit(self.rabbits_dict['ddam'].dam,0,self.rabbits_dict['ddam'].id,210,330)

        for rabbitkey, rabbitvalue in self.rabbits_dict.items():
            self.rabbits_dict[rabbitkey].label =Label(self.quadUpdate, text = rabbitvalue.name)
            if int(self.rabbits_dict[rabbitkey].id) == 0:
                self.rabbits_dict[rabbitkey].label.config(fg='red')
            self.labelslist.append(self.rabbits_dict[rabbitkey].label)
            self.rabbits_dict[rabbitkey].label.place(x = rabbitvalue.x, y = rabbitvalue.y)
            self.rabbits_dict[rabbitkey].btn_modify = Button(self.quadUpdate, text = "Edit", command = lambda rabbitkey=rabbitkey: self.display_dropdown(rabbitkey))
            self.rabbits_dict[rabbitkey].btn_modify.place(x = rabbitvalue.x, y = rabbitvalue.y + 20)

    def on_closing(self):
        self.mainscreen.addpedigreeopen = 0
        self.app1.destroy()

    def open_link_pedigree_screen(self, id=0):
        if id == 0 or int(id) != id:
            messagebox.showinfo(title = "ERROR", message = "Unable to load rabbit")
            return
        
        self.mainscreen.linkpedigreeopen = 1

        self.app1 = Toplevel()
        self.app1.title("Pedigree Linkage")
        self.app1.geometry("380x420")
        self.quadUpdate = LabelFrame(self.app1, text = "Link Pedigree")
        self.quadUpdate.pack(fill = "both", expand = "yes", padx = 10, pady = 5)

        self.labelslist = []

        self.refresh_pedigree_screen(id)

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

        self.app1.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app1.mainloop()