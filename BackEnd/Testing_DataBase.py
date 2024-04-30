import unittest
import DataBase_Manager
import os

class Test_DataBase(unittest.TestCase):

    # Users and Login:
    def test_new_user(self):
        # Adding user
        a = DataBase_Manager.Add_User('Marco', '12345')
        self.assertEqual(a, True)
        # Adding user again
        b = DataBase_Manager.Add_User('Marco', '54321')
        self.assertEqual(b, False)

    def test_right_login(self):
        a = DataBase_Manager.Validate_Login('Marco', '12345')
        self.assertEqual(a, True)

    def test_wrong_login(self):
        a = DataBase_Manager.Validate_Login('Marco', 'asdqwe')
        self.assertEqual(a, False)

    def test_wrong_user(self):
        a = DataBase_Manager.Validate_Login('Marco4', 'asdqwe')
        self.assertEqual(a, False)


    # Items:
    def test_add_items(self):
        a = DataBase_Manager.Add_Item('Blue Pen', 'Normal Blue Pen')
        b = DataBase_Manager.Add_Item('Red Pen', 'Normal Red Pen')
        self.assertEqual(a, True)
        self.assertEqual(b, True)


    # Storage:
    def test_add_storage(self):
        a = DataBase_Manager.Add_Storage('Warehouse', 'Main Warehouse')
        b = DataBase_Manager.Add_Storage('Box 1', 'Work place 1')
        self.assertEqual(a, True)
        self.assertEqual(b, True)



if __name__ == '__main__':
    unittest.main()