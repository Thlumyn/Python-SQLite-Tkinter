from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
from Screens.screen import Screen

class AddRabbitScreen(Screen):
        
    def __init__(self, mainscreen):
        self.mainscreen = mainscreen
        self.columns_new_rabbits = {
            "name": "Name",
            "earno": "Ear #",
            "breed": "Breed",
            "variety": "Variety",
            "weight": "Weight",
            "reg": "Reg #",
            "gc": "GC #",
            "legs": "Legs",
            "dob": "DOB"
        }
        self.entrylist = list(self.columns_new_rabbits.keys())
        self.entry = {}
        self.status = 1
        self.rabbitkey = 'rabbit'


    def update_rabbit(self, id = 0):
        rabbitdata = {}
        for entrycolumn in self.entrylist:
            rabbitdata[entrycolumn] = self.entry[entrycolumn].get()
        if id > 0 and int(id) == id:
            newlist = ''
            for eachcol in self.entrylist:
                if newlist != '':
                    newlist = newlist + ', '
                newlist = newlist + eachcol + " = '" + rabbitdata[eachcol] + "'"
            sqlstring = 'UPDATE rabbits SET ' + newlist + ' WHERE r_id = ' + str(id)
        else:
            selectlist = ''
            newlist = ''
            for eachcol in self.entrylist:
                if selectlist != '':
                    selectlist = selectlist + ', '
                selectlist = selectlist + eachcol
                if newlist != '':
                    newlist = newlist + "', '"
                newlist = newlist + rabbitdata[eachcol]
            sqlstring = 'INSERT into rabbits (' + selectlist + ", status) values ('" + newlist + "', '" + str(self.status) + "')"
        #print (sqlstring)
        try:
            banco.dml(sqlstring)
            self.on_closing()
        except:
            messagebox.showinfo(title = "ERROR", message = "Error saving data")

    def on_closing(self):
        self.mainscreen.populate()
        self.mainscreen.addrabbitopen = 0
        if self.mainscreen.linkpedigreeopen ==1:
            self.mainscreen.linkpedigree.add_new_finalized(self.rabbitkey)
            #self.mainscreen.linkpedigree.refresh_pedigree_screen()
        self.app1.destroy()


    def add_pedigree(self, id=0, status = 1, rabbitkey = 'rabbit'):
        update = False
        self.mainscreen.addrabbitopen = 1
        self.status = status
        self.rabbitkey = rabbitkey
        if id != 0 and int(id) == id:
            update = True
            selectlist = ''
            for eachcol in list(self.columns_new_rabbits.keys()):
                if selectlist != '':
                    selectlist = selectlist + ', '
                selectlist = selectlist + eachcol
            vquery = "SELECT " + selectlist + " FROM rabbits WHERE r_id = '" + str(id) + "'"
            rows = banco.dql(vquery)
            rows = rows[0]
            rabbitdata = {}
            for eachcol in list(self.columns_new_rabbits.keys()):
                rabbitdata[eachcol] = rows[list(self.columns_new_rabbits.keys()).index(eachcol)]
            

            #for i in rows:
            #    tv.insert("", "end", values = i)



        self.app1 = Toplevel()
        self.app1.title("Modify Rabbit")
        self.app1.geometry("240x380")
        quadUpdate = LabelFrame(self.app1, text = "Modify Rabbit")
        quadUpdate.pack(fill = "both", expand = "yes", padx = 10, pady = 5)

        placementx = 5
        placementy = 5
        for entrycolumn in self.entrylist:
            self.entry[entrycolumn] = Entry(quadUpdate)
            self.entry[entrycolumn].place(x = placementx + 50,y = placementy)

            #Add prefilled values if updating rabbits
            if update:
                if rabbitdata[entrycolumn] == None:
                    rabbitdata[entrycolumn] = ''
                self.entry[entrycolumn].insert(END,rabbitdata[entrycolumn]) 

            lbentry = Label(quadUpdate, text = self.columns_new_rabbits[entrycolumn])
            lbentry.pack(side = "left")
            lbentry.place(x = placementx, y = placementy)
            placementy += 35

        if update:
            btn_text = "Update"
        else:
            btn_text = "Add New"
        btn_Save = Button(quadUpdate, text = btn_text, command = lambda: self.update_rabbit(id))
        btn_Save.place(x = placementx, y = placementy)
        btn_Exit = Button(quadUpdate, text = "Cancel", command = self.on_closing)
        btn_Exit.place(x = placementx + 60, y = placementy)

        self.app1.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.app1.mainloop()