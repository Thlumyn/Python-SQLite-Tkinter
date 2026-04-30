from tkinter import * 
from tkinter import ttk 
from tkinter import messagebox
import banco
from Screens.screen import Screen
from Screens.addpedigree import AddRabbitScreen
from Screens.linkpedigree import LinkPedigreeScreen

class MainScreen(Screen):

    def __init__(self):
        self.datatype = "rabbits" #used to switch between breeder and rabbit views
        self.viewstatus = 1 #used to toggle between viewing different statuses
        #used to store grid values for rabbits vs breeders
        self.columns_breeders = {
            "b_id": "ID",
            "name": "Name",
            "rabbitry": "Rabbitry",
            "address": "Address"
        }
        self.columns_rabbits = {
            "r_id": "ID",
            "name": "Name",
            "earno": "Ear #",
            "variety": "Variety",
            "dob": "DOB"
        }
        self.addrabbitopen = 0
        self.linkpedigreeopen = 0

    #handle switching between rabbit view and breeder view on grid
    def switchtobreeders(self):
        self.datatype = "breeders"
        self.refresh_headers()
        self.populate()
        self.quadroGrid.configure(text=self.datatype.capitalize())
    def switchtorabbits(self):
        self.datatype = "rabbits"
        self.refresh_headers()
        self.populate()
        self.quadroGrid.configure(text=self.datatype.capitalize())

    #populat grid
    def populate(self):
        selectlist = ''
        self.tv.delete(*self.tv.get_children())
        if self.datatype == "rabbits":
            for eachcol in list(self.columns_rabbits.keys()):
                if selectlist != '':
                    selectlist = selectlist + ', '
                selectlist = selectlist + eachcol
            vquery = "SELECT " + selectlist + " FROM rabbits WHERE status = 1 order by r_id ASC"
        else: 
            for eachcol in list(self.columns_breeders.keys()):
                if selectlist != '':
                    selectlist = selectlist + ', '
                selectlist = selectlist + eachcol
            vquery = "SELECT " + selectlist + " FROM breeders WHERE status = 1 order by b_id ASC"
        rows = banco.dql(vquery)
        for i in rows:
            self.tv.insert("", "end", values = i)

    def search(self):
        self.tv.delete(*self.tv.get_children())
        vquery = "SELECT * FROM rabbits WHERE status = 1 AND name LIKE '%" + self.vnamesearch.get() + "%'"
        lines = banco.dql(vquery)
        for i in lines:
            self.tv.insert("", "end", values = i)
        self.vnamesearch.delete(0, END)


    def get_headers(self):
        #Set up columns
        if self.datatype == "rabbits":
            headers = self.columns_rabbits
        else:
            headers = self.columns_breeders
        return headers

    def refresh_headers(self):
        self.tv.delete(*self.tv.get_children())
        headers = self.get_headers()
        columns = list(headers.keys())

        self.tv["columns"] = columns
        
        for eachcol in columns:
            self.tv.column(eachcol, minwidth = 0, width = 100)
            self.tv.heading(eachcol, text = headers[eachcol])

    def get_selected_item(self):
        curItem = self.tv.focus()
        if len(curItem) > 0:
            return self.tv.item(curItem)["values"][0]
        else:
            return 0

    def open_main_screen(self):

        self.addpedigree = AddRabbitScreen(self)
        self.linkpedigree = LinkPedigreeScreen(self)
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
        m_data.add_command(label="View Rabbits", command=self.switchtorabbits)
        m_data.add_command(label="View Breeders", command=self.switchtobreeders)
        app['menu'] = m

        #Set up Grid
        self.quadroGrid = LabelFrame(app, text = self.datatype.capitalize())
        self.quadroGrid.pack(fill = "both", expand = "yes", padx = 10, pady = 10)

        headers = self.get_headers()
        columns = list(headers.keys())
        self.tv = ttk.Treeview(self.quadroGrid, columns = columns, show = 'headings')

        self.refresh_headers()

        self.tv.pack()
        self.populate()

        #Set up Insert Form
        quadInsert = LabelFrame(app, text = "Insert New Content")
        quadInsert.pack(fill = "both", expand = "yes", padx = 10, pady = 5)

        btn_addnew = Button(quadInsert, text = "Add Rabbit", command = self.addpedigree.add_pedigree)
        btn_addnew.place(x = 50, y = 0)
        btn_modify = Button(quadInsert, text = "Modify Rabbit", command = lambda: self.addpedigree.add_pedigree(self.get_selected_item()))
        btn_modify.place(x = 150, y = 0)
        btn_link = Button(quadInsert, text = "Edit Lineage", command = lambda: self.linkpedigree.open_link_pedigree_screen(self.get_selected_item()))
        btn_link.place(x = 250, y = 0)

        #Set up Search Form
        quadSearch = LabelFrame(app, text = "Search")
        quadSearch.pack(fill = "both", expand = "yes", padx= 10, pady = 10)
        lbid =Label(quadSearch, text = "Name")
        lbid.pack(side = "left")
        self.vnamesearch = Entry(quadSearch)
        self.vnamesearch.pack(side = "left", padx = 10)
        btn_search = Button(quadSearch, text = "Search", command = self.search)
        btn_search.pack(side = "left", padx = 10)
        btn_all = Button(quadSearch, text = "Show All", command = self.populate)
        btn_all.pack(side = "left", padx = 10)

        app.mainloop()