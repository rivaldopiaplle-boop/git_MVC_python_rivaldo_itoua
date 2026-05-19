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

from observer import Observer
from models import UsersList

class UsersView(Observer) :
    def __init__(self,parent,bg="white",width=600,height=300):
        if DEBUG :
            print(type(self).__name__+".__init__()")
        self.parent=parent
        self.bg=bg
        self.width,self.height=width,height
        self.gui() 
        self.actions_binding()

    def get_parent(self) :
        return self.parent
    def set_parent(self,parent) :
        self.parent=parent
        
    def gui(self) :
        if DEBUG :
            print(type(self).__name__+".gui()")
        self.frame=tk.LabelFrame(self.parent,text="users",bg="yellow")
        self.list_names=tk.Listbox(self.frame)
        self.list_names.configure(height=4)

    def update(self,model): 
        if DEBUG :
            print(type(self).__name__+".update()")
        self.list_names.delete(0, "end")
        for name in model.get_names():
            self.list_names.insert("end",name)

    def actions_binding(self) :
        if DEBUG :
            print(type(self).__name__+".actions_binding()")
        self.frame.bind("<Configure>",self.resize)
 
    def resize(self,event):
        if DEBUG :
            print(type(self).__name__+".resize()")
            print("width,height : ",(event.width,event.height))
        self.width,self.height=event.width,event.height

    def layout(self,side="top") :
        self.frame.pack(side=side,expand=1,fill="both",padx=20,pady=10)
        self.list_names.pack(expand=1,fill="both")         

if   __name__ == "__main__" :
   root=tk.Tk()
   root.title("users View")
   
   model=UsersList()
   print("model : ",model.get_names())

   view=UsersView(root)
   view.layout()
   model.attach(view) #attacher la vue au model
   model.create()
   print("model.create() : ",model.get_names())
   model.read()
   print("model.read() : ",model.get_names())

   root.mainloop()

