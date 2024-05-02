import unittest
import DataBase_Manager
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Debug DB Read/Write/Delete
report = setup_logger('Test log', 'logs/test_report.log')
report.info('---//---')


class Test_DataBase(unittest.TestCase):
    # Create DataBase and Tables
    def test_A_create_db(self):
        '''Test if All Tables are created'''
        created, total_tried = DataBase_Manager.CreateDB()

        message = f'Create DB: [{created}/{total_tried}]'
        if created == total_tried:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(created, total_tried)

    # Users and Login:
    def test_B_new_user(self):
        '''Teste adding user 2x'''
        # Adding user
        a = DataBase_Manager.Add_User('Marco', '12345')
        message = f'Adding user 1st time [{a}] (expect True)'
        if a == True:
            report.info(message)
        else:
            report.error(message)

        # Adding user again
        b = DataBase_Manager.Add_User('Marco', '54321')
        message = f'Adding user 2nd time [{b}] (expect False)'
        if b == False:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(a, True)
        self.assertEqual(b, False)

    def test_C_login(self):
        a = DataBase_Manager.Validate_Login('Marco', '12345')
        b = DataBase_Manager.Validate_Login('Marco', 'asdqwe')
        c = DataBase_Manager.Validate_Login('mARCO', '12345')

        message = f'Login: Correct User + Password [{a}] (expected True)'
        if a == True:
            report.info(message)
        else:
            report.error(message)

        message = f'Login: Correct User + Wrong Password [{b}] (expected False)'
        if b == False:
            report.info(message)
        else:
            report.error(message)

        message = f'Login: Wrong User + Password [{c}] (expected False)'
        if c == False:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(a, True)
        self.assertEqual(b, False)
        self.assertEqual(c, False)


    # Workers:
    def test_B_new_worker(self):
        '''Teste adding user 2x'''
        # Adding user
        a = DataBase_Manager.Add_Worker('Zé Maria', '12345')
        message = f'Adding worker name and number [{a}] (expect True)'
        if a == True:
            report.info(message)
        else:
            report.error(message)

        b = DataBase_Manager.Add_Worker('Manuel Silva')
        message = f'Adding worker name and NO number [{b}] (expect True)'
        if b == True:
            report.info(message)
        else:
            report.error(message)

        c = DataBase_Manager.Add_Worker('Marco', '12345')
        message = f'Adding worker number already exists [{c}] (expect False)'
        if c == False:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(a, True)
        self.assertEqual(b, True)
        self.assertEqual(c, False)


    # Items:
    def test_B_add_items(self):
        a = DataBase_Manager.Add_Item('Blue Pen', 'Normal Blue Pen')
        b = DataBase_Manager.Add_Item('Red Pen', 'Normal Red Pen')
        c = DataBase_Manager.Add_Item('Blue Pen', '2nd Blue Pen')

        message = f'Item Add [{a}] (expected True)'
        if a == True:
            report.info(message)
        else:
            report.error(message)

        message = f'Item Add [{b}] (expected True)'
        if b == True:
            report.info(message)
        else:
            report.error(message)

        message = f'Item Add Again [{c}] (expected False)'
        if c == False:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(a, True)
        self.assertEqual(b, True)
        self.assertEqual(c, False)


    # Storage:
    def test_B_add_storage(self):
        a = DataBase_Manager.Add_Storage('Warehouse', 'Main Warehouse')
        b = DataBase_Manager.Add_Storage('Box 1', 'Work place 1')
        c = DataBase_Manager.Add_Storage('Box 1', 'Work place 1')

        message = f'Storage Added [{a}] (expected True)'
        if a == True:
            report.info(message)
        else:
            report.error(message)

        message = f'Storage Added [{b}] (expected True)'
        if b == True:
            report.info(message)
        else:
            report.error(message)

        message = f'Storage Added Again [{c}] (expected False)'
        if c == False:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(a, True)
        self.assertEqual(b, True)
        self.assertEqual(c, False)



    # Delivering item:
    def test_C_add_entry(self):
        pass


    # Storage
    def test_C_read_storage(self):
        item = 3
        storage = 2
        a = DataBase_Manager.Get_Stock_Data(item, storage)
        report.info(f'it[{item}] st[{storage}] = {a}')

        item = 3
        storage = 7
        b = DataBase_Manager.Get_Stock_Data(item, storage)
        report.info(f'it[{item}] st[{storage}] = {b}')

        self.assertEqual(len(a) <= 1, True)
        self.assertEqual(len(b) == 0, True)

    def test_D_update_stocks(self):
        DataBase_Manager.Update_Stock(item_id=1, storage_id=2, units=-1)

    def test_C_first_stockup(self):
        DataBase_Manager.First_Stock(1, 1, 150, 50, 250)
        a = DataBase_Manager.First_Stock(1, 1, 150, 50, 250)

        message = f'First Stock up [{a}] (expected False)'
        if a == False:
            report.info(message)
        else:
            report.error(message)

        self.assertEqual(a, False)




if __name__ == '__main__':
    unittest.main()