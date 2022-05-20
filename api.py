import logging
import os
import sqlite3
import threading
import time

import psutil as psutil
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from common import db_name, init_logging

app = FastAPI()

logger = logging.getLogger('api')


def self_terminate():
    time.sleep(1)
    psutil.Process()
    parent = psutil.Process(psutil.Process(os.getpid()).ppid())
    parent.kill()


def run_query(query: str):
    with sqlite3.connect(db_name) as conn:
        data = []
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        # if we have rows then extract column names and zip with data rows
        if len(result) > 0:
            column_names = [x[0] for x in cursor.description]
            data = [dict(zip(column_names, row)) for row in result]
        return data


@app.on_event("startup")
async def startup_event():
    init_logging('logs/api.log')




@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
<table class="table-striped">
 <tr><td>/company_graph</td><td>returns the first 10 records from company_graph</td><td><a href="/company_graph">/company_graph</a></td></tr>
 <tr><td>/operators_for_company/{reg_id}  </td><td>returns operators for company identified by {reg_id}</td><td><a href="/operators_for_company/00124695000113">/operators_for_company/00124695000113</a></td></tr>
 <tr><td>/companies_for_operator/{name} </td><td>returns companies for operator {name}</td><td><a href="/companies_for_operator/ABEL DIAS">/companies_for_operator/ABEL DIAS</a></td></tr>
 <tr><td>/related_companies/{reg_id}</td><td>companies connected to a given company {reg_id} via shared operators</td><td><a href="/related_companies/16865452000176">/related_companies/16865452000176</a></td></tr>
 <tr><td>/kill</td><td>kill the uvicorn service</td><td><a href="/kill">/kill</a></td></tr>
</table>
        </body>
    </html>    
    """


@app.get("/company_graph")
async def company_graph():
    logger.info('running company graph query')
    return run_query('select * from company_graph limit 10')


@app.get("/operators_for_company/{name}")
async def operators_for_company(name: str):
    logger.info(f'running operators_for_company query with {name}')
    return run_query(f"select administration_name from company_graph where reg_id = '{name}'")


@app.get("/companies_for_operator/{name}")
async def companies_for_operator(name: str):
    logger.info(f'running companies_for_operator query with {name}')
    return run_query(f"select reg_id from company_graph where administration_name = '{name}'")


@app.get("/related_companies/{name}")
async def related_companies(name: str):
    logger.info(f'running related_companies query with {name}')
    return run_query(f"""
select distinct reg_id, name from company_graph
where administration_name in ( select administration_name
                               from company_graph where reg_id = '{name}')
and reg_id != '{name}'    
    """)


@app.get("/kill")
async def kill():
    threading.Thread(target=self_terminate, daemon=True).start()
    return {"success": True}
