from kivy.lang import Builder
from kivy.properties import StringProperty
import os
import json
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen

from kivymd.uix.screenmanager import MDScreenManager
from Screens.home_screen import HomeScreen
from Screens.input_screen import InputScreen
from Screens.output_screen import OutputScreen
from Screens.saved_data_screen import SavedDataScreen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import (
    MDNavigationDrawerItem, MDNavigationDrawerItemTrailingText
)
from kivymd.uix.button import MDButton,MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDExtendedFabButton

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from kivymd.uix.dropdownitem import MDDropDownItem
from custom_list_item import CustomOneLineListItem
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.uix.button import Button


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class BaseScreen(MDScreen):
    pass

# class SavedDataScreen(MDScreen):
#     pass

# class OutputScreen(MDScreen):
#     pass

# class OutputScreen(MDScreen):
#     pass

Builder.load_file("Screens/input_screen.kv")
Builder.load_file("Screens/output_screen.kv")
Builder.load_file("Screens/saved_data_screen.kv")

# class DrawerLabel(MDBoxLayout):
#     text = StringProperty()
#     icon = StringProperty()

    
class Kingsley(MDApp):
    saved_files = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filechooser_open = False    

    def on_switch_tabs(
        self,
        bar: MDNavigationBar,
        item: MDNavigationItem,
        item_icon: str,
        item_text: str,
        
    ):
        self.root.ids.screen_manager.current = item_text

    def build(self):
        self.load_saved_files()
        def semi_func(dt):
            self.root.ids.screen_manager.current = 'Home'
        Clock.schedule_once(semi_func)
        
        return Builder.load_file("Solar_main.kv")
    
    def toggle_nav_drawer(self):
        self.root.ids.nav_drawer.set_state("toggle")

    def go_home(self):
        self.root.ids.screen_manager.current = "Home"
        self.root.ids.screen_manager.transition.direction = 'right'
        # Update the navigation bar to reflect the current screen
        # self.root.ids.navigation_bar.set_current("Home")
        for item in self.root.ids.navigation_bar.children:
            if isinstance(item, MDNavigationItem):
                item.active = (item.text == "Home")



    #  now we gats to save them files somewhere don't we?
    #  I'm thinking we could save them in a pdf file
    def save_results(self):
        # Create a popup to ask for the file name   

        if self.filechooser_open:
            return
        
        self.filechooser_open = True

        # Gather data from the results screen
        data = {
            'text': ["Result 1: 123", "Result 2: 456"],
            'table': [["Header 1", "Header 2"], ["Value 1", "Value 2"], ["Value 3", "Value 4"]]
        }

        # Create a FileChooserListView set to select directories
        self.filechooser = FileChooserListView(path=os.path.expanduser('~'), dirselect=True, filters=['!*.sys', '!.*'])
        # self.filechooser.bind(on_selection=lambda instance, selection: self.on_file_chooser_selection(instance, selection, data))
        # output_screen = self.root.ids.screen_manager.get_screen('output')
        # output_screen.ids.output_screen_layout.add_widget(self.filechooser)

        # TO Create a custom layout for the popup window
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(self.filechooser)

        # Add a "Select" button to the layout
        select_button = MDButton(
                            MDButtonText(
                                text='Select'),
                            style= "elevated",
                            size_hint_y=None, height=40)
        

        select_button.bind(on_release=lambda x: self.on_file_chooser_selection(self.filechooser, self.filechooser.selection, data))
        layout.add_widget(select_button)

        # Create a popup and add the FileChooserListView to it
        self.popup = Popup(title = "Select Folder", 
                           content = layout,
                           size_hint = (0.7, 0.7),
                           auto_dismiss = True)
        self.popup.bind(on_dismiss= self.on_popup_dismiss)
        self.popup.open()

    def on_popup_dismiss(self, instance):
        self.filechooser_open = False


# omor this thing keeps getting complex
    def on_file_chooser_selection(self, instance, selection, data):
        if selection:
            selected_folder = selection[0]
            self.popup.dismiss()
            # self.filechooser_open = False

            # Create a popup to ask for the file name
            self.prompt_file_name(selected_folder, data)

    # collect the file name
    def prompt_file_name(self, folder_path, data):
        content = MDBoxLayout(orientation='vertical',md_bg_color = [0,0,1,.4])
        file_name_input = MDTextField(hint_text='Enter file name', multiline=False,background_color = [1,1,1,1])
        content.add_widget(MDLabel(text='Enter file name:'))
        content.add_widget(file_name_input)

        def save_file(instance):
            file_name = file_name_input.text
            if file_name:
                file_path = os.path.join(folder_path, file_name + '.pdf')
                self.export_to_pdf(data, file_path)
                self.saved_files.append(file_path)
                self.save_saved_files()
                self.update_saved_files_list()
                self.file_name_popup.dismiss()

        # save_button = MDButton(text='Save', on_release=save_file)

        save_button = MDButton(
                            
                            MDButtonText(
                                text='Save'),
                            style= "elevated",on_release=save_file,
                            size_hint_y=None, height=40)
        
        close_button = MDButton(
                            MDButtonText(
                                text='close'),
                            style= "elevated",on_release=lambda x: self.file_name_popup.dismiss(),
                            size_hint_y=None, height=40)


        # close_button = MDButton(text='Close', on_release=lambda x: self.file_name_popup.dismiss())
        button_layout = MDBoxLayout(orientation='horizontal')
        button_layout.add_widget(save_button)
        button_layout.add_widget(close_button)
        content.add_widget(button_layout)

        self.file_name_popup = Popup(title='Save File',
                                     content=content,
                                     size_hint=(0.9, 0.5),
                                     auto_dismiss=True)
        self.file_name_popup.open()


    def export_to_pdf(self, data, file_path):
        c = canvas.Canvas(file_path, pagesize=letter)
        width, height = letter

        # Add title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "Results")

        # Add data (example: text and table)
        c.setFont("Helvetica", 12)
        y = height - 150
        for line in data['text']:
            c.drawString(100, y, line)
            y -= 20

        # Add table (example)
        table_data = data['table']
        x = 100
        y -= 40
        for row in table_data:
            for cell in row:
                c.drawString(x, y, cell)
                x += 100
            y -= 20
            x = 100

        c.save()

    def update_saved_files_list(self):
        # saved_files_list = self.root.ids.saved_data.ids.saved_files_list
        saved_data_screen = self.root.ids.nav_screen_manager.get_screen('saved_data')
        # saved_data_screen = self.root.ids.saved_data_screen

        saved_files_list = saved_data_screen.ids.saved_files_list
    
        saved_files_list.clear_widgets()
        for file_path in self.saved_files:
            item = CustomOneLineListItem(text=file_path, on_release=lambda x=file_path: self.export_file(x))
            saved_files_list.add_widget(item)

    def export_file(self, file_path):
        # Implement the function to export the file
        print(f"Exporting file: {file_path}")

    def load_saved_files(self):
        if os.path.exists("saved_files.json"):
            with open("saved_files.json", "r") as f:
                self.saved_files = json.load(f)

    def save_saved_files(self):
        with open("saved_files.json", "w") as f:
            json.dump(self.saved_files, f)



if __name__ == "__main__":
    # SolarCalculatorApp().run()
    Kingsley().run()


# # -----------------------------------------------------------

# class SolarCalculatorApp(MDApp):
    
#     def build(self):
#         # app = self.get_running_app()
#         self.sm = MDScreenManager()

#         self.hs = HomeScreen(name="home")
#         self.sm.add_widget(self.hs)
        
#         self.input_screen = InputScreen(name="Solar Calc")
#         self.sm.add_widget(self.input_screen)
        
#         self.output_screen = OutputScreen(name="output")
#         self.sm.add_widget(self.output_screen)

#         self.saved_data_screen = SavedDataScreen(name="saved_data")
#         self.sm.add_widget(self.saved_data_screen)
        
#         self.sm.current = 'input'

#         # sm = MDScreenManager()
#         # sm.add_widget(HomeScreen(name="home"))
#         # sm.add_widget(InputScreen(name="input"))
#         # sm.add_widget(OutputScreen(name="output"))
#         # sm.current = 'home'

#         # print(sm.children, sm.current)
#         # print(sm.children[0].children)
#         # sm = MDScreenManager()
#         # Clock.schedule_once(lambda dt: setattr(sm, 'current', 'home'),.1)
#         return self.sm

    # def slander(self): print("Slander")
        
    #     return sm


