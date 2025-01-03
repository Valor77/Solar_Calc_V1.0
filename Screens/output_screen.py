from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem

class OutputScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.name = name

    def go_back(self):
        self.manager.current = "Solar Calc"
        self.parent.transition.direction = 'right'
