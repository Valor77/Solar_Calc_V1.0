from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty

class CustomOneLineListItem(MDBoxLayout):
    text = StringProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.add_widget(MDLabel(text=self.text))