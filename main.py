from kivy import Config
# set minimum screen dimensions
Config.set("graphics", "minimum_width", 800)
Config.set("graphics", "minimum_height", 800)
from kivy.app import App

from database import Database
from loginWindow import LoginWindow
from createAccountWindow import CreateAccountWindow
from mainWindow import MainWindow, MainContentCreatePatient, MainContentHome  
from dynamicSearch import DynamicSearch

class MainApp(App): 

    def build(self): 
        self.DB = Database("database/database.sqlite3")
  
if __name__=='__main__': 
    MainApp().run()