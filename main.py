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
    from tkinter import filedialog, messagebox
    tk.messagebox = messagebox
else :
    if __name__ == "__main__" :
        print("Your python version is : ",major,minor)
        print("... I guess it will work !")
    import tkinter as tk
    from tkinter import filedialog, messagebox
    tk.messagebox = messagebox

from pathlib import Path
import sqlite3

from models import UsersList
from views import UsersView
from controllers import UsersControl

def menubar() :
    if DEBUG :
        print("menubar()")
    menubar=tk.Menu(root) 
    root.config(menu=menubar)
    return menubar

def menubar_actions(menubar,actions) :
    if DEBUG :
        print("menubar_actions()")
    for key in actions.keys() :
        menu=tk.Menu(menubar)
        for action in actions[key] :
            item,ctrl=action 
            if key=="File" :
                menu.add_command(label=item,accelerator=ctrl,command=lambda name=item: on_file_actions(name))
                root.bind_all(ctrl,lambda x,name=item: on_file_actions(name))
            elif key=="Help" :
                menu.add_command(label=item,accelerator=ctrl,command=lambda name=item: on_help_actions(name))
                root.bind_all(ctrl,lambda x,name=item: on_help_actions(name))
            # if other key ("Help", ...)  : add  callbacks
        menubar.add_cascade(label=key,underline=0,menu=menu)

def on_file_actions(name): 
    if DEBUG :
        print("on_file_actions()")
    global model             
    if  name=="New" :
        new_action(model)
    elif name=="Load" :
        load_action(model)
    elif  name=="Save" :
        save_action(model)
    elif  name=="SaveAs" :
        saveAs_action(model)
    elif  name=="Exit" :
        exit_action(model)
    else :
        print(name+" : action non implémentée")
    return

def new_action(model) :
    if DEBUG:
        print("new_action()")
    
    result = tk.messagebox.askokcancel(
        title="Nouveau", 
        message="Voulez-vous créer un nouveau fichier ?",
        detail="Toutes les données actuelles seront effacées."
    )

    if result:
        model.delete()
        model.delete_names()
    
 #   pass

def load_action(model) :
    if DEBUG :
        print("load_action()")
    types=(('db files', '*.db'),)
    result=filedialog.askopenfilename(filetypes=types)
    print(result)
    if result :
        print(Path(result).name)
        name=Path(result).name
        model.read(db_name=name)
    return

def save_action(model) :
    if DEBUG :
        print("save_action()")
    result= tk.messagebox.askquestion(title="Sauvegarde", message=" fichier Users.db")
    print(result)

    if result=='yes' :
         
        model.delete()
        model.create()
    else :
      saveAs_action(model)
    return

def saveAs_action(model):
    if DEBUG:
        print("saveAs_action()")
    
    types = (("db files", "*.db"),)
    result = filedialog.asksaveasfilename(filetypes=types, defaultextension=".db")
    
    if result:
        name = Path(result).name
        
        # TO DO : connection to "name.db"
        # Cas extrême : Utilisation de sqlite3 pour gérer la structure du fichier
        import sqlite3
        conn = sqlite3.connect(result) # On utilise le chemin complet (result) pour créer le fichier
        cursor = conn.cursor()
        
        try:
            query = "DROP TABLE IF EXISTS users;"
            cursor.execute(query)
            
            query = "CREATE TABLE users (id INTEGER PRIMARY KEY, name VARCHAR(20));"
            cursor.execute(query)
            
            # TO DO : commit(), close()
            conn.commit()
            print(f"Table 'users' créée avec succès dans {name}")
            
        except Exception as e:
            print(f"Erreur lors de la création de la table : {e}")
        finally:
            conn.close()
            
        # Appel final au modèle comme dans votre code initial
        model.create(db_name=name)
    return

def exit_action(model) :
    if DEBUG:
        print("exit_action()")
    
    result = tk.messagebox.askokcancel(
        title="Exit", 
        message="Voulez-vous quitter le fichier ?",
        detail="Toutes les données seront perdus si non sauvegarder."
    )

    if result:
        exit(0)

def on_help_actions(name):
    if DEBUG :
        print("on_help_actions()")
    if  name=="About Us" :
        tk.messagebox.showinfo(
            title="About Us",
            message="Développeurs",
            detail=(
                "Francis Itoua\n"
                "f25itouam@enib.fr\n\n"
                "Rivaldo Piaplle\n"
                "f25piapll@enib.fr"
            )
        )
    elif name=="About Application" :
        tk.messagebox.showinfo(
            title="About Application",
            message="Users Manager — Gestionnaire d'utilisateurs",
            detail=(
                "Architecture : MVC (Model-View-Controller)\n"
                "Patron de conception : Observer/Subject\n"
                "Base de données : SQLite3 (users.db)\n"
                "Opérations : Créer, Lire, Mettre à jour, Supprimer (CRUD)\n"
                "Fonctionnalités : New, Load, Save, SaveAs, Exit\n"
                "Langage : Python 3 / Tkinter"
            )
        )
    elif  name=="About TkInter" :
        tk.messagebox.showinfo(
            title="About TkInter",
            message="Tkinter — Interface graphique Python",
            detail=(
                "Bibliothèque GUI standard de Python\n"
                "Widgets utilisés : Tk, Menu, LabelFrame, Listbox, Entry, Label\n"
                "Fenêtres : root (principale), Toplevel (vues secondaires)\n"
                "Événements : bind(), bind_all(), protocol()\n"
                "Boîtes de dialogue : messagebox, filedialog"
            )
        )
    else :
        print(name+" : non reconnu")
    return




# # TO DO  : MainWindow Class 
# if __name__=="__main__" :
#    ...
#     mw=MainWindow()
#     ...
#     mw.mainloop()

if __name__=="__main__" :
    root=tk.Tk()
    root.title("CAI : TkInter")
    root.resizable(width =True, height = False)
    root.option_readfile("main.opt")  
    menus=menubar()
    actions={
            "File" : [
              ("New","<Control-n>"),
              ("Load","<Control-l>"),
              ("Save","<Control-s>"),
              ("SaveAs","<Control-S>"),
              ("Exit","<Control-e>")
              ],
            "Help" : [
              ("About Us","<Control-u>"),
              ("About Application","<Control-a>"),
              ("About TkInter","<Control-t>")
              ]
    }
    menubar_actions(menus,actions)
    model=UsersList()
    view=UsersView(root)
    view.layout()
    model.attach(view)
    model.notify() 
    control=UsersControl(root,model,view)
    control.layout()

    top=tk.Toplevel(root)
    top.title("users View")
    view=UsersView(top)
    view.layout()
    model.attach(view)

    top=tk.Toplevel(root)
    top.title("users Control")
    control=UsersControl(top,model,view)
    control.layout()
    root.protocol("WM_DELETE_WINDOW", root.destroy)
    root.mainloop()

