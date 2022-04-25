# pylint: disable=C0103,C0111,W0614,W0401,C0200,C0325
from tkinter import *
import tkinter.messagebox
import tkinter.filedialog
import tkinter.filedialog
import tkinter.font
import csv
import pandas as pd
import xml.etree.ElementTree as et



class Application(Frame):

    cellList = []
    currentCells = []
    currentCell = None

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.createDefaultWidgets()

    def focus_tab(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def focus_sh_tab(self, event):
        event.widget.tk_focusPrev().focus()
        return "break"

    def focus_right(self, event):
        #event.widget.tk_focusNext().focus()
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(j >= len(self.currentCells[0]) - 1 ):
                        j = -1    
                    self.currentCells[i][j+1].focus()
        return "break"

    def focus_left(self, event):
        
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(j == 0):
                        j = len(self.currentCells[0])    
                    self.currentCells[i][j-1].focus()
        return "break"

    def focus_up(self, event):
        
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if(i < 0):
                        i = len(self.currentCells)
                    self.currentCells[i-1][j].focus()
        return "break"

    def focus_down(self, event):
        
        widget = event.widget.focus_get()

        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                if widget == self.currentCells[i][j]:
                    if( i >= len(self.currentCells) - 1):
                        i = -1
                    self.currentCells[i+1][j].focus()
        return "break"

    def selectall(self, event):
        event.widget.tag_add("sel", "1.0", "end")
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return "break"

    def saveFile(self, event):
        self.saveCells()

    # TODO: Create bind for arrow keys and enter

    def createDefaultWidgets(self):
        w, h = 10, 1
        self.sizeX = 4
        self.sizeY = 6
        self.defaultCells = []
        for i in range(self.sizeY):
            self.defaultCells.append([])
            for j in range(self.sizeX):
                self.defaultCells[i].append([])

        for i in range(self.sizeY):
            for j in range(self.sizeX):
                tmp = Text(self, width=w, height=h)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.saveFile)
                #TODO: Add resize check on column when changing focus
                tmp.insert(END, "")
                tmp.grid(padx=0, pady=0, column=j, row=i)

                self.defaultCells[i][j] = tmp
                self.cellList.append(tmp)

        self.defaultCells[0][0].focus_force()
        self.currentCells = self.defaultCells
        self.currentCell = self.currentCells[0][0]


    def newCells(self):
        self.removeCells()
        self.createDefaultWidgets()

    def removeCells(self):
        while(len(self.cellList) > 0):
            for cell in self.cellList:
                
                cell.destroy()
                self.cellList.remove(cell)

    def loadCells(self):
        filename = tkinter.filedialog.askopenfilename(initialdir=".", title="Select file",
                                                filetypes=(("txt files", "*.txt"), ("all files", "*.*")))
        ary = []
        col = -1
        rows = []

        # get array size & get contents of rows
        with open(filename, "rt") as csvfile:
            rd = csv.reader(csvfile, delimiter=";")
            for row in rd:
                ary.append([])
                col = len(row)
                rows.append(row)

        # create the array
        for i in range(len(ary)):
            for j in range(col):
                ary[i].append([])

        # fill the array
        for i in range(len(ary)):
            for j in range(col):
                # print rows[i][j]
                ary[i][j] = rows[i][j]

        self.removeCells()


        loadCells = []
        for i in range(len(ary)):
            loadCells.append([])
            for j in range(len(ary[0])):
                loadCells[i].append([])

        # create the new cells
        for i in range(len(ary)):
            for j in range(len(ary[0])):
                tmp = Text(self, width=14, height=2)
                tmp.bind("<Tab>", self.focus_tab)
                tmp.bind("<Shift-Tab>", self.focus_sh_tab)
                tmp.bind("<Return>", self.focus_down)
                tmp.bind("<Shift-Return>", self.focus_up)
                tmp.bind("<Right>", self.focus_right)
                tmp.bind("<Left>", self.focus_left)
                tmp.bind("<Up>", self.focus_up)
                tmp.bind("<Down>", self.focus_down)
                tmp.bind("<Control-a>", self.selectall)
                tmp.bind("<Control-s>", self.saveFile)
                tmp.insert(END, ary[i][j])

                if(i == 0):
                    tmp.config(font=("", 10, "bold"))

                loadCells[i][j] = tmp
                tmp.focus_force()
                self.cellList.append(tmp)

                tmp.grid(padx=0, pady=0, column=j, row=i)

        self.currentCells = loadCells
        self.currentCell = self.currentCells[0][0]


    def saveCells(self):
        filename = tkinter.filedialog.asksaveasfilename(initialdir=".", title="Save File", filetypes=(
            ("txt files", "*.txt"), ("all files", "*.*")), defaultextension=".txt")

        vals = []
        # print(self.currentCells)
        for i in range(len(self.currentCells)):
            for j in range(len(self.currentCells[0])):
                vals.append(self.currentCells[i][j].get(1.0, END).strip())
                

        with open(filename, "w", -1, "utf-8") as csvfile:
            for rw in range(len(self.currentCells)):
                row = ""
                for i in range(len(self.currentCells[0])):
                    x = rw * len(self.currentCells[0])
                    if(i != len(self.currentCells[0]) - 1):
                        row += vals[x + i] + ";"
                    else:
                        row += vals[x + i]

                csvfile.write(row + "\n")

        tkinter.messagebox.showinfo("", "Saved!")



    def parse_XML(self): 
        """Parse the input XML file and store the result in a pandas 
        DataFrame with the given columns. 
        
        The first element of df_cols is supposed to be the identifier 
        variable, which is an attribute of each node element in the 
        XML data; other features will be parsed from the text content 
        of each sub-element. 
        """

        xml_file = ("Desktop\studia\!!!3SEM\integracja\zadanie2\katalog.xml")

        df_cols= ("Producent","Wielkosc matrycy","Rozdzielczosc","Typ matrycy","Dotyk","Procesor","Liczba rdzeni","Taktowanie","RAM","Pojemnosc dysku","Typ dysku","Karta graficzna","VRAM","System operacyjny","Naped optyczny")
        xtree = et.parse(xml_file)
        xroot = xtree.getroot()
        rows = []
        
        for node in xroot: 
            res = []
            res.append(node.attrib.get(df_cols[0]))
            for el in df_cols[1:]: 
                if node is not None and node.find(el) is not None:
                    res.append(node.find(el).text)
                else: 
                    res.append(None)
            rows.append({df_cols[i]: res[i] 
                        for i, _ in enumerate(df_cols)})
        
        out_df = pd.DataFrame(rows, columns=df_cols)
            
        return out_df

app = Application()
menubar = Menu(app)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=app.newCells)     

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_command(label="Exit", command=app.quit)
menubar.add_command(label="Open txt", command=app.loadCells)
menubar.add_command(label="Save txt", command=app.saveCells)
menubar.add_command(label="Open xml", command=app.parse_XML)
#menubar.add_command(label="Save xml", command=app.saveXml)

app.master.title('Zadanie 2 Edycja ')
app.master.config(menu=menubar)

default_font = tkinter.font.Font(font="TkTextFont")
default_font.configure(family="Helvetica")

app.option_add("*Font", default_font)
app.mainloop()
