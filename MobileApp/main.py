# Base Kivy Imports:
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.core.window import Window # Remove before py --> apk

# Base KivyMD Imports:
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivy.uix.popup import Popup

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

    def item_clicked(self, instance):
        id = instance.id
        debug_MobileApp.info(f'id[{id}]')
        print(f"id[{id}]")
        response = requests.get('http://127.0.0.1:5000/item/info', json={'id': id})
        print(response)
        for i in response.json():
            print(f'\t{i}')


#TODO: Note: for the 'search' list[tuples] -> list[dict] like {'blue pen': 1} Use dict.keys -> list[keys] and use 'FuzzyWuzzy' ^_^

class Main(MDApp):
    def __init__(self, **kwargs):
        self.title = "D&D Time!"
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

        return self.screen_manager


if __name__ == '__main__':
    Window.size = (405, 700)  #TODO: Remove before py --> apk / it bugs the mobile App...
    main_app = Main()
    main_app.run()