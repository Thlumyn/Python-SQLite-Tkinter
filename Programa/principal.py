from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox 
import os
import banco

#set variables
pastaApp = os.path.dirname(__file__) #used for handling files
datatype = "rabbits" #used to switch between breeder and rabbit views
viewstatus = 1 #used to toggle between viewing different statuses
#used to store grid values for rabbits vs breeders
columns_breeders = {
    "b_id": "ID",
    "name": "Name",
    "rabbitry": "Rabbitry",
    "address": "Address"
}
columns_rabbits = {
    "r_id": "ID",
    "name": "Name",
    "earno": "Ear #",
    "variety": "Variety",
    "dob": "DOB"
}

#handle switching between rabbit view and breeder view on grid
def switchtobreeders():
    global datatype
    datatype = "breeders"
    refresh_headers()
    populate()
    quadroGrid.configure(text=datatype.capitalize())
def switchtorabbits():
    global datatype
    datatype = "rabbits"
    refresh_headers()
    populate()
    quadroGrid.configure(text=datatype.capitalize())

#populat grid
def populate():
    global datatype
    global columns_breeders
    global columns_rabbits
    selectlist = ''
    tv.delete(*tv.get_children())
    if datatype == "rabbits":
        for eachcol in list(columns_rabbits.keys()):
            if selectlist != '':
                selectlist = selectlist + ', '
            selectlist = selectlist + eachcol
        vquery = "SELECT " + selectlist + " FROM rabbits WHERE status = 1 order by r_id ASC"
    else: 
        for eachcol in list(columns_breeders.keys()):
            if selectlist != '':
                selectlist = selectlist + ', '
            selectlist = selectlist + eachcol
        vquery = "SELECT " + selectlist + " FROM breeders WHERE status = 1 order by b_id ASC"
    rows = banco.dql(vquery)
    for i in rows:
        tv.insert("", "end", values = i)

def insert():
    if vname.get()=="" or vearno.get()=="" or vvariety.get()=="" or vdob.get() == "":
        messagebox.showinfo(title = "ERROR", message = "Missing Data")
        return
    try:
        vquery = "INSERT INTO rabbits(name, earno, variety, dob, status)VALUES('" + vname.get() + "','" + vearno.get() + "','" + vvariety.get() + "','" + vdob.get() + "',1)"
        banco.dml(vquery)
    except:
        messagebox.showinfo(title = "ERROR", message = "Error in inserting")
        return
    populate()
    vname.delete(0, END)
    vearno.delete(0, END)
    vvariety.delete(0, END)
    vdob.delete(0, END)
    vname.focus()
# def deletar():
#     try:
#         vid = 1
#         itemSelecionado = tv.selection()[0]
#         valores = tv.item(itemSelecionado, "values")
#         vid = valores[0]
#         vquery = "DELETE FROM tb_nomes WHERE id = " + vid
#         banco.dml(vquery)
#         tv.delete(itemSelecionado)
#     except:
#         messagebox.showinfo(title = "ERRO", message = "Escolha um item para ser deletado")
def delete():
    try:
        vid = 1
        itemSelected = tv.selection()[0]
        values = tv.item(itemSelected, "values")
        vid = values[0]
        #vquery = "DELETE FROM rabbits WHERE r_id = " + vid
        vquery = "UPDATE rabbits SET status = 0 WHERE r_id = " + vid
        banco.dml(vquery)
        tv.delete(itemSelected)
    except:
        messagebox.showinfo(title = "ERROR", message = "Error deleting item")
# def pesquisar():
#     tv.delete(*tv.get_children())
#     vquery = "SELECT * FROM tb_nomes WHERE nome LIKE '%" + vnamepesquisar.get() + "%'"
#     linhas = banco.dql(vquery)
#     for i in linhas:
#         tv.insert("", "end", values = i)
#     vnamepesquisar.delete(0, END)
def search():
    tv.delete(*tv.get_children())
    vquery = "SELECT * FROM rabbits WHERE name LIKE '%" + vnamesearch.get() + "%'"
    lines = banco.dql(vquery)
    for i in lines:
        tv.insert("", "end", values = i)
    vnamesearch.delete(0, END)
def atualizar():
    exec(open(pastaApp+"\\atualizar.py").read())

def get_headers():
    global datatype
    global columns_rabbits
    global columns_breeders

    #Set up columns
    if datatype == "rabbits":
        headers = columns_rabbits
    else:
        headers = columns_breeders
    return headers

def refresh_headers():
    tv.delete(*tv.get_children())
    headers = get_headers()
    columns = list(headers.keys())

    tv["columns"] = columns
    
    for eachcol in columns:
        tv.column(eachcol, minwidth = 0, width = 100)
        tv.heading(eachcol, text = headers[eachcol])


#Set up heading
app = Tk()
app.title("Open Rabbit Pedigree System")
app.geometry("600x500")

#Set up menu bar
app.option_add('*tearOff', FALSE)
#toplevel = Toplevel(app)
m = Menu(app)
m_options = Menu(m)
m_data = Menu(m)
m.add_cascade(menu=m_options, label = "Settings")
m_options.add_command(label="test1")
m_options.add_command(label="test2")
m.add_cascade(menu=m_data, label = "Data")
m_data.add_command(label="View Rabbits", command=switchtorabbits)
m_data.add_command(label="View Breeders", command=switchtobreeders)
app['menu'] = m

#Set up Grid
quadroGrid = LabelFrame(app, text = datatype.capitalize())
quadroGrid.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

headers = get_headers()
columns = list(headers.keys())
tv = ttk.Treeview(quadroGrid, columns = columns, show = 'headings')

refresh_headers()

# tv = ttk.Treeview(quadroGrid, columns = ('r_id', 'name',"earno", "variety",'dob'), show = 'headings')
# tv.column('r_id', minwidth = 0, width = 30)
# tv.column('name', minwidth = 0, width = 150)
# tv.column('earno', minwidth = 0, width = 100)
# tv.column('variety', minwidth = 0, width = 100)
# tv.column('dob', minwidth = 0, width = 100)
# tv.heading('r_id', text = 'ID')
# tv.heading('name', text = 'NAME')
# tv.heading('earno', text = 'EARNO')
# tv.heading('variety', text = 'VARIETY')
# tv.heading('dob', text = 'DOB')

tv.pack()
populate()

#Set up Insert Form
quadInsert = LabelFrame(app, text = "Insert New Content")
quadInsert.pack(fill = "both", expand = "yes", padx = 10, pady = 5)
lbname = Label(quadInsert, text = "Name")
lbname.pack(side = "left")
lbname.place(x = 0, y = 0)
vname = Entry(quadInsert)
vname.pack(side = "left", padx = 10)
vname.place(x = 41, y = 0)
lbearno = Label(quadInsert, text = "EarNo")
lbearno.pack(side = "left")
vearno = Entry(quadInsert)
vearno.pack(side = "left", padx = 10, pady = 10)
lbvariety = Label(quadInsert, text = "Variety")
lbvariety.pack(side = "left")
lbvariety.place(x = 175, y = 0)
vvariety = Entry(quadInsert)
vvariety.pack(side = "left", padx = 20, pady = 10)
vvariety.place(x = 236, y = 0)
lbdob = Label(quadInsert, text = "DOB")
lbdob.pack(side = "left")
vdob = Entry(quadInsert)
vdob.pack(side = "left", padx = 20, pady = 10)
btn_insert = Button(quadInsert, text = "Insert", command = insert)
btn_delete = Button(quadInsert, text  = "Delete", command = delete)
btn_delete.place(x = 388, y = -5)
btn_insert.pack(side = "left", padx = 10)

#Set up Search Form
quadSearch = LabelFrame(app, text = "Search")
quadSearch.pack(fill = "both", expand = "yes", padx= 10, pady = 10)
lbid =Label(quadSearch, text = "Name")
lbid.pack(side = "left")
vnamesearch = Entry(quadSearch)
vnamesearch.pack(side = "left", padx = 10)
btn_search = Button(quadSearch, text = "Search", command = search)
btn_search.pack(side = "left", padx = 10)
btn_all = Button(quadSearch, text = "Show All", command = populate)
btn_all.pack(side = "left", padx = 10)
app.mainloop()