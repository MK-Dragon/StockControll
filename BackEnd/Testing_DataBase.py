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




if __name__ == '__main__':
    unittest.main()