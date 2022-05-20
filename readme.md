# Altana coding exercice 

## Requirements

* pandas~=1.4.2
* psutil~=5.9.0
* fastapi~=0.78.0
* SQLAlchemy~=1.4.36
* uvicorn==0.17.6

Ensure requirements are installed by runing the following commands. 

#### python -m pip install --upgrade pip
#### python -m pip install -r requirements.txt

## Project structure
### data
location for data files. contains a small.csv containing 11,3xx records from teh original file. 
### Database
folder containing the sqlite database wiht properly structure company_graph table. This can be recreated if required by runnign the create_db.py file.
### logs
fodler to hold log files for the importer and api

##### api.py
python code implementing a fastapi to query the sqlite database.

with the service running browse to http://127.0.0.1:8000
##### importer.py
python code to import delimited files to target tables in the sqlite database
##### create_db.py
python script to recreate the sqlite database

## Running the API and importer. 
### Api service 
python -m uvicorn api:app --reload
### importer 
python importer.py --filename {path to csv file} --target_table company_graph

Please note after the first log message the read of the file make take a minute or so (macbook pro 16")
the load to datastore following the importing xxxx rows using a chunk size xxxx takes 2-3 minutes on my machine. 

if the --target_table parameter is changed to any other target that table will be created in the database with all columns defined as text. All column names will be the column names in the header row of the import file.

If the --filename parameter is not of the same structure as ReceitaFederal_QuadroSocietario.csv the target table must be changed. The target table will be created correctly will all columns of type text. If the target  table is not changed the import will fail.

#### sample log. 

2022-05-20 08:58:11,432 - MainProcess - INFO - importer -starting import of file data/ReceitaFederal_QuadroSocietario.csv to company_graph

2022-05-20 08:59:05,008 - MainProcess - INFO - importer -read file data/ReceitaFederal_QuadroSocietario.csv

2022-05-20 08:59:05,028 - MainProcess - INFO - importer - deleting all records from company_graph if it exists

2022-05-20 08:59:05,133 - MainProcess - INFO - importer -importing 17780860 rows using a chunk size 6250

2022-05-20 09:01:45,997 - MainProcess - INFO - importer -file imported

## Architecture
### Design decisions
#### data store
I selected sqlite as a datastore as it is lightweight, readily available, requires no installation, and preformant for POCs in single user mode. 
#### import and persistence
I selected pandas because it is tried, tested,  and trusted for importing files is performant even for large files. 
#### command line paramters
Click was selected as it trivializes creating CLIs and provides defaults and error messages. 

In a real world instance I would likely leverage modin running on Ray to improve performance as it will scale per core on the the target and can also be sclae across devices using Ray's remote cpability. 

If the data store provided a bulk load capabiltiy e.g. sql server I would leverage that for the import instead of to_sql. 

Please note that the code does not leverage multi in to_sql as it is an order of magnitude slower for sqlite3 which implements its own multi code if a chunck size is passed.

As noted below in concerns the database table uses english column names. This is implemented by a trivial diationary of new column names. In the real world this would be handled via metadata.

As performance was not an issue I did not implement indexes on the reg_id or administration_name tables. This woudl have hampered import speed unless we drop and recreate the indexes.

### Concerns
The data was stated to be CSV but is in fact tab delimited. 

The column name in the instructions has a typo in the column name nr_cpf_cpnj_socio  the pn in nr_cpf_cpnj_socio are transposed.

The columns  nr_cnpj, nm_fantasia are not normalized. the name should be in a lookup table. 
The columns  cd_qualificacao_socio, ds_qualificacao_socio are not normalized. the description should be in a lookup table. 

The column names are not readily readble by non portuguese speakers. In the real world i would map the names to english via metadata.   

