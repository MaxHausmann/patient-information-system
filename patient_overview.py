from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import ObjectProperty, BooleanProperty, StringProperty, ListProperty, NumericProperty
from kivy.factory import Factory
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.animation import Animation

from patient import Patient
from patientDiagnostics import PatientDiagnostics
from image_processing import ImageProcessing
from user import User

import os
import glob
from shutil import copyfile
from datetime import datetime
from dateutil.relativedelta import relativedelta

class MainContentPatientOverview(AnchorLayout):

    name = StringProperty(None)
    diagnostics = ObjectProperty(None)
    appraisal = ObjectProperty(None)
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
        """
        trigger all other on_enter events and hand in patient-obj
        """
        self.diagnostics.on_enter(self.patient)
        self.appraisal.on_enter(self.patient)

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


class Appraisal(BoxLayout):

    FILE_TYPE = ".jpeg"
    PATH = "patients/{}/ap/{}" + FILE_TYPE
    appraisal_list = ObjectProperty(None)

    """
    filters available and true/false if they accept one input value
    """
    FILTERS = [[ImageProcessing.inversion, False], 
               [ImageProcessing.binarization, True], 
               [ImageProcessing.gamma_correction, True],
               [ImageProcessing.smoothing, False],
               [ImageProcessing.vert_edge_detection, False],
               [ImageProcessing.hor_edge_detection, False]]

    def on_enter(self, patient):
        self.patient = patient
        self.fetch_images()

    def fetch_images(self):
        self.appraisal_list.reset()
        app = App.get_running_app()
        for img in self.get_images_in_folder():
            self.appraisal_list.add_image(img)

    def show_load(self):
        content = AppraisalImageLoadDialog(load=self.load_image, cancel=self.dismiss_load_popup)
        self._popup_load = Popup(title="Bild öffnen", content=content, size_hint=(0.5, 0.5))
        self._popup_load.open()

    def show_edit(self, source):
        content = AppraisalImageEditDialog(source=source, save=self.save_image, cancel=self.dismiss_edit_popup)
        self._popup_edit = Popup(title="Bild bearbeiten", content=content, size_hint=(0.9, 0.9))
        self._popup_edit.open()

    def load_image(self, path, filename):
        new_count = len(self.get_images_in_folder()) + 1  # generate new name by counting existing images
        print("source: ", filename[0])
        print("dest: ", self.PATH.format(self.patient.id, new_count))
        copyfile(filename[0], self.PATH.format(self.patient.id, new_count))
        self.fetch_images()
        self.dismiss_load_popup()
        self.appraisal_list.highlight_last_image()
        
    def save_image(self, filter, value, source):
        filter_method = self.FILTERS[filter]
        if filter_method[1]:
            filter_method[0](source, value)
        else:
            filter_method[0](source)
        self.dismiss_edit_popup()
        self.appraisal_list.refresh_images()
        
    def dismiss_load_popup(self):
        self._popup_load.dismiss()

    def dismiss_edit_popup(self):
        self._popup_edit.dismiss()

    def get_images_in_folder(self):
        return glob.glob(self.PATH.format(self.patient.id, "*"))
   

class AppraisalView(RecycleView):

    def __init__(self, **kwargs):
        super(AppraisalView, self).__init__(**kwargs)
        self.reset()

    def add_image(self, path):
        self.data.append({"source": path, "first_button": False})

    def reset(self):
        self.data = []
        self.data.append({"first_button": True})
        
    def refresh_images(self):
        for images in self.children[0].children:
            images.refresh_image()


class AppraisalImage(Button):

    first_button = BooleanProperty(False)
    source = StringProperty()
    image = ObjectProperty()
    highlight = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(AppraisalImage, self).__init__(**kwargs)

    def refresh_image(self):
        self.image.reload()

    def check_highlight(self, dt):
        self.background_color = [0, 0.25, 1, 1]
        anim = Animation(background_color = [1, 1, 1, 1], duration = 4)
        anim.start(self)

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
            self.parent.parent.parent.parent.show_load() # todo: fix poor way of propagation
        else:
            self.parent.parent.parent.parent.show_edit(self.source)


class AppraisalImageEditDialog(FloatLayout):
    source = StringProperty()
    cancel = ObjectProperty(None)
    save = ObjectProperty(None)
    filter_selector = ObjectProperty(None)
    input_value = ObjectProperty(None)

    def apply_filter(self):
        filter_value = self.input_value.text
        try:
            filter_value = float(filter_value)
        except:
            filter_value = 0
        self.save(self.filter_selector.selected_filter, filter_value, self.source)


class AppraisalImageLoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    

class LeaveDialog(FloatLayout):
    cancel = ObjectProperty(None)
    leave = ObjectProperty(None)
    next_content = ObjectProperty(None)
    callback = ObjectProperty(None)


class FilterLine(BoxLayout):

    num = NumericProperty(None)
    
    def set_active(self):
        self.parent.selected_filter = self.num
