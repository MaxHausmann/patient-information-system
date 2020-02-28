from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, ListProperty
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button

from patient import Patient
from patientDiagnostics import PatientDiagnostics
from user import User

import os
from datetime import datetime
from dateutil.relativedelta import relativedelta

class MainContentPatientOverview(AnchorLayout):

    name = StringProperty(None)
    diagnostics = ObjectProperty(None)
    label_name = ObjectProperty(None)
    label_age = ObjectProperty(None)
    label_phone = ObjectProperty(None)

    def on_enter(self, dt):
        self.get_patient()
        self.fill_header()
        self.route_trigger()

    def on_leave(self, callback, next_content):
        content = LeaveDialog(cancel=self.cancel_leave, leave=self.accept_leave, callback=callback, next_content=next_content)
        self._popup_leave = Popup(title="Verlassen", content=content, size_hint=(0.5, 0.2))
        self._popup_leave.open()

    def cancel_leave(self):
        self._popup_leave.dismiss()

    def accept_leave(self, callback, next_content):
        self._popup_leave.dismiss()
        callback(next_content)

    def get_patient(self):
        app = App.get_running_app()
        db = app.DB
        self.patient = Patient(db).get_by_id(app.GLOBAL_PAT_ID)

    def fill_header(self):
        self.label_name.text = "[b]{}, {}[/b] ({})".format(self.patient.surname, self.patient.firstname, self.patient.gender)
        self.label_age.text = "{} JAHRE".format(self.calc_age(datetime.strptime(self.patient.birthday, "%d.%m.%Y")))
        self.label_phone.text = "TELEFON: {}".format(self.patient.phone)

    def route_trigger(self):
        self.diagnostics.on_enter(self.patient)

    @staticmethod
    def calc_age(birth):
        today = datetime.now()
        return relativedelta(today, birth).years


class Diagnostics(BoxLayout):
    button_save = ObjectProperty(None)
    input_diagnostics = ObjectProperty(None)
    list_diagnostics = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Diagnostics, self).__init__(**kwargs)
        
    def on_enter(self, patient):
        app = App.get_running_app()
        self.db = app.DB
        user = User(self.db).get_by_id(app.GLOBAL_USR_ID)
        self.diag = PatientDiagnostics(self.db, patient, user)
        self.update_diag()
        
    def save_diag(self):
        self.diag.add(self.input_diagnostics.text)
        self.input_diagnostics.text = ""
        self.update_diag()

    def update_diag(self):
        self.list_diagnostics.data = []
        for entry in self.diag.get_all()[1]:
            user = User(self.db).get_by_id(entry[2])
            date = datetime.strptime(entry[4], "%Y-%m-%d %H:%M:%S")
            content = "[b]{}[/b] [color=#007db8]({}, {}. am {:02d}.{:02d}.{:d}, {:02d}:{:02d} Uhr)[/color]".format(entry[3], 
                        user.surname, user.firstname[0], date.day, date.month, date.year, date.hour, date.minute)
            self.list_diagnostics.data.append({"text": content})


class DiagnosticsList(RecycleView):

    def __init__(self, **kwargs):
        super(DiagnosticsList, self).__init__(**kwargs)
        #self.data = [{'text': "27.02.2020, 15:03 Uhr - " + str(x)} for x in range(20)]

   
class AppraisalView(RecycleView):

    def __init__(self, **kwargs):
        super(AppraisalView, self).__init__(**kwargs)
        self.data = [{"first_button": True}] + [{"source": "patients/13/ap/" + str(x) + ".jpeg", "first_button": False} for x in range(1, 4)]


class AppraisalImage(Button):

    first_button = BooleanProperty(False)
    source = StringProperty()
    image = ObjectProperty()

    def refresh_view_attrs(self, rv, index, data):
        return super(AppraisalImage, self).refresh_view_attrs(rv, index, data)

    def on_first_button(self, instance, value):
        if value is True:
            self.image.height = 0
            self.image.width = 0
            self.text = "+"
            self.font_size = 50
        else:
            self.image.height = self.height * 0.9
            self.image.width = self.width * 0.9

    def on_release(self):
        if self.first_button:
            self.show_load()
        else:
            self.show_edit()

    def show_load(self):
        content = AppraisalImageLoadDialog(load=self.load_image, cancel=self.dismiss_load_popup)
        self._popup_load = Popup(title="Bild öffnen", content=content, size_hint=(0.5, 0.5))
        self._popup_load.open()

    def show_edit(self):
        content = AppraisalImageEditDialog(image="", save=self.save_image, cancel=self.dismiss_edit_popup)
        self._popup_edit = Popup(title="Bild bearbeiten", content=content, size_hint=(0.9, 0.9))
        self._popup_edit.open()

    def load_image(self, path, filename):
        print("File loaded.")
        self.dismiss_load_popup()

    def save_image(self):
        print("Image saved.")
        self.dismiss_edit_popup()

    def dismiss_load_popup(self):
        self._popup_load.dismiss()

    def dismiss_edit_popup(self):
        self._popup_edit.dismiss()


class AppraisalImageEditDialog(FloatLayout):
    image = StringProperty()
    cancel = ObjectProperty(None)
    save = ObjectProperty(None)

class AppraisalImageLoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    
class LeaveDialog(FloatLayout):
    cancel = ObjectProperty(None)
    leave = ObjectProperty(None)
    next_content = ObjectProperty(None)
    callback = ObjectProperty(None)