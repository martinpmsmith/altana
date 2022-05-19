tabu# bhf-edaf-core Will be the central location for any core functionality necessary to power data movement technology
within BHF

- Constants
- Utilities
- Loggers
- Event Maps

### How do I integrate with a local package on my machine?
Example: Your are adding features to bhf_edaf_core and want to integrate the changes with a consumer application.

Run `pip install -e <path/to/local/repo>`
This will build the specific repo and reference the egg

To create a symlink, make sure _**wheel**_ is installed and then re-run the pip install

# Requirements


# Project Structure

### Core files
Should be in the corresponding folder named after the project

### Tests
All test cases are written for pytest and should belong in the **tests** directory

### Examples
Any example scripts should be in the **examples** directory


### Concerns
The data was stated to be CSV but is in fact tab delimited. 

the column name in the instructions has a typo in the column name nr_cpf_cpnj_socio  the pn in nr_cpf_cpnj_socio are transposed.

the columns  cd_qualificacao_socio, ds_qualificacao_socio are not normalized. the description should be in a lookup table. 

the column names are not readily readble by non portuguese speakers. In the real world i would map the names to english via metadata. here i simply created a view.  

the column business_partner_role_code is 