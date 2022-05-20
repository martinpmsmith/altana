import logging
import sys

db_name = 'Database/testDB.db'

def init_logging(logfile_name: str = None):
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s - %(processName)s - %(levelname)s - %(name)s -%(message)s')
    fh = logging.FileHandler(logfile_name)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    logger.setLevel('INFO')
