# Base Kivy Imports:
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.core.window import Window # Remove before py --> apk
# Base KivyMD Imports:
from kivymd.app import MDApp

# Dynamic UI:
# Layout:
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
# Buttons & Labels:
from kivymd.uix.list import TwoLineAvatarIconListItem, OneLineAvatarIconListItem, ThreeLineAvatarListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.list import IconLeftWidget, IconRightWidget
# Other Parts:
from kivymd.uix.list import IRightBodyTouch
from kivy.uix.popup import Popup
from kivymd.uix.dialog import MDDialog


import requests
import logging


def setup_logger(name, log_file, level=logging.INFO): #TODO: change INFO to ERROR before py -> APK
    """To setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Debug DB Read/Write/Delete
debug_MobileApp = setup_logger('mobile app', 'logs/app.log')
debug_MobileApp.info('---//---')




class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    container = ObjectProperty(None)
    def button(self):
        print("Duck Test")
        try:
            response = requests.get('http://127.0.0.1:5000/items')
            print(response)
            for i in response.json():
                print(f'\t{i}')
                self.ids.container.add_widget(
                    TwoLineAvatarIconListItem(
                        text=f'{i[1]}',
                        secondary_text=f'{i[2]}',
                        id=f'{i[0]}',
                        on_release=self.item_clicked
                    )
                )
        except Exception as err:
            debug_MobileApp.error(f'No Connection: {err}')
            print("No Connection!! ^_^")

            items = []
            items.append(
                ThreeLineAvatarListItem(
                    IconLeftWidget(
                        icon='wifi-off'
                    ),
                    text="No Connection!",
                    secondary_text='Check Internet Connection',
                    tertiary_text='Or Try Again Later'
                ),
            )

            # Popup:
            self.dialog = MDDialog(
                title="Failed to Connect:",
                type="confirmation",
                items=items,
                content_cls=PopupError(),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=main_app.theme_cls.primary_color,
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                ],
            )
            self.dialog.open()

    def item_clicked(self, instance):
        id = instance.id
        debug_MobileApp.info(f'id[{id}]')
        print(f"id[{id}]")
        response = requests.get('http://127.0.0.1:5000/item/info', json={'id': id})
        print(response)
        for i in response.json():
            print(f'\t{i}')

    def button_go_to_add_entry(self):
        main_app.screen_manager.transition.direction = 'left'
        main_app.screen_manager.current = 'Deliver Item'


class DeliverItem(Screen):
    # ids:
    '''storage_picked = ObjectProperty(None)
    item_picked = ObjectProperty(None)
    num_items  = ObjectProperty(None)'''

    label_storage = StringProperty('')
    label_item = StringProperty('')
    num_items = 0
    label_num_items = StringProperty('')
    label_worker = StringProperty('')

    def on_kv_post(self, *args):
        self.reset_fields()

    def reset_fields(self):
        self.label_storage = 'Click to Pick'
        self.label_item = 'Click to Pick'
        self.num_items = 1
        self.label_num_items = str(self.num_items)
        self.label_worker = 'Click to Pick'


    def button_cancel(self):
        # Reset all
        self.reset_fields()
        # Go back to main screen
        main_app.screen_manager.transition.direction = 'right'
        main_app.screen_manager.current = 'Main Screen'

    def button_submit(self):
        # Send data

        # Go back to main screen
        main_app.screen_manager.transition.direction = 'right'
        main_app.screen_manager.current = 'Main Screen'

    def button_plus(self):
        print("plus")
        self.num_items += 1
        self.label_num_items = str(self.num_items)
        print(f'{self.label_num_items = }')

    def button_minus(self):
        print("minus")
        self.num_items -= 1
        self.label_num_items = str(self.num_items)
        print(f'{self.label_num_items = }')

#TODO: Note: for the 'search' list[tuples] -> list[dict] like {'blue pen': 1} Use dict.keys -> list[keys] and use 'FuzzyWuzzy' ^_^



# Custom wedgets:
class YourContainer(IRightBodyTouch, MDBoxLayout):
    # use for TwoLineAvatarIconListItem: with 2 left items
    adaptive_width = True

class PopupError(BoxLayout):
    pass




class Main(MDApp):
    def __init__(self, **kwargs):
        self.title = "Stock Control"
        super().__init__(**kwargs)

    def build(self):
        # Theme and Colors:

        # Screen Management:
        self.screen_manager = ScreenManager()

        '''self.login_screen = LoginScreen()
        screen = Screen(name='Login Screen')
        screen.add_widget(self.login_screen)
        self.screen_manager.add_widget(screen)'''

        self.main_screen = MainScreen()
        screen = Screen(name='Main Screen')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        self.main_screen = DeliverItem()
        screen = Screen(name='Deliver Item')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

        return self.screen_manager


if __name__ == '__main__':
    Window.size = (405, 700)  #TODO: Remove before py --> apk / it bugs the mobile App...
    main_app = Main()
    main_app.run()