# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 20:48:15 2015

@author: PaulJ
"""

#from jsonReadWriteFile import *
import pandas as pd
from tkinter import *
from tkinter.ttk import Frame, Button, Style



class Example(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
        self.parent = parent
        self.initUI()
        self.centerWindow(500, 500)
        
    def initUI(self, width=300, height=300):
        self.parent.title("Simple")
        self.style = Style()
        self.style.theme_use("default")
        self.pack(fill=BOTH, expand=1)
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x_loc = (sw - width)/2
        y_loc = (sh - height)/2
        ww = self.winfo_screenwidth()
        wh = self.winfo_screenheight()
        buttonWidth = 100
        buttonHeight = 50
        x_but_loc = (ww - buttonWidth)/2
        y_but_loc = (wh - buttonHeight)/2
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x_loc, y_loc))
        quitButton = Button(self, text="Quit",
                            command=self.quit)
        quitButton.place(x=x_but_loc, y=y_but_loc)

    def centerWindow(self, width=300, height=300):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()
        x_loc = (sw - width)/2
        y_loc = (sh - height)/2
        self.parent.geometry("%dx%d+%d+%d" % (width, height, x_loc, y_loc))



def main():
    databaseCSVFile = "Huron_River_Data.csv"
#    print("Reading CSV database into Dataframe...")
    try:                                    
        #Load local car database
        #riverDataDict = load_json(databaseFile)
        #print("Converting Dictionary into Panda Dataframe...")
        #riverData = pd.DataFrame.from_dict(riverDataDict, orient='index')
        riverData = pd.read_csv(databaseCSVFile, sep=",", engine="c", index_col=0)
        riverData.index = pd.to_datetime(riverData.index)
    except (FileNotFoundError):  #OSError, ValueError
        print("No good csv file found, exiting...")
        return
    else:
        startNoRiverData = len(riverData)
        print("Found csv file and loaded into 'riverData' Dataframe with", startNoRiverData, "entries.")
    root = Tk()
    root.geometry("250x150+300+300")
    app = Example(root)
    root.mainloop()
        
    
if __name__ == '__main__':
    main()