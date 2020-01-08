from firebase import firebase
import tkinter as tk
from tkinter import ttk
from tkinter import *

database = 'https://crud-python-emi.firebaseio.com/'
table = '/Students'

firebase = firebase.FirebaseApplication(database, None)

#Create         POST
def post(name,mail,phone):
        student = {     'Name': name,
                        'Email': mail,
                        'Phone': phone
                }
        result = firebase.post(table, student)
        return result

#Read           GET
def getAll():
        result = firebase.get(table, '')
        return result
def getById(id):
        result = firebase.get(table, id)
        return result

#Update         PUT
def putName(id,name):
        result = firebase.put(table+id, 'Name', name)
        return result
def putMail(id,mail):
        result = firebase.put(table+id, 'Email', mail)
        return result
def putPhone(id,phone):
        result = firebase.put(table+id, 'Phone', phone)
        return result
#Delete         DELTE
def delete(id):
        result = firebase.delete(table, id)
        return result







########################"""" Interface with Tkinter """"""###################""
def openregistration():
    def postForm():
        name_info = name.get()  #recupération des données depuis le formulaire
        mail_info = mail.get()
        phone_info = phone.get()
        post(name_info, mail_info, phone_info)     #envoie de la requete
        refreshList()                              #Reactulisation de la liste
        name_entry.delete(0, END)
        mail_entry.delete(0, END)                   # on vide le formulaire pour
        phone_entry.delete(0, END)                  #  une éventuel réutilisation

    registerForm = Toplevel()
    registerForm.geometry("500x360")
    registerForm.title("Add Student")
    heading = Label(registerForm,text="Enter Student Information", bg="orange", fg="black", width="500", height="3")
    heading.pack()
    name_text = Label(registerForm,text="Full Name * ", )
    mail_text = Label(registerForm,text="Email * ", )
    phone_text = Label(registerForm,text="Phone * ", )
    name_text.place(x=100, y=80)
    mail_text.place(x=100, y=120)
    phone_text.place(x=100, y=160)
    name = StringVar()
    mail = StringVar()
    phone = StringVar()
    name_entry = Entry(registerForm,textvariable=name, width="30")
    mail_entry = Entry(registerForm,textvariable=mail, width="30")
    phone_entry = Entry(registerForm,textvariable=phone, width="30")
    name_entry.place(x=180, y=80)
    mail_entry.place(x=180, y=120)
    phone_entry.place(x=180, y=160)
    register = Button(registerForm, text="Register", width="16", height="2", command=postForm, bg="orange")
    register.place(x=210, y=190)
    exitBtn = Button(registerForm, text="Close", width="16", height="2", command=registerForm.destroy,bg="orange")
    exitBtn.place(x=210, y=235)

    registerForm.mainloop()

##################### Main Window ############################
mainWin = Tk()
mainWin.geometry("1000x400")
mainWin.title("Firebase CRUD Example With Python")
heading = Label(text="Students Registred into Database :", bg="orange", fg="black", width="500", height="2")
heading.pack()

## tableau ##
tree=ttk.Treeview()
tree["columns"]=("1","2","3")
tree.column("#0", width=250, minwidth=200, stretch=tk.NO)
tree.column("1", width=250, minwidth=200, stretch=tk.NO)
tree.column("2", width=250, minwidth=200)
tree.column("3", width=250, minwidth=150, stretch=tk.NO)
tree.heading("#0",text="id",anchor=tk.W)
tree.heading("1", text="Name",anchor=tk.W)
tree.heading("2", text="Email",anchor=tk.W)
tree.heading("3", text="Phone",anchor=tk.W)

######################### USED FUNCTION ##################
def insert(id_stud,name_stud,mail_stud,phone_stud,row_id):
    tree.insert('', 'end', row_id, text=id_stud, values=(name_stud, mail_stud, phone_stud))

def refreshList():  # Remplissage de la liste
    tree.delete(*tree.get_children())       # On vide la liste
    students = getAll()                     # On Récupère les étudiants sous form json
    if ( students == None):                 # On vérifie s'il y a des étudiants
        return                              #       dans la BD
    values = list(students.values())
    ids =list(students.keys())              # On trannsforme le JSON en 2 listes
    for i in range(0,len(values)):          #      afin de les parcourirs
        student = values[i]                 #   pour récuperer leurs contenu
        id = ids[i]
        name = student.get("Name")
        mail = student.get("Email")
        phone = student.get("Phone")
        insert(id, name, mail, phone, i)       # insertion de l'étudiant dans la liste

def searchList():
    tree.delete(*tree.get_children())
    search_value = str(search.get())
    students = getAll()
    if ( students == None):
        return
    values = list(students.values())
    ids =list(students.keys())
    for i in range(0,len(values)):
        student = values[i]
        id = ids[i]
        name = student.get("Name")
        mail = student.get("Email")
        phone = student.get("Phone")
        regex = str(name + mail + phone).lower()
        if(search_value in regex):
            insert(id, name, mail, phone, i)

################Recherche
searchFrame = Frame(mainWin)
search_label = Label(searchFrame,text="Search : ",width="10" )
search_label.grid(row=0,column=0)
search = StringVar()
search_entry = Entry(searchFrame,textvariable=search, width="30")
search_entry.grid(row=0,column=1)
searchBtn = Button(searchFrame, text="Search", width="10", height="1", command=searchList, bg="orange")
searchBtn.grid(row=0,column=2)
searchFrame.pack()
####################################################################
tree.pack()

addBtn = Button(mainWin, text="Add Student", width="16", height="2", command=openregistration, bg="orange")
addBtn.pack()
refreshBtn = Button(mainWin, text="Refresh List", width="16", height="1", command=refreshList, bg="orange")
refreshBtn.pack()
closeBtn = Button(mainWin, text="Close", width="16", height="1", command=mainWin.destroy, bg="orange")
closeBtn.pack()

refreshList()
mainWin.mainloop()