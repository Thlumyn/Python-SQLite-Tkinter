from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
def Id():
    Varcontrole = 1
    if entryId.get() == "":
        messagebox.showinfo(title = "ERROR", message = "Error loading")
        Varcontrol = 0
        return Varcontrol
    try:
        Varcontrol = entryId.get()
        return Varcontrol
    except:
        messagebox.showinfo(title = "ERROR", message = "Error loading")
        Varcontrol = 0
        return Varcontrol
    
def Name():
    if entryName.get()=="":
        messagebox.showinfo(title = "ERROR", message = "Failure loading Name")
        return
    try:
        resId = Id()
        if resId == 0:
            return
        vquery = "UPDATE rabbits SET name = " + "\'" + entryName.get() + "\' WHERE r_id=" + resId
        banco.dml(vquery)
    except:
        messagebox.showinfo(title = "ERROR", message = "Error loading")
        return
    entryName.delete(0, END)
def EarNo():
    if entryEarNo.get()=="":
        messagebox.showinfo(title = "ERROR", message = "Error loading ear number")
        return
    try:
        resId = Id()
        if resId == 0:
            return
        vquery = "UPDATE rabbits SET ear_no=" + "\'" + entryEarNo.get() + "\' WHERE r_id=" + resId
        banco.dml(vquery)
    except:
        messagebox.showinfo(title = "ERROR", message = "Error updating ear number")
        return
    entryEarNo.delete(0, END)
def Variety():
    if entryVariety.get()=="":
        messagebox.showinfo(title = "ERROR", message = "Error loading variety")
        return
    try:
        resId = Id()
        if resId == 0:
            return
        vquery = "UPDATE rabbits SET variety=" + "\'" + entryVariety.get() + "\' WHERE r_id=" + resId
        banco.dml(vquery)
    except:
        messagebox.showinfo(title = "ERROR", message = "Error updating")
        return
    entryVariety.delete(0, END)
def DOB():
    if entryDOB.get()=="":
        messagebox.showinfo(title = "ERROR", message = "Error loading dob")
        return
    try:
        resId = Id()
        if resId == 0:
            return
        vquery = "UPDATE rabbits SET dob =" + "\'" + entryDOB.get() + "\' WHERE r_id=" + resId
        banco.dml(vquery)
    except:
        messagebox.showinfo(title = "ERROR", message = "Error updating")
        return
    entryDOB.delete(0, END)
app1 = Tk()
app1.title("Update")
app1.geometry("240x270")
quadUpdate = LabelFrame(app1, text = "Update")
quadUpdate.pack(fill = "both", expand = "yes", padx = 10, pady = 5)
entryName = Entry(quadUpdate)
entryEarNo = Entry(quadUpdate)
entryVariety = Entry(quadUpdate)
entryDOB = Entry(quadUpdate)
entryId = Entry(quadUpdate)
Label(quadUpdate, text = "Digite o Id abaixo:", background = "#dde", foreground = "#009", anchor = W).place(x = 5, y = 180)
entryName.place(x = 5,y = 5)
entryEarNo.place(x = 5,y = 50)
entryVariety.place(x = 5,y = 105)
entryDOB.place(x = 5,y = 155)
entryId.place(x = 5, y = 215)
btn_Name = Button(quadUpdate, text = "Name", command = Name)
btn_EarNo = Button(quadUpdate, text  = "EarNo", command = EarNo)
btn_Variety = Button(quadUpdate, text = "Variety", command = Variety)
btn_DOB = Button(quadUpdate, text = "DOB", command = DOB)
btn_Name.place(x = 135, y = 0)
btn_EarNo.place(x = 135, y = 50)
btn_Variety.place(x = 135, y = 100)
btn_DOB.place(x = 135, y = 150)
app1.mainloop()