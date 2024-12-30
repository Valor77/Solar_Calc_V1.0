from kivy.lang import Builder
from kivy.properties import StringProperty
import os
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen

from kivymd.uix.screenmanager import MDScreenManager
from Screens.home_screen import HomeScreen
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
    
class Kingsley(MDApp):
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
            self.root.ids.screen_manager.current = 'Home'
        Clock.schedule_once(semi_func)
        
        return Builder.load_file("Solar_main.kv")

class SolarCalculatorApp(MDApp):
    
    def build(self):
        sm = MDScreenManager()
        sm.add_widget(HomeScreen(name="home"))
        sm.add_widget(InputScreen(name="input"))
        sm.add_widget(OutputScreen(name="output"))
        sm.current = 'home'
        # print(sm.children, sm.current)
        # print(sm.children[0].children)
        # sm = MDScreenManager()
        # Clock.schedule_once(lambda dt: setattr(sm, 'current', 'home'),.1)
        return sm


        
    #     return sm

if __name__ == "__main__":
    # SolarCalculatorApp().run()

    Kingsley().run()