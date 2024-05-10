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


import DEncrypt
import requests
import logging


# Data Holder:
class DataBase_Data:
    db_data: dict = {}
    popup_data = None

    def load_popup_data(self, data):
        self.popup_data = data
DATA = DataBase_Data()



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
        password = self.pw_field.text

        # try connection
        try:
            login_info = {
                'user': user,
                'password': password
            }

            # Encrypt data
            login_info = DEncrypt.encrypt_to_json(login_info)

            response = requests.get(
                'http://127.0.0.1:5000/login',
                json=login_info
            )

            # Decrypt the response
            db_data = response.json()
            db_data = DEncrypt.decrypt_from_json(db_data)

            if db_data['login'] == True:
                # reset login screen
                self.pw_field.text = ''
                # Save data for later
                DATA.db_data = db_data

                # Go to Main Screen
                main_app.screen_manager.transition.direction = 'up'
                main_app.screen_manager.current = 'Main Screen'

            elif db_data['login'] == False:
                # TODO: Add limit to wrong password
                open_popup(
                    title="Failed Login",
                    icon='account',
                    text_1="Wrong Username or Password",
                    text_2='If you forgot your login info,',
                    text_3='Please Contact the Admin'
                )
            else:
                debug_MobileApp.error(f'\tFailed to Login...') # ¨\_(^-^)_/¨

        except Exception as err:
            debug_MobileApp.error(f'No Connection: {err}')
            open_popup(
                title="Failed to Connect:",
                icon='wifi-off',
                text_1="No Connection!",
                text_2='Check Internet Connection',
                text_3='Or Try Again Later'
            )



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
    label_storage = StringProperty('')
    label_item = StringProperty('')
    num_items = 0
    label_num_items = StringProperty('')
    label_worker = StringProperty('')

    dialog = None

    entry_data:dict = {}

    def on_kv_post(self, base_widget):
        self.reset_fields()
        self.display_fields()


    def reset_fields(self):
        self.label_worker = 'Click to Select'
        self.label_storage = 'Click to Select'
        self.label_item = 'Click to Select'
        self.num_items = 1
        self.label_num_items = str(self.num_items)

        self.entry_data = {
            'worker': None,
            'storage': None,
            'item': None
        }

    def display_fields(self):
        # Clear
        self.ids.container2.clear_widgets(children=None)

        #Display all input fields:
        self.ids.container2.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='account-arrow-down'
                ),
                text='Worker',
                secondary_text=self.label_worker,
                id='Worker',
                on_release=self.select_item
            )
        )
        self.ids.container2.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='locker'
                ),
                text='Storage',
                secondary_text=self.label_storage,
                id='Storage',
                on_release=self.select_item
            )
        )
        self.ids.container2.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='pen'
                ),
                text='Item',
                secondary_text=self.label_item,
                id='Items',
                on_release=self.select_item
            )
        )

    def select_item(self, instance):
        # Get Index of Server Clicked:
        field = instance.id
        print(f'select_item {field}]')
        DATA.popup_data = field.lower()

        # debug
        '''DATA.db_data = {
            'login': True,
            'user_id': 1,
            'worker': [['1', '354', 'zé'], ['2', '454', 'rita']],
            'storage': [['1', 'whouse', 'hee'], ['2', 'box1', 'asd']],
            'items': [('1', 'blue pen', 'Algo'), ('2', 'red pen', 'algo')]
        }'''


        items = [] # append items ^_^

        for entry in DATA.db_data[field.lower()]:
            items.append(
                TwoLineAvatarIconListItem(
                    IconLeftWidget(
                        icon='duck'
                        #theme_icon_color="Custom",
                        #icon_color=color
                    ),
                    IconRightWidget(
                        icon='duck'
                        #id=f"{server['Index']}",
                        #on_release=self.delete_button
                    ),
                    text=f"{entry[1]}",
                    secondary_text=f'{entry[2]}',
                    id=f"{entry[0]}",
                    on_release=self.item_clicked
                )
            )

        # Popup list:
        self.dialog = MDDialog(
            title=field,
            type="confirmation",
            items=items,
            buttons=[
                MDFlatButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    #text_color=self.theme_cls.primary_color,
                    id='cancel',
                    on_release=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def item_clicked(self, instance):
        # save data
        id = instance.id
        self.entry_data[DATA.popup_data] = id

        # update label
        if DATA.popup_data == 'worker':
            print('worker')
            for i in DATA.db_data[DATA.popup_data]:
                if i[0] == id:
                    print('\tid')
                    self.label_worker = i[2]
                    print(f'\t\t{self.label_worker}')

        elif DATA.popup_data == 'storage':
            for i in DATA.db_data[DATA.popup_data]:
                if i[0] == id:
                    self.label_storage = i[1]
                    print(f'\t\t{self.label_storage}')

        elif DATA.popup_data == 'items':
            for i in DATA.db_data[DATA.popup_data]:
                if i[0] == id:
                    self.label_item = i[1]
                    print(f'\t\t{self.label_item}')

        print(f'{self.entry_data = }')

        # desmiss popup:
        self.dialog.dismiss()
        # refresh fields!
        self.display_fields()

    def button_cancel(self):
        # Reset all
        self.reset_fields()
        # Go back to main screen
        main_app.screen_manager.transition.direction = 'right'
        main_app.screen_manager.current = 'Main Screen'

    def button_submit(self):
        try:
            # Get data:
            data_package = {
                'user_id': DATA.db_data['user_id'],
                'worker_id': self.entry_data['worker'],
                'item_id': self.entry_data['items'],
                'num': self.num_items,
                'storage_id': self.entry_data['storage']
            }

            #TODO: add check for 'Click to Select'... popup error blank field...

            # Encrypt and Send data
            data_package = DEncrypt.encrypt_to_json(data_package)
            response = requests.post(
                'http://127.0.0.1:5000/items',
                json=data_package
            )

            # decrypt response
            db_data = response.json()
            db_data = DEncrypt.decrypt_from_json(db_data)

            # TODO: Review the popup... needs work
            if db_data['status'] == 'True':
                print('All good ^_^')
                open_popup(
                    title="Operation Status:",
                    icon='emoticon-happy',
                    text_1="Item Delivered!",
                    text_2='Items left: [{?}]',
                    text_3=''
                )
            elif db_data['status'] == 'False':
                print('Operation Failed!')
                open_popup(
                    title="Operation Status:",
                    icon='emoticon-sad',
                    text_1="An Error Has Occurred!",
                    text_2='Item Was NOT Delivered!',
                    text_3='Try again later...'
                )
            else:
                print("Error... Opps..")
                open_popup(
                    title="Operation Status:",
                    icon='robot-confused',
                    text_1="An Error Has Occurred!",
                    text_2='data error...',
                    text_3='Try again later...'
                )

            # Ask: new entry?? yes -> Stay / no -> back to main screen
            if DATA.popup_data == 'yes':
                print('Popup YES!!!')
            elif DATA.popup_data == 'no':
                    print('Popup NO!!!')
                    # Go back to main screen
                    main_app.screen_manager.transition.direction = 'right'
                    main_app.screen_manager.current = 'Main Screen'
            # reset popup data...
            DATA.popup_data = None

        except Exception as err:
            debug_MobileApp.error(f'Error Delivering item: {err}')
            open_popup(
                title="Failed to Connect:",
                icon='emoticon-sad',
                text_1="ErrorDelivering item!",
                text_2='Check Internet Connection',
                text_3='Or Try Again Later'
            )

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



        self.main_screen = DeliverItem()
        screen = Screen(name='Deliver Item')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)

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
    Window.size = (405, 700)  #TODO: Remove before py --> apk / it bugs the mobile App...
    main_app = Main()
    main_app.run()