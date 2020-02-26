from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, ListProperty
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from patient import Patient


class MainWindow(Screen):
    
    content_main = ObjectProperty(None)
    button_home = ObjectProperty(None)
    button_create_patient = ObjectProperty(None)

    def change_content(self, name):
        for child in self.content_main.children: 
            if child.name == name:  # show child
                if hasattr(child, "attr_backup"):
                    child.height, child.size_hint_y, child.opacity, child.disabled = child.attr_backup
                    del child.attr_backup
                self.highlight_button(child)
                continue
            child.attr_backup = child.height, child.size_hint_y, child.opacity, child.disabled
            child.height, child.size_hint_y, child.opacity, child.disabled = 0, None, 0, True  # hide child
            child.reset()
            self.highlight_button(child, reset=True)

    def to_home(self):
        self.change_content("home")

    def to_create_patient(self):
        self.change_content("create_patient")

    def highlight_button(self, widget, reset=False):
        button = getattr(self, "button_" + widget.name)
        if reset:
            button.background_color = [1, 1, 1, 1]
            return
        button.background_color = button.highlight_color


class MainContentHome(AnchorLayout):
    name = StringProperty(None)
    dynamic_search = ObjectProperty(None)

    def on_enter(self):
        self.reset()

    def reset(self):
        self.dynamic_search.text_input.text = ""
        self.dynamic_search.selection.data = []


class MainContentCreatePatient(AnchorLayout):
    
    name = StringProperty(None)
    checkbox_gender_is_male = BooleanProperty(None)
    input_surname = ObjectProperty(None)
    input_first_name = ObjectProperty(None)
    input_birthday_day = ObjectProperty(None)
    input_birthday_month = ObjectProperty(None)
    input_birthday_year = ObjectProperty(None)
    input_phone = ObjectProperty(None)

    def on_enter(self):
        self.reset()
   
    def create_patient(self):
        app = App.get_running_app()
        db = app.DB
        birthday = "{:02d}".format(int(self.input_birthday_day.text)) + "." + "{:02d}".format(int(self.input_birthday_month.text)) + "." + str(self.input_birthday_year.text)
        gender = Patient.GENDER_M
        if not self.checkbox_gender_is_male:
            gender = Patient.GENDER_F
        if len(self.input_surname.text) > 0 and len(self.input_first_name.text) > 0 and len(self.input_phone.text) > 0:
            patient = Patient(db, self.input_surname.text, self.input_first_name.text, birthday, gender, self.input_phone.text)
            try:
                patient.save()
                Factory.PatientCreationSuccessPopup().open()
                app.root.get_screen(app.root.current).to_home()
            except Exception as e:
                print(e)
                Factory.PatientCreationFailedPopup().open()
        else:
            Factory.PatientCreationInputFailedPopup().open()

    def reset(self):
        self.checkbox_gender_is_male = True
        self.input_surname.text = ""
        self.input_first_name.text = ""
        self.input_birthday_day.text = "1"
        self.input_birthday_month.text = "1"
        self.input_birthday_year.text = "1990"
        self.input_phone.text = ""
