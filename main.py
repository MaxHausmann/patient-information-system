from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from database import Database


class CreateAccountWindow(Screen):
    input_username = ObjectProperty(None)
    input_email = ObjectProperty(None)
    input_password = ObjectProperty(None)

    def btn_create_acc(self):
        db = MainApp.get_running_app().DB
        if self.input_username.text != "" and self.input_email.text != "" and self.input_email.text.count("@") == 1 and self.input_email.text.count(".") > 0:
            if self.input_password != "":
                db.add_user(self.input_email.text, self.input_password.text, self.input_username.text)
                MainWindow.current = self.input_username.text
                self.reset()
                self.manager.current = "main"
            else:
                invalidForm()
        else:
            invalidForm()

    def btn_abort(self):
        self.reset()
        self.manager.current = "login"

    def reset(self):
        self.input_email.text = ""
        self.input_password.text = ""
        self.input_username.text = ""


class LoginWindow(Screen):
    input_username = ObjectProperty(None)
    input_password = ObjectProperty(None)

    def btn_login(self):
        db = MainApp.get_running_app().DB
        if db.validate(self.input_username.text, self.input_password.text):
            MainWindow.current = self.input_username.text
            self.reset()
            self.manager.current = "main"
        else:
            invalidLogin()

    def btn_create_acc(self):
        self.reset()
        self.manager.current = "create_acc"

    def reset(self):
        self.input_username.text = ""
        self.input_password.text = ""


class MainWindow(Screen):
    n = ObjectProperty(None)
    created = ObjectProperty(None)
    email = ObjectProperty(None)
    current = ""

    def logOut(self):
        self.manager.current = "login"

    def on_enter(self, *args):
        db = MainApp.get_running_app().DB
        password, name, created = db.get_user(self.current)
        self.n.text = "Account Name: " + name
        self.email.text = "Email: " + self.current
        self.created.text = "Created On: " + created

class MainApp(App):
    def build(self):
        self.DB = Database("database/database.sql")
        return Builder.load_file("template_files/my.kv")

if __name__ == "__main__":
    MainApp().run()