from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, ListProperty
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.clock import Clock

from user import User
from patient import Patient
from patient_overview import MainContentPatientOverview

class MainWindow(Screen):
    
    label_username = ObjectProperty(None)
    label_status = ObjectProperty(None)
    content_main = ObjectProperty(None)
    button_home = ObjectProperty(None)
    button_create_patient = ObjectProperty(None)
    button_patient_overview = ObjectProperty(None)
    current_child = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        Clock.schedule_once(self.fetch_userdata)

    def init_view(self, name):
        self._content_changeover(name)

    def change_content(self, name):
        """
        manage change-content procedure:
            - prevent from loading if same button is pressed again
            - handles callbacks (on_leave-event) for popups etc.
            - triggers changeover
        """
        if self.current_child.name == name:
            return

        if hasattr(self.current_child, "on_leave"):
            self.current_child.on_leave(self._content_changeover, name)
        else:
            self._content_changeover(name)

    def _content_changeover(self, name):
        for child in self.content_main.children: 
            if child.name == name:  # show child
                if hasattr(child, "attr_backup"):
                    child.height, child.size_hint_y, child.opacity, child.disabled = child.attr_backup
                    del child.attr_backup
                self.current_child = child
                Clock.schedule_once(child.on_enter)
                self.highlight_button(child)
                continue
            if not hasattr(child, "attr_backup"):
                child.attr_backup = child.height, child.size_hint_y, child.opacity, child.disabled
            child.height, child.size_hint_y, child.opacity, child.disabled = 0, None, 0, True  # hide child
            self.highlight_button(child, reset=True)

    def to_home(self):
        self.change_content("home")

    def to_create_patient(self):
        self.change_content("create_patient")

    def to_patient_overview(self):
        self.change_content("patient_overview")

    def highlight_button(self, widget, reset=False):
        button = getattr(self, "button_" + widget.name)
        if reset:
            button.background_color = [1, 1, 1, 1]
            return
        button.background_color = button.highlight_color

    def fetch_userdata(self, dt):
        app = App.get_running_app()
        user = User(app.DB).get_by_id(app.GLOBAL_USR_ID)
        self.label_username.text = "[b]{}, {}[/b]".format(user.surname, user.firstname)
        self.label_status.text = user.status.replace("medical_doctor", "Arzt")  # todo: fix

class MainContentHome(AnchorLayout):

    name = StringProperty(None)
    dynamic_search = ObjectProperty(None)

    def on_enter(self, dt):
        self._reset()

    def _reset(self):
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

    def on_enter(self, dt):
        self._reset()
   
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

    def _reset(self):
        self.checkbox_gender_is_male = True
        self.input_surname.text = ""
        self.input_first_name.text = ""
        self.input_birthday_day.text = "1"
        self.input_birthday_month.text = "1"
        self.input_birthday_year.text = "1990"
        self.input_phone.text = ""
