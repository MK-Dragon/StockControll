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
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout


import DEncrypt
import requests
import logging


# Data Holder:
class DataBase_Data:
    db_data: dict = None
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
    container_notifications = ObjectProperty(None)
    container_storage = ObjectProperty(None)
    container_restock_entries = ObjectProperty(None)
    container_delivery_entries = ObjectProperty(None)

    sort_stock_by = 'item' # or 'storage'

    def on_kv_post(self, base_widget):
        print('\n * on_kv_post * \n')
        # Get data from server
        self.get_data_from_server()

        # Load/display containers
        self.display_all()


# TODO: Add Notifications for low stock + "shopping list"


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



    # Geting and Displaying data:
    def get_data_from_server(self):
        print("Getting data:")
        debug_MobileApp.info('Gating data from Server')
        try:
            response = requests.get('http://127.0.0.1:5000/reload')
            data = response.json()
            data = DEncrypt.decrypt_from_json(data)
            print(f'from server: {data}')
            print(f'{data = }')
            if DATA.db_data == None:
                print('\tif')
                # Debug mode only
                DATA.db_data = data
                DATA.db_data.update({'user_id': '1'})
                print('')
            else:
                print('\telse')
                # Normal mode:
                DATA.db_data['worker'] = data['worker']
                DATA.db_data['storage'] = data['storage']
                DATA.db_data['items'] = data['items']
                DATA.db_data['stock'] = data['stock']
                DATA.db_data['restock'] = data['restock']
                DATA.db_data['delivered'] = data['delivered']
            debug_MobileApp.info('\t\tall good')
        except Exception as err:
            print("\texcept")
            debug_MobileApp.error(f'Error Re/Loading Data from Server: {err}')

    def display_all(self):
        debug_MobileApp.info('\tLoading/Displaying All Containers:')
        self.display_low_stock()
        self.display_stock()
        self.display_restock_entries()
        self.display_delivery_entries()

    def display_low_stock(self):
        # TODO: ... coming soon... ish.......
        pass

    def display_stock(self):
        # TODO:... ui/ux on the way...
        # Clear container
        self.ids.container_storage.clear_widgets(children=None)

        debug_MobileApp.info('\t\tDisplaying: Stock')
        for entry in DATA.db_data['stock']:
            print(f'\t{entry = }')
            item = ''
            storage = ''

            num = entry[2]
            min = entry[3]
            max = entry[4]

            # Get Storage data:
            for i in DATA.db_data['storage']:
                # getting storage
                if entry[1] == i[0]:
                    storage = i[1]
                    print(f'\t\t{storage = }')

            # Get item info:
            for i in DATA.db_data['items']:
                if entry[0] == i[0]:
                    item = i[1]
                    print(f'\t\t{item = }')
                    break

            # Display it!
            self.ids.container_storage.add_widget(
                ThreeLineAvatarListItem(
                    IconLeftWidget(
                        icon='pen'
                    ),
                    text=f'{item}',
                    secondary_text=f'{storage}',
                    tertiary_text=f'min [{min}] / Max [{max}]',
                    id=f'{entry[0]}'
                    #on_release=self.item_clicked # TODO: Entries are read only (??)
                )
            )

    def display_restock_entries(self):
        # Clear container
        self.ids.container_restock_entries.clear_widgets(children=None)

        debug_MobileApp.info('\t\tDisplaying: ReStock')
        print('\n\nDisplay ReStock:')
        print(f'{DATA.db_data['restock'] = }\n'
              f'{type(DATA.db_data['restock']) = }')
        for entry in DATA.db_data['restock']:
            print(f'\t{entry = }')
            user = ''
            source = ''
            restocked = ''
            item = ''
            num = entry[6]
            date = entry[2]

            # Get user data: # TODO do Special read for users with only usernames! NO PASSWORDS!!!
            """for i in DATA.db_data['user']:
                user = '(?)'
                break"""
            user = '(?)'

            # Get Storage data:
            for i in DATA.db_data['storage']:
                # getting source
                if entry[3] == i[0]:
                    source = i[1]
                    print(f'\t\t{source = }')
                # getting restocked
                if entry[4] == i[0]:
                    restocked = i[1]
                    print(f'\t\t{restocked = }')
            if source == '':
                source = '* Store'
                print(f'\t\t{source = }')

            # Get item info:
            for i in DATA.db_data['items']:
                if entry[5] == i[0]:
                    item = i[1]
                    print(f'\t\t{item = }')
                    break

            # Display it!
            self.ids.container_restock_entries.add_widget(
                ThreeLineAvatarListItem(
                    IconLeftWidget(
                        icon='cube-send'
                    ),
                    text=f'[{num}x] {item}',
                    secondary_text=f'{user}: {source} -> {restocked}',
                    tertiary_text=f'{date}',
                    id=f'{entry[0]}'
                    #on_release=self.item_clicked # TODO: Entries are read only (??)
                )
            )

    def display_delivery_entries(self):
        # Clear container
        self.ids.container_delivery_entries.clear_widgets(children=None)

        debug_MobileApp.info('\t\tDisplaying: Delivered')
        print('\n\nDisplay Delivered:')
        print(f'{DATA.db_data['delivered'] = }\n'
              f'{type(DATA.db_data['delivered']) = }')
        for entry in DATA.db_data['delivered']:
            print(f'\t{entry = }')
            user = ''
            storage = ''
            worker = ''
            item = ''
            num = entry[5]
            date = entry[1]

            # Get user data: # TODO do Special read for users with only usernames! NO PASSWORDS!!!
            """for i in DATA.db_data['user']:
                user = '(?)'
                break"""
            user = '(?)'

            # Get Storage data:
            for i in DATA.db_data['storage']:
                # getting storage
                if entry[6] == i[0]:
                    storage = i[1]
                    print(f'\t\t{storage = }')
                    break
            if storage == '':
                storage = '* Store'
                print(f'\t\t{storage = }')

            # Get Worker:
            for i in DATA.db_data['worker']:
                # getting worker
                if entry[3] == i[0]:
                    worker = i[1]
                    print(f'\t\t{worker = }')
                    break

            # Get item info:
            for i in DATA.db_data['items']:
                if entry[4] == i[0]:
                    item = i[1]
                    print(f'\t\t{item = }')
                    break

            # Display it!
            self.ids.container_delivery_entries.add_widget(
                ThreeLineAvatarListItem(
                    IconLeftWidget(
                        icon='pen'
                    ),
                    text=f'[{num}x] {item}',
                    secondary_text=f'{user}: {storage} -> {worker}',
                    tertiary_text=f'{date}',
                    id=f'{entry[0]}'
                    # on_release=self.item_clicked # TODO: Entries are read only (??)
                )
            )


    def button_reload(self):
        self.get_data_from_server()
        self.display_all()



    # Navigation:
    def button_go_to_add_entry(self):
        main_app.screen_manager.transition.direction = 'left'
        main_app.screen_manager.current = 'Deliver Item'

    def button_go_to_login_screen(self):
        main_app.screen_manager.transition.direction = 'down'
        main_app.screen_manager.current = 'Login Screen'

    def button_go_to_restock(self):
        main_app.screen_manager.transition.direction = 'left'
        main_app.screen_manager.current = 'ReStock Item'



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

        print(f'\n\nitem_clicked: {id = }')

        print(f'\t{DATA.popup_data = }')
        print(f'\t{DATA.db_data[DATA.popup_data] = }')

        # update label
        if DATA.popup_data == 'worker':
            for i in DATA.db_data[DATA.popup_data]:
                if str(i[0]) == id:
                    self.label_worker = i[1]
                    break

        elif DATA.popup_data == 'storage':
            for i in DATA.db_data[DATA.popup_data]:
                if str(i[0]) == id:
                    self.label_storage = i[1]
                    break

        elif DATA.popup_data == 'items':
            print(f'for loop:')
            for i in DATA.db_data[DATA.popup_data]:
                if str(i[0]) == id:
                    self.label_item = i[1]
                    break

        print(f'\n{self.entry_data = }')

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
                'http://127.0.0.1:5000/deliveritem',
                json=data_package
            )

            # decrypt response
            db_data = response.json()
            db_data = DEncrypt.decrypt_from_json(db_data)

            # TODO: Review the popup... needs work
            if db_data['status'] == 'True':

                # Popup list:
                self.dialog = MDDialog(
                    title='Operation Status:',
                    type="confirmation",
                    items=[
                        TwoLineAvatarIconListItem(
                            IconLeftWidget(
                                icon='emoticon-happy'
                                # theme_icon_color="Custom",
                                # icon_color=color
                            ),
                            IconRightWidget(
                                icon='pen'
                                # id=f"{server['Index']}",
                                # on_release=self.delete_button
                            ),
                            text=f"Item Delivered!",
                            secondary_text=f'Deliver other item?',
                            # id=f"{entry[0]}",
                            on_release=self.item_clicked
                        )
                    ],
                    buttons=[
                        MDFlatButton(
                            text="Done",
                            theme_text_color="Custom",
                            # text_color=self.theme_cls.primary_color,
                            id='done',
                            on_release=lambda x: self.button_yes_no('done')
                        ),
                        MDFlatButton(
                            text="New",
                            theme_text_color="Custom",
                            # text_color=self.theme_cls.primary_color,
                            id='new',
                            on_release=lambda x: self.button_yes_no('new')
                        )
                    ]
                )
                self.dialog.open()

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

        except Exception as err:
            debug_MobileApp.error(f'Error Delivering item: {err}')
            open_popup(
                title="Failed to Connect:",
                icon='emoticon-sad',
                text_1="ErrorDelivering item!",
                text_2='Check Internet Connection',
                text_3='Or Try Again Later'
            )

    def button_yes_no(self, val:str):
        if val == 'new':
            self.reset_fields()
            self.dialog.dismiss()
            self.display_fields()
        elif val == 'done':
            self.reset_fields()
            self.dialog.dismiss()
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


class ReStock(Screen):
    label_storage_to_restock = StringProperty('')
    label_storage_source = StringProperty('')
    label_item = StringProperty('')
    number_of_items = ObjectProperty(None)

    dialog = None

    entry_data: dict = {}
    entry_key = ''
    data_key = ''

    def on_kv_post(self, base_widget):
        self.reset_fields()
        self.display_fields()


    def reset_fields(self):
        # TODO: reset doesn't clean the fields... love bugs... -.-
        self.label_worker = 'Click to Select'

        self.label_item = 'Click to Select'

        self.label_storage_to_restock = 'Click to Select'
        self.label_storage_source = 'Click to Select'
        self.number_of_items.text = '1'

        self.entry_data = {
            'StorageS': None,
            'StorageR': None,
            'Items': None
        }
        self.entry_key = ''
        self.data_key = ''

    def button_cancel(self):
        # Reset all
        self.reset_fields()
        # Go back to main screen
        main_app.screen_manager.transition.direction = 'right'
        main_app.screen_manager.current = 'Main Screen'

    def display_fields(self):
        # Clear
        self.ids.container2.clear_widgets(children=None)

        #Display all input fields:
        self.ids.container2.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='cube-send' # 'export'
                ),
                text='Storage Source',
                secondary_text=self.label_storage_to_restock,
                id='StorageS',
                on_release=self.select_item
            )
        )
        self.ids.container2.add_widget(
            TwoLineAvatarIconListItem(
                IconLeftWidget(
                    icon='locker' # 'import'
                ),
                text='Storage to Restock',
                secondary_text=self.label_storage_source,
                id='StorageR',
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

        # set entry key:
        self.entry_key = field

        # set DATA.db_data key:
        if field == 'StorageS' or field == 'StorageR':
            self.data_key = 'storage'

        else:
            self.data_key = 'items'

        DATA.popup_data = field#.lower()

        items = [] # append items ^_^

        for entry in DATA.db_data[self.data_key]:
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
        self.entry_data[self.entry_key] = id

        print(f'\n\nitem_clicked: {id = }')

        print(f'\t{self.data_key = }')
        print(f'\t{DATA.db_data[self.data_key] = }')

        # update label
        if self.entry_key == 'StorageS':
            for i in DATA.db_data['storage']:
                if str(i[0]) == id:
                    self.label_storage_to_restock = i[1]
                    break

        elif self.entry_key == 'StorageR':
            for i in DATA.db_data['storage']:
                if str(i[0]) == id:
                    self.label_storage_source = i[1]
                    break

        elif self.data_key == 'items':
            print(f'for loop:')
            for i in DATA.db_data[self.data_key]:
                if str(i[0]) == id:
                    self.label_item = i[1]
                    break

        print(f'\n{self.entry_data = }')

        # desmiss popup:
        self.dialog.dismiss()
        # refresh fields!
        self.display_fields()

    def button_submit(self):
        debug_MobileApp.info('Submit ReStock:')
        num = self.number_of_items.text
        debug_MobileApp.info(f'\t{self.entry_data = } [x{num}]')

        # TODO: Data Validation for Storage.

        try:
            # if it can NOT be an INT... it's an ERROR! ^_^
            num = int(num)

        except Exception as err:
            debug_MobileApp.error(f'\tNumber of Items, is NOT a Number!')
            open_popup(
                title="Input Error!",
                icon='emoticon-sad',
                text_1="Number of Items",
                text_2='Must be a Number!',
                text_3='From 1 to 9999'
            )
            return

        try:
            # Get data:
            data_package = {
                'user_id': DATA.db_data['user_id'],
                'storage_source': self.entry_data['StorageS'],
                'storage_restock': self.entry_data['StorageR'],
                'item_id': self.entry_data['Items'],
                'num': int(self.number_of_items.text),
            }

            # TODO: add check for 'Click to Select'... popup error blank field...

            # Encrypt and Send data
            data_package = DEncrypt.encrypt_to_json(data_package)
            response = requests.post(
                'http://127.0.0.1:5000/restock',
                json=data_package
            )

            # decrypt response
            db_data = response.json()
            db_data = DEncrypt.decrypt_from_json(db_data)

            # TODO: Review the popup... needs work
            if db_data['status'] == 'True':

                # Popup list:
                self.dialog = MDDialog(
                    title='Operation Status:',
                    type="confirmation",
                    items=[
                        TwoLineAvatarIconListItem(
                            IconLeftWidget(
                                icon='emoticon-happy'
                                # theme_icon_color="Custom",
                                # icon_color=color
                            ),
                            IconRightWidget(
                                icon='pen'
                                # id=f"{server['Index']}",
                                # on_release=self.delete_button
                            ),
                            text=f"Storage Restocked!",
                            secondary_text=f'Stock Other Item?',
                            # id=f"{entry[0]}",
                            on_release=self.item_clicked
                        )
                    ],
                    buttons=[
                        MDFlatButton(
                            text="Done",
                            theme_text_color="Custom",
                            # text_color=self.theme_cls.primary_color,
                            id='done',
                            on_release=lambda x: self.button_yes_no('done')
                        ),
                        MDFlatButton(
                            text="New",
                            theme_text_color="Custom",
                            # text_color=self.theme_cls.primary_color,
                            id='new',
                            on_release=lambda x: self.button_yes_no('new')
                        )
                    ]
                )
                self.dialog.open()
                debug_MobileApp.info('\tAll good')

            elif db_data['status'] == 'False':
                print(f'\tOperation Failed! {db_data['status'] = }')
                debug_MobileApp.error('\tOperation Failed!')
                open_popup(
                    title="Operation Status:",
                    icon='emoticon-sad',
                    text_1="An Error Has Occurred!",
                    text_2='Storage NOT Restocked!',
                    text_3='Try again later...'
                )
            else:
                print("Error... Opps..")
                debug_MobileApp.error('\tOperation Failed! data error...')
                open_popup(
                    title="Operation Status:",
                    icon='robot-confused',
                    text_1="An Error Has Occurred!",
                    text_2='data error...',
                    text_3='Try again later...'
                )

        except Exception as err:
            debug_MobileApp.error(f'\tError Restocking Storage: {err}')
            open_popup(
                title="Failed to Connect:",
                icon='emoticon-sad',
                text_1="ErrorRestocking item!",
                text_2='Check Internet Connection',
                text_3='Or Try Again Later'
            )

    def button_yes_no(self, val:str):
        if val == 'new':
            self.reset_fields()
            self.dialog.dismiss()
            self.display_fields()
        elif val == 'done':
            self.reset_fields()
            self.dialog.dismiss()
            main_app.screen_manager.transition.direction = 'right'
            main_app.screen_manager.current = 'Main Screen'

    def button_plus(self):
        a = self.number_of_items.text
        try:
            a = int(a)
            a += 1
            self.number_of_items.text = str(a)
        except:
            #a = a + ' Numbers Only'
            self.number_of_items.text = '1'

    def button_minus(self):
        a = self.number_of_items.text
        try:
            a = int(a)
            a -= 1
            self.number_of_items.text = str(a)
        except:
            #a = str(a) + ' Numbers Only'
            self.number_of_items.text = '1'


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

class DiceCard(MDCard):
    text = ObjectProperty(None)
    dice_icon = ObjectProperty(None)
    card_id = ObjectProperty(None)



class Main(MDApp):
    def __init__(self, **kwargs):
        self.title = "Stock Control"
        super().__init__(**kwargs)

    def build(self):
        # Theme and Colors:

        # Screen Management:
        self.screen_manager = ScreenManager()


        self.main_screen = MainScreen()
        screen = Screen(name='Main Screen')
        screen.add_widget(self.main_screen)
        self.screen_manager.add_widget(screen)


        self.login_screen = LoginScreen()
        screen = Screen(name='Login Screen')
        screen.add_widget(self.login_screen)
        self.screen_manager.add_widget(screen)

        # Adding Entries:
        self.deliver_item_screen = DeliverItem()
        screen = Screen(name='Deliver Item')
        screen.add_widget(self.deliver_item_screen)
        self.screen_manager.add_widget(screen)

        self.restock_screen = ReStock()
        screen = Screen(name='ReStock Item')
        screen.add_widget(self.restock_screen)
        self.screen_manager.add_widget(screen)



        return self.screen_manager


if __name__ == '__main__':
    Window.size = (405, 700)  #TODO: Remove before py --> apk / it bugs the mobile App...
    main_app = Main()
    main_app.run()