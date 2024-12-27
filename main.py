from kivy.lang import Builder
from kivy.properties import StringProperty
import os

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen

from kivymd.uix.screenmanager import MDScreenManager
from Screens.input_screen import InputScreen
from Screens.output_screen import OutputScreen

from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDExtendedFabButton
from kivy.clock import Clock
# MDTextField(hint_text_color)

class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class BaseScreen(MDScreen):
    pass

# class OutputScreen(MDScreen):
#     pass

# class OutputScreen(MDScreen):
#     pass

Builder.load_file("Screens/input_screen.kv")
Builder.load_file("Screens/output_screen.kv")
    
class Example(MDApp):
    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
        
    ):
        self.root.ids.screen_manager.current = item_text

    def build(self):

        def semi_func(dt):
            self.root.ids.screen_manager.current = 'Solar Calc'
        Clock.schedule_once(semi_func)
        
        return Builder.load_file("Solar_main.kv")

class SolarCalculatorApp(MDApp):
    
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(InputScreen(name="input"))
        sm.add_widget(OutputScreen(name="output"))
        sm.current = 'input'
        # print(sm.children, sm.current)
        # print(sm.children[0].children)
        # sm = MDScreenManager()
        return sm

    # trying to display files..
    # def build(self):

    #     current_dir = os.path.dirname(__file__)
    #     screen1_kv =os.path.join(current_dir, 'Screens', 'input_screen.kv')
    #     screen2_kv =os.path.join(current_dir, 'Screens', 'output_screen.kv')

    #     Builder.load_file(screen1_kv)
    #     Builder.load_file(screen2_kv)

    # def build(self):
    #     sm = MDScreenManager()
    #     sm.add_widget(InputScreen(name="input"))
    #     sm.add_widget(OutputScreen(name="output"))
        
    #     return sm

if __name__ == "__main__":
    # SolarCalculatorApp().run()

    Example().run()