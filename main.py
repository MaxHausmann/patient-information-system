from kivy import Config
# set minimum screen dimensions
Config.set("graphics", "minimum_width", 1280)
Config.set("graphics", "minimum_height", 800)
from kivy.app import App

from database import Database
from loginWindow import LoginWindow
from createAccountWindow import CreateAccountWindow
from mainWindow import MainWindow, MainContentCreatePatient, MainContentHome, MainContentPatientOverview
from pulse_measurement import PulsePlot
from dynamicSearch import DynamicSearch

class MainApp(App): 

    def build(self): 
        self.DB = Database("database/database.sqlite3")
        self.GLOBAL_PAT_ID = 13 # set back to 0
  
if __name__=='__main__': 
    MainApp().run()