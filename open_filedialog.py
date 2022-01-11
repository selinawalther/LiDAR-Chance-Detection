import sys
from tkinter import *
from tkinter.filedialog import askopenfilenames

fname = "unassigned"

def openFile():
    global fname
    fname = askopenfilenames()
    root.destroy()

if __name__ == '__main__':

    root = Tk()
    Button(root, text='File Open', command = openFile).pack(fill=X)
    mainloop()

    print (fname)