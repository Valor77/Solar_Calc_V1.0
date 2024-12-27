from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFabButton

def show_popup(title, message):
    dialog = MDDialog(
        title=title,
        text=message,
        buttons=[
            MDFabButton(text="Close", on_release=lambda x: dialog.dismiss())
        ],
    )
    dialog.open()
