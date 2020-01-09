from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.app import App
from kivy.factory import Factory
from user import User

class CreateAccountWindow(Screen):
    input_username = ObjectProperty(None)
    input_email = ObjectProperty(None)
    input_password = ObjectProperty(None)

    def btn_create_acc(self):
        db = App.get_running_app().DB
        if self.input_username.text != "" and self.input_email.text != "" and self.input_email.text.count("@") == 1 and self.input_email.text.count(".") > 0:
            if self.input_password != "":
                name = self.input_username.text.split("_")
                user = User(db, self.input_username.text, self.input_password.text, self.input_email.text, name[0], name[1]).save()
                self.reset()
                self.manager.current = "main"
            else:
                Factory.InvalidInputPopup().open()
        else:
            Factory.InvalidInputPopup().open()

    def btn_abort(self):
        self.reset()
        self.manager.current = "login"

    def reset(self):
        self.input_email.text = ""
        self.input_password.text = ""
        self.input_username.text = ""