import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from database import Database
from loginWindow import LoginWindow
from createAccountWindow import CreateAccountWindow
from mainWindow import MainWindow
  

class MainApp(App): 

    def build(self): 
        self.DB = Database("database/database.sqlite3")
        #return Builder.load_file("main.kv")
  
if __name__=='__main__': 
    MainApp().run() 