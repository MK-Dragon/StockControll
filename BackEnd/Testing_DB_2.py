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
    def test_A_query_stock(self):
        report.info(f'\t---')
        report.info(f'Query Stock:')
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


if __name__ == '__main__':
    unittest.main()