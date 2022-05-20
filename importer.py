import logging
import sqlite3
from math import floor

import click
import pandas as pd
from sqlalchemy import create_engine

from common import db_name, init_logging

logger = logging.getLogger('importer')



class Importer():
    column_names_for_table = {
        'company_graph': ['reg_id', 'name', 'state', 'company_or_business', 'partner_reg_id',
                          'business_partner_role_code',
                          'business_partner_role_desc', 'administration_name']
    }

    def __init__(self, target_table: str):
        self.target_table = target_table
        self.db_name = db_name

    def clean_table(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{self.target_table}'")
            if cursor.fetchone()[0]==1 :
                logger.info(f' deleting all records from {self.target_table} if it exists ')
                cursor.execute(f'delete from {self.target_table}')

    def import_file(self, filename: str = 'data/ReceitaFederal_QuadroSocietario.csv', delim: str = '\t'):
        logger.info(f'starting import of file {filename} to {self.target_table}')
        df = pd.read_csv(filename, delimiter=delim, dtype=str)
        logger.info(f'read file {filename} ')
        # rename the column names to english so they match the DB description
        # if they exist in the map in the real world this would be in metadata
        if self.target_table in self.column_names_for_table.keys():
            df.set_axis(self.column_names_for_table[self.target_table], axis=1, inplace=True)
        self.clean_table()
        engine = create_engine(f'sqlite:///{self.db_name}')
        # calculate chunk size based on # columns in DF dont use multi for sqlite as it is an order of magnitude slower.
        chunksize = floor(50000 / len(df.columns))
        logger.info(f'importing {df.shape[0]} rows using a chunk size {chunksize}')
        df.to_sql(name=self.target_table, con=engine, if_exists='append', index=False, chunksize=chunksize)
        logger.info(f'file imported ')


@click.command()
@click.option('--filename', default='data/ReceitaFederal_QuadroSocietario.csv', help='file to import')
@click.option('--target_table', default='company_graph', help='eventmap filename.')
def main(filename: str, target_table:str):
    Importer(target_table=target_table).import_file(filename=filename)


if __name__ == '__main__':
    init_logging('logs/importer.log')
    main()