from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
from Screens.screen import Screen

class AddRabbitScreen(Screen):
        
    def __init__(self):
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


    def update_rabbit(self, app1, id = 0):
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
            sqlstring = 'INSERT into rabbits (' + selectlist + ", status) values ('" + newlist + "', '1')"
        #print (sqlstring)
        try:
            banco.dml(sqlstring)
            app1.destroy()
        except:
            messagebox.showinfo(title = "ERROR", message = "Error saving data")


    def add_pedigree(self, id=0):
        update = False
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



        app1 = Toplevel()
        app1.title("Modify Rabbit")
        app1.geometry("240x380")
        quadUpdate = LabelFrame(app1, text = "Modify Rabbit")
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
        btn_Save = Button(quadUpdate, text = btn_text, command = lambda: self.update_rabbit(app1, id))
        btn_Save.place(x = placementx, y = placementy)
        btn_Exit = Button(quadUpdate, text = "Cancel", command = app1.destroy)
        btn_Exit.place(x = placementx + 60, y = placementy)

        app1.mainloop()