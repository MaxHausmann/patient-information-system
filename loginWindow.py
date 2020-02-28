from user import User
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.factory import Factory

"""
Class for login window
"""

class LoginWindow(Screen):
    input_username = ObjectProperty(None)
    input_password = ObjectProperty(None)

    def btn_login(self):
        db = App.get_running_app().DB
        user = User(db)
        if user.exist(self.input_username.text):
            user = user.get_by_username(self.input_username.text)
            if user.check_password(self.input_password.text):
                self.reset()
                self.manager.current = "main"
                App.get_running_app().GLOBAL_USR_ID = user.id
            else:
                Factory.InvalidLoginPopup().open()
        else:
            Factory.InvalidLoginPopup().open()

    def btn_create_acc(self):
        self.reset()
        self.manager.current = "create_acc"

    def reset(self):
        self.input_username.text = ""
        self.input_password.text = ""
