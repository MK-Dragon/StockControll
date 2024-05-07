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
from kivymd.uix.relativelayout import MDRelativeLayout


import requests
import logging


# Data Holder:
db_data: dict = {}



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
    user_field = ObjectProperty(None)
    pw_field = ObjectProperty(None)

    def button_login(self):
        debug_MobileApp.info(f'Login:')
        # Get user and password
        user = self.user_field.text
        print(f'user: {user}')
        password = self.pw_field.text
        print(f'pw: {password}')

        # try connection
        try:
            login_info = {
                'user': user,
                'password': password
            }

            response = requests.get('http://127.0.0.1:5000/login', json=login_info)
            debug_MobileApp.info(f'\t{response = }')
            for i in response.json():
                debug_MobileApp.info(f'\t\t{i}')

            # TODO: Encrypt and Decrypt JSON String

            db_data = response.json()[0]

            if db_data['login'] == True:
                # reset login screen
                self.pw_field.text = ''

                main_app.screen_manager.transition.direction = 'up'
                main_app.screen_manager.current = 'Main Screen'
            elif db_data['login'] == False:
                print("... Wrong shit!")
                open_popup(
                    title="Failed Login",
                    icon='wifi-off',
                    text_1="Wrong Username or Password",
                    text_2='If you forgot your login info,',
                    text_3='Please Contact the Admin'
                )
            else:
                debug_MobileApp.error(f'\tFailed to Login...')

        except Exception as err:
            debug_MobileApp.error(f'No Connection: {err}')
            open_popup(
                title="Failed to Connect:",
                icon='wifi-off',
                text_1="No Connection!",
                text_2='Check Internet Connection',
                text_3='Or Try Again Later'
            )
        # if login ok: go to main screen



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
            open_popup(
                title="Failed to Connect:",
                icon='wifi-off',
                text_1="No Connection!",
                text_2='Check Internet Connection',
                text_3='Or Try Again Later'
            )


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

    def button_go_to_login_screen(self):
        main_app.screen_manager.transition.direction = 'down'
        main_app.screen_manager.current = 'Login Screen'


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



# Helper Funtions:
def open_popup(title:str, text_1:str, text_2:str='', text_3:str='', icon:str='alert'):
    '''
    Opens a confirmation PopUp with:

    :param title:
    :param text_1:
    :param text_2:
    :param text_3:
    :param icon:
    :return:
    '''
    items = []
    items.append(
        ThreeLineAvatarListItem(
            IconLeftWidget(
                icon=icon
            ),
            text=text_1,
            secondary_text=text_2,
            tertiary_text=text_3
        ),
    )

    # Popup:
    dialog = MDDialog(
        title=title,
        type="confirmation",
        items=items,
        content_cls=PopupError(),
        buttons=[
            MDFlatButton(
                text="OK",
                theme_text_color="Custom",
                text_color=main_app.theme_cls.primary_color,
                on_release=lambda x: dialog.dismiss()
            ),
        ],
    )
    dialog.open()


# Custom widgets:
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

        self.login_screen = LoginScreen()
        screen = Screen(name='Login Screen')
        screen.add_widget(self.login_screen)
        self.screen_manager.add_widget(screen)

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