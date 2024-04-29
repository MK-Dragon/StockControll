# Base Kivy Imports:
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from kivy.core.window import Window # Remove before py --> apk

# Base KivyMD Imports:
from kivymd.app import MDApp
from kivy.uix.popup import Popup


class LoginScreen(Screen):
    pass

class MainScreen(Screen):
    pass


class Main(MDApp):
    def __init__(self, **kwargs):
        self.title = "D&D Time!"
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

        return self.screen_manager


if __name__ == '__main__':
    Window.size = (405, 700)  # Remove before py --> apk
    main_app = Main()
    main_app.run()