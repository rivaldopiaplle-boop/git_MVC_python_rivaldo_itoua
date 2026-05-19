# coding: utf-8
DEBUG=False
import sys
major=sys.version_info.major
minor=sys.version_info.minor
if major==2 and minor==7 :
    import Tkinter as tk
    import tkFileDialog as filedialog
elif major==3 :
    import tkinter as tk
    from tkinter import filedialog
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog 

from models import UsersList
from views import UsersView

class UsersControl :
    def __init__(self,parent,model,view):
        if DEBUG :
            print(type(self).__name__+".__init__()")
        self.parent=parent
        self.model=model
        self.view=view
        self.gui()
        self.actions_binding()

    def gui(self):
        if DEBUG :
            print(type(self).__name__+".gui()")
        self.frame=tk.LabelFrame(self.parent,text="Insert",fg="red") 
        self.label=tk.Label(self.frame,text="Name") # ,bitmap = 'questhead'
        self.entry_var=tk.StringVar()
        self.entry=tk.Entry(self.frame,textvariable=self.entry_var)
        
    def actions_binding(self) :
        if DEBUG :
            print(type(self).__name__+".actions_binding()")
        self.entry.bind("<Return>",self.enter_action)
        self.view.list_names.bind("<Delete>",self.delete_action)

    def enter_action(self, event):
        if DEBUG :
            print(type(self).__name__+".enter_action()")
        name = event.widget.get()
        if name not in self.model.get_names() :
            self.model.set_name(name)
        self.entry.delete(0, "end")

    def delete_action(self, event): 
        if DEBUG :
            print(type(self).__name__+".delete_action()")
        for index in self.view.list_names.curselection():
            self.model.remove(int(index))

    def layout(self,side="top") :
        self.frame.pack(side=side)
        self.label.grid()
        self.entry.grid(row=0,column=1)

if   __name__ == "__main__" :
   root=tk.Tk()
   root.title("users Control")

   model=UsersList()

   view=UsersView(root)
   view.layout()
   model.attach(view) #attacher la vue au model
   model.read()
   control=UsersControl(root,model,view)
   control.layout()
   root.mainloop()

