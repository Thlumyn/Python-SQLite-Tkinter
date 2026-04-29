from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco


columns_new_rabbits = {
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
entrylist = list(columns_new_rabbits.keys())
entry = {}


def update_rabbit(app1, id = 0):
    rabbitdata = {}
    for entrycolumn in entrylist:
        rabbitdata[entrycolumn] = entry[entrycolumn].get()
    if id > 0 and int(id) == id:
        newlist = ''
        for eachcol in entrylist:
            if newlist != '':
                newlist = newlist + ', '
            newlist = newlist + eachcol + " = '" + rabbitdata[eachcol] + "'"
        sqlstring = 'UPDATE rabbits SET ' + newlist + ' WHERE r_id = ' + str(id)
    else:
        selectlist = ''
        newlist = ''
        for eachcol in entrylist:
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





        


# def Id():
#     Varcontrole = 1
#     if entryId.get() == "":
#         messagebox.showinfo(title = "ERROR", message = "Error loading")
#         Varcontrol = 0
#         return Varcontrol
#     try:
#         Varcontrol = entryId.get()
#         return Varcontrol
#     except:
#         messagebox.showinfo(title = "ERROR", message = "Error loading")
#         Varcontrol = 0
#         return Varcontrol
    
# def Name():
#     if entryName.get()=="":
#         messagebox.showinfo(title = "ERROR", message = "Failure loading Name")
#         return
#     try:
#         resId = Id()
#         if resId == 0:
#             return
#         vquery = "UPDATE rabbits SET name = " + "\'" + entryName.get() + "\' WHERE r_id=" + resId
#         banco.dml(vquery)
#     except:
#         messagebox.showinfo(title = "ERROR", message = "Error loading")
#         return
#     entryName.delete(0, END)
# def EarNo():
#     if entryEarNo.get()=="":
#         messagebox.showinfo(title = "ERROR", message = "Error loading ear number")
#         return
#     try:
#         resId = Id()
#         if resId == 0:
#             return
#         vquery = "UPDATE rabbits SET ear_no=" + "\'" + entryEarNo.get() + "\' WHERE r_id=" + resId
#         banco.dml(vquery)
#     except:
#         messagebox.showinfo(title = "ERROR", message = "Error updating ear number")
#         return
#     entryEarNo.delete(0, END)
# def Variety():
#     if entryVariety.get()=="":
#         messagebox.showinfo(title = "ERROR", message = "Error loading variety")
#         return
#     try:
#         resId = Id()
#         if resId == 0:
#             return
#         vquery = "UPDATE rabbits SET variety=" + "\'" + entryVariety.get() + "\' WHERE r_id=" + resId
#         banco.dml(vquery)
#     except:
#         messagebox.showinfo(title = "ERROR", message = "Error updating")
#         return
#     entryVariety.delete(0, END)
# def DOB():
#     if entryDOB.get()=="":
#         messagebox.showinfo(title = "ERROR", message = "Error loading dob")
#         return
#     try:
#         resId = Id()
#         if resId == 0:
#             return
#         vquery = "UPDATE rabbits SET dob =" + "\'" + entryDOB.get() + "\' WHERE r_id=" + resId
#         banco.dml(vquery)
#     except:
#         messagebox.showinfo(title = "ERROR", message = "Error updating")
#         return
#     entryDOB.delete(0, END)

def add_pedigree(id=0):
    update = False
    if id != 0 and int(id) == id:
        update = True
        selectlist = ''
        for eachcol in list(columns_new_rabbits.keys()):
            if selectlist != '':
                selectlist = selectlist + ', '
            selectlist = selectlist + eachcol
        vquery = "SELECT " + selectlist + " FROM rabbits WHERE r_id = '" + str(id) + "'"
        rows = banco.dql(vquery)
        rows = rows[0]
        rabbitdata = {}
        for eachcol in list(columns_new_rabbits.keys()):
            rabbitdata[eachcol] = rows[list(columns_new_rabbits.keys()).index(eachcol)]
        

        #for i in rows:
        #    tv.insert("", "end", values = i)



    app1 = Toplevel()
    app1.title("Modify Rabbit")
    app1.geometry("240x380")
    quadUpdate = LabelFrame(app1, text = "Modify Rabbit")
    quadUpdate.pack(fill = "both", expand = "yes", padx = 10, pady = 5)

    placementx = 5
    placementy = 5
    for entrycolumn in entrylist:
        entry[entrycolumn] = Entry(quadUpdate)
        entry[entrycolumn].place(x = placementx + 50,y = placementy)

        if update:
           if rabbitdata[entrycolumn] == None:
                rabbitdata[entrycolumn] = ''
           entry[entrycolumn].insert(END,rabbitdata[entrycolumn]) 

        lbentry = Label(quadUpdate, text = columns_new_rabbits[entrycolumn])
        lbentry.pack(side = "left")
        lbentry.place(x = placementx, y = placementy)
        placementy += 35

    if update:
        btn_text = "Update"
    else:
        btn_text = "Add New"
    btn_Save = Button(quadUpdate, text = btn_text, command = lambda: update_rabbit(app1, id))
    btn_Save.place(x = placementx, y = placementy)
    btn_Exit = Button(quadUpdate, text = "Cancel", command = app1.destroy)
    btn_Exit.place(x = placementx + 60, y = placementy)

    # entryName = Entry(quadUpdate)
    # entryEarNo = Entry(quadUpdate)
    # entryVariety = Entry(quadUpdate)
    # entryDOB = Entry(quadUpdate)
    # entryId = Entry(quadUpdate)
    #Label(quadUpdate, text = "Digite o Id abaixo:", background = "#dde", foreground = "#009", anchor = W).place(x = 5, y = 180)
    # entryName.place(x = 5,y = 5)
    # entryEarNo.place(x = 5,y = 50)
    # entryVariety.place(x = 5,y = 105)
    # entryDOB.place(x = 5,y = 155)
    # entryId.place(x = 5, y = 215)
    # btn_Name = Button(quadUpdate, text = "Name", command = Name)
    # btn_EarNo = Button(quadUpdate, text  = "EarNo", command = EarNo)
    # btn_Variety = Button(quadUpdate, text = "Variety", command = Variety)
    # btn_DOB = Button(quadUpdate, text = "DOB", command = DOB)
    # btn_Name.place(x = 135, y = 0)
    # btn_EarNo.place(x = 135, y = 50)
    # btn_Variety.place(x = 135, y = 100)
    # btn_DOB.place(x = 135, y = 150)
    
    
    
    app1.mainloop()