from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)

    #def logOut(self):
    #    self.manager.current = "login"

    #def on_enter(self, *args):
    #    db = MainApp.get_running_app().DB
    #    password, name, created = db.get_user(self.current)
    #    self.n.text = "Account Name: " + name
    #    self.email.text = "Email: " + self.current
    #    self.created.text = "Created On: " + created
