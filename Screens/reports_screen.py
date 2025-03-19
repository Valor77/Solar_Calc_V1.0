from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivymd.uix.list import MDListItem  # Updated import for latest KivyMD version
import sqlite3
import webbrowser

from kivymd.uix.list import MDListItem
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard



from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.metrics import dp

# Builder.load_file("Screens/reports_screen.kv")




# from functools import partial

class ReportsScreen(Screen):
    """Screen for displaying saved reports."""

    def on_enter(self):
        """Ensure the table exists and update saved reports when the screen is entered."""
        self.create_reports_table()  # Ensure table is created


        Clock.schedule_once(lambda dt: self.update_saved_reports(), 0)

    def create_reports_table(self):
        """Ensure the reports table exists before using it."""
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def update_saved_reports(self):
        """Fetch saved reports from the database and update the UI."""
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()

        # Fetch reports sorted by latest date
        cursor.execute("SELECT file_name, file_path, timestamp FROM reports ORDER BY timestamp DESC")
        reports = cursor.fetchall()

        conn.close()

        # Get the MDList where reports will be displayed
        saved_reports_list = self.ids.saved_reports_list

        # Clear previous items
        saved_reports_list.clear_widgets()




       # Add each report as a clickable item
        for file_name, file_path, timestamp in reports:
            item = MDCard(  # Wrap in MDCard for better appearance
                size_hint_y=None,
                height=dp(60),
                padding=[dp(10), dp(5), dp(10), dp(5)],
                radius=dp(10),
                ripple_behavior=True,  # Adds material click effect
                on_release=lambda x, path=file_path: self.open_report(path)  # Make entire card clickable
            )

            content = MDBoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                padding=[dp(10), 0, dp(10), 0]
            )

            label = MDLabel(
                text=f"{file_name} - {timestamp}",
                size_hint_x=1,  # Takes full width
                halign="left",
                valign="center"
            )

            icon = MDIconButton(
                icon="file-eye",  # Icon representing view action
                on_release=lambda x, path=file_path: self.open_report(path)
            )

            content.add_widget(label)
            content.add_widget(icon)
            item.add_widget(content)
            saved_reports_list.add_widget(item)
   




    def go_back(self):
        """Function to navigate back to the Output Screen"""
        self.manager.current = "output"

    def open_report(self, file_path):
        """Open the selected report file."""
        webbrowser.open(file_path)