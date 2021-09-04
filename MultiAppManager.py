# THIS IS AN APP TO AUTOMATE THE OPENING THE REQURIEMENT APPS INSTAD OF OPEN THEM MANUALLY 
# THIS APP IS WRETEN WITH TKINTER PYTHON MODULE ins
# THE DATA BASE OF THE APP IS A JSON FORMAT 
# THE APP IS BASED ON WEDGETS 
# C:\Users\hp\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from backend import *

# CONSTANTS
db = DataBase()
db.upload()
TASKS = db.get_data()
print(TASKS)
CHECKED = []
GUIS = []
APPS = {}
CHECKEDAPPS ={}
PAGE = 'main'
# main app
root = Tk()
root.geometry("540x540")
root.resizable(False,False)
root.iconbitmap('icon.ico')
root.title('oudr - Multy App Opener')
top = ttk.Frame(root,relief=GROOVE,border=5)
top.pack(fill=BOTH,padx=20,ipadx=10,pady=(20,0))
def render():
  pass
page1 = Frame(root,relief=GROOVE,border=1)
page2 = Frame(root,relief=GROOVE,border=1)
page1.pack(fill=BOTH,expand=1,padx=20,ipadx=10,pady=20)
sidebar = ttk.Scrollbar(page1,orient='vertical')
sidebar.pack(side=RIGHT,fill=Y)
render()
bottom = ttk.Frame(root,relief=GROOVE,border=5)
bottom.pack(fill=BOTH,padx=20,ipadx=10,pady=(0,20))
class TaskGUI:
  def __init__(self,task):
    self.task = task
  def draw(self):
    self.container = Frame(page1,bg='#fff',padx=5,pady=5)#,yscrollcommand=sidebar.set)
    self.container.pack(fill=X,padx=(20,40),pady=10)
    self.var = IntVar()
    self.check = Checkbutton(self.container,text=self.task.name,variable=self.var,bg='#fff',activebackground='#fff',font=('Arial',10))
    self.check.grid(row=0,column=0)
  def get_state(self):
    return (self.task.id,self.var.get())
  def open_apps(self):
    self.task.open_apps()
  def destroy(self):
    self.container.destroy()
  def get_id(self):
    return self.task.id
  def __repr__(self):
    return f'TaskGUI<{self.task.id}>'
class AppGUI:
  def __init__(self,app):
    self.app = app
  def draw(self):
    self.container = Frame(page1,bg='#fff',padx=5,pady=5)#,yscrollcommand=sidebar.set)
    self.container.pack(fill=X,padx=(20,60),pady=10)
    self.var = IntVar()
    self.check = Checkbutton(self.container,text=self.app.name,variable=self.var,bg='#fff',activebackground='#fff',font=('Arial',10))
    self.check.pack(side=LEFT)
    self.browse_btn = ttk.Button(self.container,text='browse',command=self.browse)
    self.browse_btn.pack(side=RIGHT)
  def get_state(self):
    return (self.app.id,self.var.get())
  def browse(self):
    types = (
      ('apps','*.exe'),
      ('all files','*.*'))
    filepath = fd.askopenfilename(
      title='choose task apps',
      initialdir='C:\\Program Files',
      filetypes=types)
    print(filepath)
    self.app.set_path(filepath)
    destroyApps()
    displayApps(self.app.parent)
  def destroy(self):
    self.container.destroy()
  def __repr__(self):
    return f'AppGUI<{self.app.get_index()}>'
# MAIN FUNCTONS
def switchPage():
  global PAGE
  PAGE= 'main' if PAGE == 'edit' else 'edit'
  print(PAGE)
def OpenFiles():
  update()
  for arr in CHECKED:
    if arr[1] == 1:
      TASKS[arr[0]].open_apps()
def CloseFiles():
  update()
  for arr in CHECKED:
    if arr[1] == 1:
      TASKS[arr[0]].close_apps()
def OpenApp(task):
  updateApps(task)
  for arr in CHECKEDAPPS[task.id]:
    if arr[1]==1:
      app = task.get_app(arr[0])
      app.open()
def CloseApp(task):
  updateApps(task)
  for arr in CHECKEDAPPS[task.id]:
    if arr[1]==1:
      app = task.get_app(arr[0])
      app.close()
def removeTask():
  global CHECKED,GUIS,TASKS
  update()
  destroy()
  for arr in CHECKED:
    if arr[1]==1:
      CHECKED.pop(arr[0])
      TASKS.pop(arr[0])
      GUIS.pop(arr[0])
  display()
def removeApp(task):
  destroyApps()
  updateApps(task)
  for arr in CHECKEDAPPS[task.id]:
    if arr[1]==1:
      CHECKEDAPPS[task.id].pop(arr[0])
      task.remove_app(arr[0])
      APPS[task.id].pop(arr[0])
  print(CHECKEDAPPS)
  print(task.apps)
  print(APPS)
  displayApps(task)
def addTask(name):
  TASKS.append(Task(len(TASKS),'task' if name=='' else name))
  destroy()
  display()
  entry.delete(0,END)
def addApp(name):
  idx=None
  for arr in CHECKED:
    if arr[1]==1:
      idx = arr[0]
      task = TASKS[idx]
      task.add_app(App(name))
      destroyApps()
      displayApps(task)
      break
  entry.delete(0,END)
def editTask():
  global bottom
  switchPage()
  update()
  print(CHECKED)
  print(GUIS)
  print(TASKS)
  print('\n')
  array = ()
  task =None
  for arr in CHECKED:
    if arr[1] == 1:
      array = arr
      break
  if len(array) > 0:
    task = TASKS[array[0]]
  destroy()
  displayApps(task)
  add_btn.config(text='add app',command=lambda:addApp(entry.get()))
  remove_btn.config(command=lambda:removeApp(task))
  open_btn.config(command=lambda:OpenApp(task))
  close_btn.config(command=lambda:CloseApp(task))
  edit_btn.config(state=DISABLED)
  return_btn.config(state=NORMAL)
  entry.delete(0,END)
def returnPage():
  global bottom
  switchPage()
  destroy()
  destroyApps()
  add_btn.config(text='add task',command=lambda:addTask(entry.get()))
  remove_btn.config(command=removeTask)
  open_btn.config(command=OpenFiles)
  close_btn.config(command=CloseFiles)
  entry.delete(0,END)
  return_btn.config(state=DISABLED)
  if PAGE=='main':
    display()
    edit_btn.config(state=NORMAL)
# MAIN GUI WEDGET
entry = Entry(top)
add_btn = ttk.Button(top,text='add task',command=lambda:addTask(entry.get()))
return_btn = ttk.Button(top,text='return',command=returnPage,state=DISABLED)
edit_btn = ttk.Button(bottom,text='edit',command=editTask)
close_btn = ttk.Button(bottom,text='close',command=CloseFiles)
open_btn = ttk.Button(bottom,text='open',command=OpenFiles)
remove_btn = ttk.Button(bottom,text='remove',command=removeTask)
edit_btn.grid(row=0,column=0,padx=20,pady=10)
remove_btn.grid(row=0,column=1,padx=20,pady=10)
close_btn.grid(row=0,column=2,padx=20,pady=10)
open_btn.grid(row=0,column=3,padx=20,pady=10)
add_btn.grid(row=0,column=2,padx=20,pady=10)
return_btn.grid(row=0,column=0,padx=20,pady=10)
entry.grid(row=0,column=1,padx=20,pady=10)

#-----------  MAIN LOOP ----------------#
def display():
  render()
  global CHECKED,GUIS
  array1 = []
  array2 = []
  for task in TASKS:
    taskgui = TaskGUI(task)
    array1.append(taskgui)
    taskgui.draw()
    array2.append(taskgui.get_state())
  GUIS = array1
  CHECKED = array2
display()
def displayApps(task):
  if task == None: return
  global APPS
  array =[]
  array2 = []
  for app in task.apps:
    appgui = AppGUI(app)
    array.append(appgui)
    appgui.draw()
    array2.append(appgui.get_state())
  APPS[task.id] = array
  CHECKEDAPPS[task.id] = array2
def destroyApps():
  global APPS
  for key in APPS:
    for appgui in APPS[key]:
      appgui.destroy()
  # APPS = []
def destroy():
  for taskgui in GUIS:
    taskgui.destroy()
def update():
  global CHECKED,GUIS
  for taskgui in GUIS:
    lst = taskgui.get_state()
    array = []
    for arr in CHECKED:
      if lst[0]==arr[0]:
        array.append(lst)
      else:
        array.append(arr)
    CHECKED = array
def updateApps(task):
  global APPS,CHECKEDAPPS
  for appgui in APPS[task.id]:
    lst = appgui.get_state()
    array=[]
    for arr in CHECKEDAPPS[task.id]:
      if lst[0] == arr[0]:array.append(lst)
      else: array.append(arr)
    CHECKEDAPPS[task.id] = array

root.mainloop()
print('finish')
db.set_data(TASKS)
db.save()