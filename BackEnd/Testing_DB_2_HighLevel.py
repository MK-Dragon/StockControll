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
report = setup_logger('Test log 2', 'logs/test_report_2.log')
report.info('---//---')

class Test_DataBase_2(unittest.TestCase):
    def test_READ_ALL_TABLES(self):
        DataBase_Manager.Read_Full_Table('utilizadores')
        DataBase_Manager.Read_Full_Table('colaboradores')
        DataBase_Manager.Read_Full_Table('armarios')
        DataBase_Manager.Read_Full_Table('items')
        DataBase_Manager.Read_Full_Table('entrega')
        DataBase_Manager.Read_Full_Table('stock')
        self.assertEqual(True, True)


    def test_A_get_stock(self):
        report.info(f'\t---')
        report.info(f'Get Stock:')
        item = 1
        storage = 1
        report.info(f'\tItem [{item}] Storage [{storage}]:')
        a = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=storage)
        for entry in a:
            report.info(f'\t\t> {entry}')

        item = 1
        report.info(f'\tItem [{item}] Only:')
        b = DataBase_Manager.Get_Stock_Data(item_id=item)
        for entry in b:
            report.info(f'\t\t> {entry}')

        storage = 1
        report.info(f'\tStorage [{storage}] Only:')
        c = DataBase_Manager.Get_Stock_Data(storage_id=storage)
        for entry in c:
            report.info(f'\t\t> {entry}')

        self.assertEqual(len(a) == 1, True)
        self.assertEqual(len(b) > 1, True)
        self.assertEqual(len(c) > 1, True)

    def test_A_deliver_item_to_worker(self):
        report.info(f'\t---')
        report.info(f'Deliver Item to Worker:')

        a = DataBase_Manager.Deliver_Item(item_id=1, storage_id=2, num=-1, worker_id=1, user_id=1)
        self.assertEqual(a, True)
        #TODO: add more testes...

    # ReStock Testing
    def test_Aa_reStock_from_store(self):
        report.info(f'\t---')
        report.info(f'ReStock Store -> Storage:')

        # test Restock from STORE aka: source = None
        user = 1
        rs_storage = 2
        item = 1
        units = 3
        # get initial values
        ini_stock = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=rs_storage)
        ini_stock = ini_stock[0][2]
        # test:
        a = DataBase_Manager.ReStock(storage_restocked_id=rs_storage, item_id=item, units=units, user=user)
        report.info(f'\tFrom Store -> Storage [{rs_storage}] -> item[{item}] (+{units})')
        # get final values
        final_stock = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=rs_storage)
        final_stock = final_stock[0][2]
        # Log:
        if ini_stock + units == final_stock:
            report.info(f'\tini [{ini_stock}] + [{units}] == final [{final_stock}]')
        else:
            report.error(f'\tini [{ini_stock}] + [{units}] != final [{final_stock}]')

        self.assertEqual(a, True)
        self.assertEqual(ini_stock + units, final_stock)

    def test_Ab_reStock_transfer(self):
        report.info(f'\t---')
        report.info(f'ReStock S1 -> S2:')

        # test Restock from Storage
        user = 2
        rs_storage = 2
        souce_storage = 1
        item = 3
        units = 10
        # get initial values
        ini_stock_rs = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=rs_storage)
        ini_stock_rs = ini_stock_rs[0][2]
        ini_stock_source = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=souce_storage)
        ini_stock_source = ini_stock_source[0][2]

        # test:
        a = DataBase_Manager.ReStock(storage_source_id=souce_storage, storage_restocked_id=rs_storage, item_id=item, units=units, user=user)
        report.info(f'\tFrom Storage [{souce_storage}] -> Storage [{rs_storage}] -> item[{item}] ({units})')

        # get final values
        final_stock_rs = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=rs_storage)
        final_stock_rs = final_stock_rs[0][2]
        final_stock_source = DataBase_Manager.Get_Stock_Data(item_id=item, storage_id=souce_storage)
        final_stock_source = final_stock_source[0][2]

        # Log:
        if ini_stock_rs + units == final_stock_rs:
            report.info(f'\tini [{ini_stock_rs}] + [{units}] == final [{final_stock_rs}]')
        else:
            report.error(f'\tini [{ini_stock_rs}] + [{units}] != final [{final_stock_rs}]')

        if ini_stock_source - units == final_stock_source:
            report.info(f'\tini [{ini_stock_source}] - [{units}] == final [{final_stock_source}]')
        else:
            report.error(f'\tini [{ini_stock_source}] - [{units}] != final [{final_stock_source}]')

        self.assertEqual(a, True)
        self.assertEqual(ini_stock_rs + units, final_stock_rs)
        self.assertEqual(ini_stock_source - units, final_stock_source)

    def test_Ac_reStock_erro(self):
        # test error... out of bounds and all...
        #TODO test ReStock Erros!
        pass

    # Complex Table Reads
    def test_A_Complex_Read_get_defaults(self):
        report.info(f'\t---')
        report.info(f'Complex_Read: get_defaults:')

        # test a:

        number_of_results_a = 2
        data = DataBase_Manager.Complex_Read_Table(
            table='entrega',
            num_results=number_of_results_a,
        )

        a_len = len(data)
        if a_len <= number_of_results_a:
            report.info(f'{a_len} <= {number_of_results_a} = {a_len <= number_of_results_a}')
        else:
            report.error(f'{a_len} <= {number_of_results_a} = {a_len <= number_of_results_a}')

        for i in data:
            report.info(f'\t{i}')

        # Test b:

        report.info(f'num_results = Zero for retrieve ALL data:')

        data = DataBase_Manager.Complex_Read_Table(
            table='entrega',
            num_results=0,
        )

        b_len = len(data)
        if b_len >= number_of_results_a:
            report.info(f'{b_len} >= {a_len} = {b_len >= a_len}')
        else:
            report.error(f'{b_len} >= {a_len} = {b_len >= a_len}')

        for i in data:
            report.info(f'\t{i}')


        self.assertEqual(a_len <= number_of_results_a, True)
        self.assertEqual(b_len >= a_len, True)





if __name__ == '__main__':
    unittest.main()