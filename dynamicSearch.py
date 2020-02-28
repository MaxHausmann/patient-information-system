from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.app import App
from patient import Patient
import re


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):

    idx_child_selected = 0

    def select_next_child(self):
        self._unselect_all()
        self._fetch_selected_child()
        self.idx_child_selected += 1
        if self.idx_child_selected > len(self.children)-1:
            self.idx_child_selected = 0
        self.children[self.idx_child_selected].select()

    def select_prev_child(self):
        self._unselect_all()
        self._fetch_selected_child()
        self.idx_child_selected -= 1
        if self.idx_child_selected < 0:
            self.idx_child_selected = len(self.children)-1
        self.children[self.idx_child_selected].select()

    def get_selected_child(self):
        return self.idx_child_selected

    def _fetch_selected_child(self):
        idx_child = 0
        for child in self.children:
            idx_child += 1
            if child.selected:
                self.idx_child_selected = idx_child

    def _unselect_all(self):
        for child in self.children:
            child.select(False)

class DSLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    patient_id = NumericProperty()

    def __init__(self, **kwargs):
       super(DSLabel, self).__init__(**kwargs)

    def refresh_view_attrs(self, rv, index, data):
        """
        reset crucial parameters in case of recycling
        """
        self.index = index
        self.selected = False
        self.selectable = True
        return super(DSLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(DSLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.select(is_selected)

    def select(self, sel=True):
        if self.selectable:
            self.selected = sel


class DSTextInput(TextInput):

    def insert_text(self, substring, from_undo=False):
        """input filtering: allowed: a-z, A-Z, 1x comma, 1x space."""
        match = re.match(r"[a-zA-Z\s,]", substring)
        if match:
            rtrn_text = match.group(0)
            if not (rtrn_text == "," and self.text.count(",") == 1) and not (rtrn_text == " " and self.text.count(" ") == 1): 
                return super(DSTextInput, self).insert_text(match.group(0), from_undo=from_undo)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 274:  # key 'down' pressed
            self.parent.select_next_item()
        elif keycode[0] == 273:  # key 'up' pressed
            self.parent.select_prev_item()
        elif keycode[0] == 13:  # key 'enter' pressed -> open patient
            self.parent.select_patient()
        else:
            self.parent.trigger_search()
        return super(DSTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)


class DSSelection(RecycleView):
    def __init__(self, **kwargs):
        super(DSSelection, self).__init__(**kwargs)


class DynamicSearch(BoxLayout):
    text_input = ObjectProperty(None)
    selection = ObjectProperty(None)
    item_container = ObjectProperty(None)
    trigger = None  # Clock-Event for triggering

    def trigger_search(self):
        if not self.trigger is None:
            Clock.unschedule(self.trigger)  # overflow protection
        if len(self.text_input.text) < 2:
            return
        self.selection.data = []
        self.trigger = Clock.schedule_once(self.search_patient, 0.5)
        Clock.schedule_once(self.highlight_search_text) #  trigger highlighter

    def select_next_item(self):
        self.item_container.select_next_child()

    def select_prev_item(self):
        self.item_container.select_prev_child()

    def select_patient(self):
        child_id = self.item_container.get_selected_child()
        patient_id = self.selection.data[child_id]["patient_id"]
        app = App.get_running_app()
        app.GLOBAL_PAT_ID = patient_id  # assign patient globally
        app.root.get_screen(app.root.current).to_patient_overview()

    def search_patient(self, dt):
        search_engine = Patient(App.get_running_app().DB)
        search_results = search_engine.get_dynamic_search(self.text_input.text)
        if len(search_results) < 1:
            self.selection.data.append({"text": "Keine Ergebnisse gefunden.", "selectable": False})
            return
        selection_first = True
        for patient in search_results:
            self.selection.data.append({"text": patient[1] + ", " + patient[2] + " - " + patient[4], "patient_id": patient[0]})
            if selection_first:
                selection_first = False
        self.highlight_search_text()

    def highlight_search_text(self, dt=None):
        highlighted = []
        for patient in self.selection.data:
            for m in re.finditer(self.text_input.text, patient["text"]):
                # slice text into pieces to insert markup elements to hightlight + hold other properties
                patient.update({"text": patient["text"][:m.start()] + "[b]" + patient["text"][m.start():m.end()] + "[/b]" + patient["text"][m.end():]})
                highlighted.append(patient)     
        self.selection.data = highlighted # overwrite old data list