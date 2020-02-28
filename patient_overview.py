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

import os


class MainContentPatientOverview(AnchorLayout):

    diagnostics_view = ObjectProperty(None)

    def on_enter(self):
        app = App.get_running_app()
        db = app.DB
        patient = Patient(db).get_by_id(app.GLOBAL_PAT_ID)
        print(patient)
        
    def reset(self):
        pass


class DiagnosticsView(RecycleView):
    def __init__(self, **kwargs):
        super(DiagnosticsView, self).__init__(**kwargs)
        self.data = [{'text': "27.02.2020, 15:03 Uhr - " + str(x)} for x in range(20)]


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
    