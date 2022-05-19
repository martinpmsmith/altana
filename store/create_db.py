import sqlite3
from os import path


def create_db():
    dbname = 'Database/testDB.db'
    if not path.exists(dbname):
        with sqlite3.connect('Database/testDB.db') as conn:
            cursor = conn.cursor()

            # Drop the GEEK table if already exists.
            cursor.execute("DROP TABLE IF EXISTS ")

            # Creating table
            table = """ 
create table company_graph
(
    reg_id                     varchar(255),
    name                       varchar(255),
    state                      varchar(25),
    company_or_business        numeric,
    partner_reg_id             varchar(25),
    business_partner_role_code numeric,
    business_partner_role_desc varchar(25),
    administration_name        varchar(25)
);             
             """

            cursor.execute(table)
