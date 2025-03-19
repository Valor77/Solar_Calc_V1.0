from kivymd.uix.screen import MDScreen
from custom_list_item import CustomOneLineListItem
from kivy.properties import StringProperty
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from Solar_database import get_files


class CustomOneLineListItem(CustomOneLineListItem):
    text = StringProperty()

class SavedDataScreen(MDScreen):
    def on_enter(self):
        self.load_files()

    def load_files(self):
        files = get_files()
        for file in files:
            item = CustomOneLineListItem(text=file.name)
            item.bind(on_release=self.view_pdf)
            self.ids.file_list.add_widget(item)


    def view_pdf(self, instance):
        pdf_path = instance.text  # Assuming the text contains the file path
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=f"Viewing PDF: {pdf_path}"))
        export_button = Button(text="Export", size_hint_y=None, height=40)
        export_button.bind(on_release=lambda x: self.export_pdf(pdf_path))
        content.add_widget(export_button)
        popup = Popup(title="PDF Viewer", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def export_pdf(self, pdf_path):
        content = BoxLayout(orientation='vertical')
        filechooser = FileChooserIconView()
        content.add_widget(filechooser)
        select_button = Button(text="Select Folder", size_hint_y=None, height=40)
        select_button.bind(on_release=lambda x: self.save_pdf(filechooser.path, pdf_path))
        content.add_widget(select_button)
        popup = Popup(title="Select Export Folder", content=content, size_hint=(0.9, 0.9))
        popup.open()

    def save_pdf(self, folder_path, pdf_path):
        import shutil
        shutil.copy(pdf_path, folder_path)
        print(f"Exported {pdf_path} to {folder_path}")