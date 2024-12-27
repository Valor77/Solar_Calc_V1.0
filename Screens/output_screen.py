from kivymd.uix.screen import MDScreen

class OutputScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.name = name

    def go_back(self):
        self.manager.current = "Solar Calc"
        self.parent.transition.direction = 'right'
