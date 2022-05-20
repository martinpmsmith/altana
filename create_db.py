import sqlite3

from common import db_name


def create_db():
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Creating table
        table = """ 
    create table if not exists company_graph
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


if __name__ == '__main__':
    create_db()
