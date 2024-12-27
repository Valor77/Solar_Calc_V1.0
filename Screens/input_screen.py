from kivymd.uix.screen import MDScreen
from utils import show_popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

class InputScreen(MDScreen):

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.name = name
    #     box_layout = MDBoxLayout(orientation= 'vertical', md_bg_color=[1,0,1,1])
       
    #     label = MDLabel(text="show something")
    #     box_layout.add_widget(label)
       
    #     self.add_widget(box_layout)

    def check_float(self, val):
        if val != '' and isinstance(val, str):
            val = float(val)
        print(val)
        if isinstance(val, float) or isinstance(val, int):
            return float(val)
        else:
            return None
    
    def calculate(self):
        self.parent.transition.direction = 'left'

        

        try:
            # Fetch inputs
            estimated_load = self.check_float(self.ids.estimated_load.text)
            backup_hours = self.check_float(self.ids.backup_hours.text)
            peak_sun_hours = self.check_float(self.ids.peak_sun_hours.text)
            panel_efficiency = self.check_float(self.ids.panel_efficiency.text)
            values_ch = [estimated_load, backup_hours, peak_sun_hours, panel_efficiency]

            if not all(values_ch):
                print(all(values_ch))
                print(values_ch)
                return 

            # Validate inputs
            if not (1 <= panel_efficiency <= 99):
                self.ids.panel_efficiency.text = ''
                self.ids.panel_efficiency.helper_text = 'Panel Efficiency must be between 1 and 99 '
                self.ids.panel_efficiency.helper_text_color = (1,0,0,1)
                return
                raise ValueError("Panel efficiency must be between 1 and 99.")

            # Perform calculations
            inverter_size = estimated_load * 1.3  # Adding a 30% buffer

            system_voltage = 24 if estimated_load <= 3000 else 48  # Decide system voltage

            battery_capacity = (estimated_load * backup_hours) / system_voltage
            battery_count = round(battery_capacity / 200)  # Assume 200Ah batteries

            panel_output = (estimated_load / peak_sun_hours) * (100 / panel_efficiency)
            panel_count = round(panel_output / 300)  # Assume 300W panels

            charger_rating = panel_count * 300 / system_voltage  # Charger rating in Amps

            battery_setup = "Series" if battery_count > 1 else "Parallel"


            # Pass data to Output Screen
            result_screen = self.manager.get_screen("output")
            result_screen.ids.inverter_size.text = f"Inverter Size: {inverter_size:.2f} W"
            result_screen.ids.battery_count.text = f"Number of Batteries: {battery_count}"
            result_screen.ids.panel_count.text = f"Number of Panels: {panel_count}"
            result_screen.ids.charger_controller.text = f"Charger Controller: {charger_rating:.2f} A"
            result_screen.ids.battery_setup.text = f"Battery Bank Setup: {battery_setup}"
            result_screen.ids.system_voltage.text = f"Advised System Voltage: {system_voltage}V"

            self.manager.current = "output"

        except ValueError as ve:
            show_popup("Input Error", str(ve))
        except Exception as e:
            show_popup("Error", f"Unexpected error: {e}")
