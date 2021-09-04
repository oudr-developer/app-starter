# THIS IS THE BACKEND OF THE APPLICATION 
# IT TAKE CARE OF LOADING DATA , SAVING DATA , OPENING APPS AND CLOSE THEM
import json
import os
# CLASSES 

class Task:
  def __init__(self,index,name):
    self.id = index 
    self.name = name
    self.apps = []
  def add_app(self,app):
    if isinstance(app,App): 
      app.set_index(len(self.apps))
      app.set_parent(self)
      self.apps.append(app)
  def set_name(self,name):
    self.name=name
    return self
  def remove_app(self,index):
    for app in self.apps:
      if app.get_index() == index:
        self.apps.remove(app)
  def get_app(self,idx):
    for app in self.apps:
      if app.get_index() == idx:
        return app
  def open_apps(self):
    for app in self.apps:
      app.open()
  def close_apps(self):
    for app in self.apps:
      try:
        app.close()
      except:pass
  def parse(self):
    return {
    'id':self.id,
    'name':self.name,
    'apps':[app.parse() for app in self.apps]
    }
  def __repr__(self):
    return f'Task:{self.id}<{",".join([app.name for app in self.apps])}>'

class App:
  def __init__(self,name):
    self.id = None
    self.path=None
    self.name='app' if name=='' else name
    self.filename = ''
  def set_path(self,path):
    self.path = path
    if self.path != None:
      self.name = self.path.split('/')[-1].lower().split('.')[0] if self.name=='app' else self.name
      self.filename = self.path.split('/')[-1]
  def get_index(self):
    return self.id
  def set_parent(self,parent):self.parent = parent
  def set_index(self,idx):
    self.id=idx
  def open(self):os.startfile(self.path)
  def close(self):
    os.system(f'TASKKILL /F /IM {self.filename}')
  def parse(self):
    return {
    'id':self.id,
    'path':self.path,
    'name':self.name
    }
  def __repr__(self):
    return f'App:{self.name}<{self.id}>'

class DataBase:
  def __init__(self):
    self.json = []
    self.data = []
  def set_data(self,tasks):
    self.json = []
    for i in range(len(tasks)):
      task = tasks[i]
      data = task.parse()
      self.json.append(data)
  def get_data(self):
    return self.data
  def save(self):
    file = open('db.json','r').read()
    data = [] if (file == '' or file =='null') else json.loads(file)
    dumbdata = json.dumps(self.json,indent=2)
    file =  open('db.json','w')
    file.write(dumbdata)
  def parse(self,dumbdata):
    
    self.data = []
    for task in dumbdata:
      my_task =Task(task['id'],task['name'])
      for i in range(len(task['apps'])):
        app = task['apps'][i]
        
        my_app = App(app['name'])
        
        my_app.set_index(app['id'])
        my_app.set_path(app['path'])
        my_task.add_app(my_app)
        
      self.data.append(my_task)
      
  def murge(self,array1,array2):
    array = []
    for item1 in array1:
      for item2 in array2:
        if item1['id'] == item2['id']:
          array.append(item1)
        else:
          array.append(item2)
    return array
  def upload(self):
    try:
      file = open('db.json','r').read()
      data = [] if (file == '' or file == 'null') else json.loads(file)
      self.parse(data)
    except:
      file = open('db.json','w')
      file.write('[]')

    