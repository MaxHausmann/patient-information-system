from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout):
    pass

class DSLabel(RecycleDataViewBehavior, Label):
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(DSLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        if super(DSLabel,self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected

class DSTextInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        self.parent.print_text(text)
        return super(DSTextInput, self).keyboard_on_key_down(window, keycode, text, modifiers)

class DSSelection(RecycleView):
    def __init__(self, **kwargs):
        super(DSSelection, self).__init__(**kwargs)
        self.data = [{'text' : str(x)} for x in range(1)]

class DynamicSearch(BoxLayout):
    text_input = ObjectProperty(None)
    selection = ObjectProperty(None)

    def print_text(self, text):
        self.selection.data.append({'text': text})

    

    
    
    