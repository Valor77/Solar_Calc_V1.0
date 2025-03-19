from kivy.lang import Builder
from kivy.properties import StringProperty
import os
import json
import sys
from kivy.clock import Clock

from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationBar, MDNavigationItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from Screens.home_screen import HomeScreen
from Screens.input_screen import InputScreen
from Screens.output_screen import OutputScreen
from Screens.saved_data_screen import SavedDataScreen
from Screens.reports_screen import ReportsScreen

from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from custom_list_item import CustomOneLineListItem
from Solar_database import insert_file, get_files



from fpdf import FPDF
from kivy.uix.screenmanager import Screen
from kivy.app import App
from datetime import datetime




from database import initialize_database, insert_file, get_saved_files
import sqlite3








class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class BaseScreen(MDScreen):
    pass

Builder.load_file("Screens/input_screen.kv")
Builder.load_file("Screens/output_screen.kv")
Builder.load_file("Screens/saved_data_screen.kv")
Builder.load_file("Screens/reports_screen.kv")






class Kingsley(MDApp):
    # def build(self):
    #     Builder.load_file("Solar_main.kv")  # Load main KV file
        
    #     sm = MDScreenManager()

    #     sm.add_widget(HomeScreen(name="Home"))
    #     sm.add_widget(ReportsScreen(name="reports"))  # Register ReportsScreen
        # return sm

   
    def build(self):
        Clock.schedule_once(lambda dt: self.update_saved_files_list())
        return Builder.load_file("Solar_main.kv")

    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     self.filechooser_open = False    

    # def on_switch_tabs(self, bar, item, item_icon, item_text):
    #     self.root.ids.screen_manager.current = item_text

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.filechooser_open = False
        # Builder.load_file("Solar_main.kv")
        self.calculated_results = {}
        initialize_database()    

    def on_switch_tabs(self, bar, item, item_icon, item_text):
        self.root.ids.screen_manager.current = item_text

    def toggle_nav_drawer(self):
        self.root.ids.nav_drawer.set_state("toggle")

    def go_home(self):
        self.root.ids.screen_manager.current = "Home"
        self.root.ids.screen_manager.transition.direction = 'right'
        for item in self.root.ids.navigation_bar.children:
            if isinstance(item, MDNavigationItem):
                item.active = (item.text == "Home")



    def save_results(self):
        """Generate a PDF and save report details in the database."""

        # Call export_to_data_base() and get file details
        file_path, file_name, timestamp = self.export_to_data_base(self.calculated_results)

        # Connect to database
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()

        # Insert into reports table
        cursor.execute("""
            INSERT INTO reports (file_name, file_path, timestamp)
            VALUES (?, ?, ?)
        """, (file_name, file_path, timestamp))

        # Commit and close connection
        conn.commit()
        conn.close()

        print(f"Report saved: {file_name} at {file_path}")



    def on_popup_dismiss(self, instance):
        self.filechooser_open = False

    def on_file_chooser_selection(self, selection, data):
        if selection:
            self.popup.dismiss()
            self.prompt_file_name(selection[0], data)

    def prompt_file_name(self, folder_path, data):
        content = MDBoxLayout(orientation='vertical')
        file_name_input = MDTextField(hint_text='Enter file name', multiline=False)
        content.add_widget(MDLabel(text='Enter file name:'))
        content.add_widget(file_name_input)

        def save_file(instance):
            file_name = file_name_input.text
            if file_name:
                file_path = os.path.join(folder_path, file_name + '.pdf')
                self.export_to_pdf(data, file_path)
                insert_file(file_name, file_path)
                self.update_saved_files_list()
                self.file_name_popup.dismiss()

        save_button = MDButton(MDButtonText(text='Save'), style="elevated", on_release=save_file, size_hint_y=None, height=40)
        close_button = MDButton(MDButtonText(text='Close'), style="elevated", on_release=lambda x: self.file_name_popup.dismiss(), size_hint_y=None, height=40)
        
        button_layout = MDBoxLayout(orientation='horizontal')
        button_layout.add_widget(save_button)
        button_layout.add_widget(close_button)
        content.add_widget(button_layout)

        self.file_name_popup = Popup(title='Save File', content=content, size_hint=(0.9, 0.5), auto_dismiss=True)
        self.file_name_popup.open()

    def on_pre_enter(self):
        
        """Fetch stored results from MDApp before displaying the screen."""
        app = App.get_running_app()
        calculated_results = app.calculated_results  # Get stored results

        if not isinstance(calculated_results, dict):
            calculated_results = {}

        # Update UI elements with stored data
        self.ids.inverter_size.text = calculated_results.get("inverter_size", "N/A")
        self.ids.battery_count.text = calculated_results.get("battery_count", "N/A")
        self.ids.panel_count.text = calculated_results.get("panel_count", "N/A")
        self.ids.charger_controller.text = calculated_results.get("charger_controller", "N/A")
        self.ids.battery_setup.text = calculated_results.get("battery_setup", "N/A")
        self.ids.system_voltage.text = calculated_results.get("system_voltage", "N/A")
        self.ids.total_energy_demand.text = calculated_results.get("total_energy_demand", "N/A")
        self.ids.battery_bank_energy_capacity.text = calculated_results.get("battery_bank_energy_capacity", "N/A")
        self.ids.daily_solar_energy_generation_needed.text = calculated_results.get("daily_solar_energy_generation_needed", "N/A")
        self.ids.solar_panel_array_power.text = calculated_results.get("solar_panel_array_power", "N/A")
        self.ids.expected_system_losses.text = calculated_results.get("expected_system_losses", "N/A")
        self.ids.maximum_load_capacity.text = calculated_results.get("maximum_load_capacity", "N/A")




    def export_to_data_base(self, data):
        """Generate a PDF and return file details."""
        
        app = MDApp.get_running_app()
        calculated_results = app.calculated_results

        # Define storage folder
        save_folder = os.path.join(os.getcwd(), "saved_reports")
        os.makedirs(save_folder, exist_ok=True)

        # Generate file name and timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        file_name = f"solar_report_{timestamp}.pdf"
        file_path = os.path.join(save_folder, file_name)

        if getattr(sys, 'frozen', False):
            app_path = sys._MEIPASS  # Compiled app path
        else:
            app_path = os.path.dirname(__file__)  # Normal script path

        letterhead_path = os.path.join(app_path, "assets", "letterhead.png")

        # Create PDF
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Insert the letterhead image if it exists
        if os.path.exists(letterhead_path):
            pdf.image(letterhead_path, x=10, y=8, w=190)  # Adjust width and positioning
            pdf.ln(55)  # Add space below the image    

        pdf.cell(200, 10, "D.E.I Solar Calculation Report", ln=True, align='C')
        pdf.ln(10)

        # Set normal font for report details
        pdf.set_font("Arial", size=12)

        # Format the results with better display
        for key, value in calculated_results.items():
            formatted_key = key.replace("_", " ").title()  # Replace underscores and capitalize words

            # Ensure numbers are formatted nicely
            if isinstance(value, (int, float)):
                value = f"{value:,.2f}"  # Adds comma separation and rounds to 2 decimal places

            pdf.cell(0, 10, f"{formatted_key}: {value}", ln=True)



        # # Write data to PDF
        # for key, value in calculated_results.items():
        #     pdf.cell(0, 10, f"{key}: {value}", ln=True)

        # Save PDF
        pdf.output(file_path)
        
        print("PDF exported successfully!")
        
        # Return values
        return file_path, file_name, timestamp




    def update_saved_files_list(self):
        saved_data_screen = self.root.ids.nav_screen_manager.get_screen('saved_data')
        saved_files_list = saved_data_screen.ids.saved_files_list
        saved_files_list.clear_widgets()
        
        files = get_files()
        for file in files:
            item = CustomOneLineListItem(text=file.name, on_release=lambda x=file.path: self.show_file_popup(x))
            saved_files_list.add_widget(item)




    def open_reports_screen(self):
        """Switch to the Reports screen"""
        self.root.ids.screen_manager.current = "reports"


    

    def show_file_popup(self, file_path):
        content = MDBoxLayout(orientation='vertical')
        content.add_widget(MDLabel(text=f"File Path: {file_path}"))
        
        export_button = MDButton(MDButtonText(text='Export'), style="elevated", on_release=lambda x: self.export_to_pdf_from_path(file_path), size_hint_y=None, height=40)
        close_button = MDButton(MDButtonText(text='Close'), style="elevated", on_release=lambda x: self.file_popup.dismiss(), size_hint_y=None, height=40)
        
        button_layout = MDBoxLayout(orientation='horizontal')
        button_layout.add_widget(export_button)
        button_layout.add_widget(close_button)
        content.add_widget(button_layout)
        
        self.file_popup = Popup(title='File Details', content=content, size_hint=(0.9, 0.5), auto_dismiss=True)
        self.file_popup.open()

if __name__ == "__main__":
    Kingsley().run()
