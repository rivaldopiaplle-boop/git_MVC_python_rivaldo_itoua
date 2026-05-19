# coding: utf-8
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

from copy import copy
import sqlite3
from observer import Subject

DEBUG=False

class UsersList(Subject) :
    def __init__(self,names=[]) :
        if DEBUG :
            print(type(self).__name__+".__init__()")
        Subject.__init__(self)
        self.names=names
     
    def get_names(self) :
        return self.names
    def set_names(self,names) :
        if DEBUG :
            print(type(self).__name__+".set_names()")
        del self.names[:]
        self.names=copy(names)
        return

    def delete_names(self) :
        del self.names[:]
        self.notify()
        return

    def set_name(self,name):
        if DEBUG :
            print(type(self).__name__+".set_name()")
        if name not in self.names :
            self.names.append(name)
        self.notify()
        return 
    def remove(self,index):
        if DEBUG :
            print(type(self).__name__+".remove()")
        del self.names[index]
        self.notify()
        return

    # database connection, table creation from sqlite3 
    # $ sqlite3 users.db 
    # ....
    # sqlite> DROP TABLE IF EXISTS users;
    # sqlite> CREATE TABLE users (id INTEGER PRIMARY KEY,name VARCHAR(20));

    # database connection, table creation from python
    # def create_table(self,db_name="users.db",name="users",query="CREATE TABLE users(id INTEGER PRIMARY KEY,name VARCHAR(20));") :
    #     if DEBUG :
    #         print(type(self).__name__+".create_table()")
    #     connect=sqlite3.connect(db_name)
    #     cursor=connect.cursor()   
    #     drop="DROP TABLE IF EXISTS "+name+";"
    #     cursor.execute(drop)
    #     cursor.execute(query)
    #     connect.commit()
    #     cursor.close()
    #     connect.close()
       
    def create(self,db_name="users.db") :
        if DEBUG :
            print(type(self).__name__+".create()")
        connect=sqlite3.connect(db_name)
        cursor=connect.cursor()   
        query="INSERT OR IGNORE INTO users(id,name) VALUES(?,?)"
        key=1
        for name in self.get_names() :
            to_insert=key,name
            cursor.execute(query,to_insert)
            key+=1
        connect.commit()
        cursor.close()
        connect.close()


    def read(self,db_name="users.db") :
        if DEBUG :
            print(type(self).__name__+".read()")
        connect=sqlite3.connect(db_name)
        cursor=connect.cursor()
        query="SELECT name FROM users;"
        results=cursor.execute(query)
        if results :
            del self.names[:]
            for result in results :
                self.names.append(result[0])
        else :
            print("no users in database : "+db)
        connect.commit()
        cursor.close()
        connect.close()
        self.notify() #notifier les observateurs


    def update(self,db_name="users.db") :
        if DEBUG :
            print(type(self).__name__+".update()")
        connect=sqlite3.connect(db_name)
        cursor=connect.cursor()
        keys=cursor.execute("SELECT id FROM users")
        query="UPDATE users SET name= ? WHERE id=?;"
        for key in keys.fetchall() :
            index=key[0]-1
            cursor.execute(query, (self.names[index],key[0]) )
        connect.commit()
        cursor.close()
        connect.close()

    def delete(self,db_name="users.db") :
        if DEBUG :
            print(type(self).__name__+".delete()")
        connect=sqlite3.connect(db_name)
        cursor=connect.cursor()
        query="DELETE FROM users;"
        cursor.execute(query)   
        connect.commit()
        cursor.close()
        connect.close()
 
if   __name__ == "__main__" :
    model=UsersList()
    crud=input("choose CRUD (0,1,2,3) : ")
    crud=int(crud)
    if crud==0 :
        names=["Dupond","Durand"]
        model.set_names(names)
    #    print(model.get_names())
        model.delete()
        model.create()
     #   print(model.get_names())
    elif  crud==1 :
        model.read()
    elif  crud==2 :
        names=["Smith","Wesson"]
        model.set_names(names)
        model.update()
    elif   crud==3 :
        model.delete()
    for name in model.get_names() :
        print("user : "+name)

 
 

