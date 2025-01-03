from kivymd.uix.screen import MDScreen
from utils import show_popup
from kivy.metrics import dp 
from kivy.clock import Clock
# from kivymd.uix.spinner import MDSpinner
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivymd.uix.scrollview import MDScrollView, ScrollView
from kivymd.uix.dropdownitem import MDDropDownItem

import random
from kivymd.uix.list import MDList

class InputScreen(MDScreen):
    input_parent_box_layout = ObjectProperty()
    
    cow_count = NumericProperty(0)

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)



    def voltage_drop_menu(self, item):
        
        menu_items = [
            {"text": "12",  "on_release": lambda x="12": self.set_battery_item(x)},
            {"text": "24",  "on_release": lambda x="24": self.set_battery_item(x)},
            {"text": "48",  "on_release": lambda x="48": self.set_battery_item(x)},        
        ]
        self.voltage_menu = MDDropdownMenu(
            caller= item,
            items=menu_items,
            width_mult=4,
        )
        # self.menu.bind(on_release=self.set_item)
        self.voltage_menu.open()
    
    def set_battery_item(self, text_item):
        self.ids.system_voltage.text = text_item
        self.ids.system_voltage_text.text_color = (0,0,1,1)
        self.voltage_menu.dismiss()
        print("system_voltage.text", self.ids.system_voltage.text)

        # # scroll back to the top after selecting an item
        next_field = self.ids.estimated_load
        next_field.focus = True    
        self.ids.scroll_input_text_field.scroll_to(next_field, padding = 15)



# Drop down menu for battery type
    def drop_menu(self, item):
        
        menu_items = [
            {"text": "Dry Cell",  "on_release": lambda x="Dry Cell": self.set_item(x)},
            {"text": "Wet Cell",  "on_release": lambda x="Wet Cell": self.set_item(x)},
            {"text": "Lithium-ion",  "on_release": lambda x="Lithium-ion": self.set_item(x)},        
        ]
        self.menu = MDDropdownMenu(
            caller= item,
            items=menu_items,
            width_mult=4,
        )
        # self.menu.bind(on_release=self.set_item)
        self.menu.open()
    
    def set_item(self, text_item):
        self.ids.battery_type.text = text_item
        self.ids.battery_type_text.text = text_item
        self.ids.battery_type_text.text_color = (0,0,1,1)
        self.menu.dismiss()

        # scroll back to the top after selecting an item
        first_field = self.ids.estimated_load
        first_field.focus = True    
        self.ids.scroll_input_text_field.scroll_to(first_field, padding = 25)
    

# Padding in case of smaller screen
    def on_size(self, *args):
        print(self.size)

        if self.size[0] <= 600:
            self.ids.input_parent_box_layout.padding = [5,5,5,5]
            self.ids.text_field_box_layout.padding = [5,5,5,5]
            # self.ids.input_home_button.padding = [5,5,5,5]
        else:
            self.ids.input_parent_box_layout.padding = [20,5,20,5]
            self.ids.text_field_box_layout.padding = [5,30,5,30]
            # self.ids.input_home_button.padding = [20,5,20,5]

    def check_float_and_validate_range(self, val, comparism=range(0, 100)):
    # def check_float_and_validate_range(self, val):
        if val == '': return None
        try:
            val = float(val)
            if val not in comparism: return None
            return val
        except ValueError:
            return None
        
# focus on the next text field even if it's below screen level
    def focus_next_text_field(self, current_field):
        fields = [
            self.ids.estimated_load,
            self.ids.backup_hours,
            self.ids.peak_sun_hours,
            self.ids.rating_of_panels,
            self.ids.panel_efficiency,
            self.ids.battery_amps,
            self.ids.inverter_efficiency,
        
        ]
        try:
            current_index = fields.index(current_field)
            if current_index < len(fields) - 1:
                next_field = fields[current_index + 1]
                # next_field = fields[fields.index(current_field) + 1]
                next_field.focus = True
                padding = 25
                if current_index == len(fields) - 2:
                    padding = 60
                self.ids.scroll_input_text_field.scroll_to(next_field,padding = padding)
            
            else:
                # if the current field is hte last one before the drop-own menu,  trigger the drop down menu
                self.ids.battery_type.focus = True
                self.drop_menu(self.ids.battery_type)

        except (ValueError, IndexError):
            # If the current field is the last one, scroll back to the top
            first_field = fields[0]
            first_field.focus = True
            self.ids.scroll_input_text_field.scroll_to(first_field, padding = 25)


    
    def calculate(self):
        self.parent.transition.direction = 'left'

        try:
            # Loading indicator
            self.ids.loading_spinner.active = True

            # delay the calculations to allow the loading spinner to show
            Clock.schedule_once(self.perform_calculations, 0.5)

        except ValueError as ve:
            self.ids.loading_spinner.active = False
            show_popup("Input Error", str(ve))
        except Exception as e:
            self.ids.loading_spinner.active = False
            show_popup("Error", f"Unexpected error: {e}")

        
    def perform_calculations(self, dt):
        try:
            # Fetch inputs
            # validate the inputs, convert to float and check if they are within the specified range
            system_voltage = self.check_float_and_validate_range(self.ids.system_voltage.text, [12, 24, 48])
            estimated_load = self.check_float_and_validate_range(self.ids.estimated_load.text, range(1, 10000))
            backup_hours = self.check_float_and_validate_range(self.ids.backup_hours.text, range(1, 24))
            peak_sun_hours = self.check_float_and_validate_range(self.ids.peak_sun_hours.text, range(1, 24))
            rating_of_panels = self.check_float_and_validate_range(self.ids.rating_of_panels.text, range(1, 1000))
            panel_efficiency = self.check_float_and_validate_range(self.ids.panel_efficiency.text, range(1, 99))
            battery_amps = self.check_float_and_validate_range(self.ids.battery_amps.text, range(1, 1000))
            # system_voltage = self.check_float_and_validate_range(self.ids.system_voltage.text)
            inverter_efficiency = self.check_float_and_validate_range(self.ids.inverter_efficiency.text, range(1, 100))
            battery_type = self.ids.battery_type.text or None
            # battery_type = self.ids.battery_type.text if self.ids.battery_type.text != 'Select Battery Type' else None
            # battery_type = self.ids.battery_type.current_item if self.ids.battery_type.current_item != 'Select Battery Type' else None
            # '', 0, False, None, [], {}, ()
            try:
                system_voltage = int(self.ids.system_voltage.text)
            except ValueError:
                print("Invalid system voltage value") 

            print("battery_type.text", battery_type)
            print("system_voltage.text", system_voltage)


            fields = self.get_all_fields() # get all fields using the get_all_fields() method created for simplicity

            values_ch = [system_voltage, estimated_load, backup_hours, peak_sun_hours,
                         rating_of_panels,  panel_efficiency, battery_amps, inverter_efficiency, battery_type]

            for count, values in enumerate(values_ch): # check if any of the values is None
                if values is None:
                    field = fields[count] # get the field that has an error
                    field.text = ''
                    # field.helper_text = 'Field cannot be empty'
                    field.helper_text_color = (1,0,0,1)
                    field.error = True

            # if textfield
            # self.ids.estimated_load.

            if not all(values_ch) or battery_type == 'Select Battery Type':
                self.ids.loading_spinner.active = False
                show_popup("Input Error", "Please fill all fields with valid values")
                print(all(values_ch))
                print(values_ch)
                return 

            # Validate inputs
            if not (1 <= panel_efficiency <= 99):
                self.ids.panel_efficiency.text = ''
                self.ids.rating_of_panels.text = ''
                self.ids.panel_efficiency.helper_text = 'Panel Efficiency must be between 1 and 99 '
                self.ids.panel_efficiency.helper_text_color = (1,0,0,1)
                self.ids.loading_spinner.active = False
                return
                raise ValueError("Panel efficiency must be between 1 and 99.")
            


            
            # Determine depth of discharge (DoD) based on battery type
            if battery_type == "Dry Cell":
                dod = 0.50
            elif battery_type == "Wet Cell":
                dod = 0.65
            elif battery_type == "Lithium-ion":
                dod = 0.85
            else:
                raise ValueError("Unknown battery type")



            # Perform calculations
            inverter_size = estimated_load * (1 / (inverter_efficiency / 100))

            # Total energy storage required (Wh)
            total_energy_storage = estimated_load * backup_hours / dod

            # Assume battery voltage (e.g., 12V for lead-acid batteries)
            battery_voltage = 12

            # Number of batteries in series
            batteries_in_series = system_voltage / battery_voltage

            energy_capacity_per_string = battery_voltage * battery_amps  * batteries_in_series

            # Number of parallel strings
            parallel_strings = total_energy_storage / energy_capacity_per_string

            # Total number of batteries
            battery_count = round(batteries_in_series * parallel_strings)

            panel_output = (estimated_load / peak_sun_hours) * (panel_efficiency / 100)
            panel_count = round(panel_output / rating_of_panels)  

            charger_rating = panel_count * rating_of_panels / system_voltage  # Charger rating in Amps

            battery_setup = f"{int(batteries_in_series)} in series, {int(parallel_strings)} in parallel"

            # Additional Outputs
            total_energy_demand = estimated_load * backup_hours
            battery_bank_energy_capacity = battery_count * battery_amps * battery_voltage
            daily_solar_energy_generation_needed = total_energy_demand / (panel_efficiency / 100)
            solar_panel_array_power = panel_count * rating_of_panels
            expected_system_losses = total_energy_demand - (inverter_size * inverter_efficiency / 100)
            maximum_load_capacity = inverter_size * inverter_efficiency / 100


            # Pass data to Output Screen
            result_screen = self.manager.get_screen("output")
            result_screen.ids.inverter_size.text = f"{inverter_size:.2f} W"
            result_screen.ids.battery_count.text = f"{battery_count}"
            result_screen.ids.panel_count.text = f"{panel_count}"
            result_screen.ids.charger_controller.text = f"{charger_rating:.2f} A"
            result_screen.ids.battery_setup.text = f"{battery_setup}"
            result_screen.ids.system_voltage.text = f"{system_voltage}V"
            result_screen.ids.total_energy_demand.text = f"{total_energy_demand:.2f} Wh"
            result_screen.ids.battery_bank_energy_capacity.text = f"{battery_bank_energy_capacity:.2f} Wh"
            result_screen.ids.daily_solar_energy_generation_needed.text = f"{daily_solar_energy_generation_needed:.2f} Wh/day"
            result_screen.ids.solar_panel_array_power.text = f"{solar_panel_array_power:.2f} W"
            result_screen.ids.expected_system_losses.text = f"{expected_system_losses:.2f} Wh"
            result_screen.ids.maximum_load_capacity.text = f"{maximum_load_capacity:.2f} W"

            # Hide loading indicator and show success message
            self.ids.loading_spinner.active = False
            show_popup("Success", "Calculations completed successfully!")

            self.manager.current = "output"
            self.clear_inputs()

        except ValueError as ve:
            self.ids.loading_spinner.active = False
            show_popup("Input Error", str(ve))
        except Exception as e:
            self.ids.loading_spinner.active = False
            show_popup("Error", f"Unexpected error: {e}")
            raise(e)


    def clear_inputs(self):
        fields = self.get_all_fields()
        for field in fields:
            field.text = ''
            # field.helper_text = ''
            field.error = False

    def reset_fields(self):
        self.ids.system_voltage.text = ''
        self.ids.system_voltage_text.text = 'Select System Voltage'

        self.ids.estimated_load.text = ''
        self.ids.backup_hours.text = ''
        self.ids.peak_sun_hours.text = ''
        self.ids.rating_of_panels.text = ''
        self.ids.panel_efficiency.text = ''
        self.ids.battery_amps.text = ''
        self.ids.inverter_efficiency.text = ''

        self.ids.battery_type.text = ''
        self.ids.battery_type_text.text = 'Select Battery Type'

        self.ids.system_voltage_text.text_color = (0,0,0,.71)
        self.ids.battery_type_text.text_color = (0,0,0,.71)

        self.ids.loading_spinner.active = False

    def get_all_fields(self):
        fields = [self.ids.system_voltage, self.ids.estimated_load, self.ids.backup_hours, self.ids.peak_sun_hours, self.ids.rating_of_panels,
                  self.ids.panel_efficiency, self.ids.battery_amps, self.ids.inverter_efficiency, self.ids.battery_type]
        return fields
    
    def auto_generate(self):
        # fields = self.get_all_fields()

        # for field in fields[:-1]:
        #     field.text = str()
        random_system_voltage = str(random.choice([12, 24, 48]))
        self.ids.system_voltage.text = random_system_voltage
        self.ids.system_voltage_text.text = random_system_voltage
        self.ids.system_voltage_text.text_color = (0,0,1,.41)
        self.ids.estimated_load.text = str(random.randint(1, 10000))
        self.ids.backup_hours.text = str(random.randint(1, 24))         
        self.ids.peak_sun_hours.text = str(random.randint(1, 24))
        self.ids.rating_of_panels.text = str(random.randint(1, 1000))
        self.ids.panel_efficiency.text = str(random.randint(1, 99))
        self.ids.battery_amps.text = str(random.randint(1, 1000))
        self.ids.inverter_efficiency.text = str(random.randint(1, 100))
        option_text = random.choice(["Dry Cell", "Wet Cell", "Lithium-ion"]) # ['Dry Cell', 'Wet Cell', 'Lithium-ion'][random.randint(0, 2)]
        self.ids.battery_type.text = option_text
        self.ids.battery_type_text.text = option_text
        self.ids.battery_type_text.text_color = (0,0,1,.41)
        self.ids.loading_spinner.active = False
        


















