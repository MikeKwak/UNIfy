# run "pip install pandas openpyxl"
# excel file should be explicitly saved on ur device 

import pandas as pd 
import sqlite3
import os


# replace this w the path of excel file saved on ur device
db = "/Users/chevinjeon/Downloads/UNIfy_Database_23_08_25.xlsx" 
xlsx = pd.ExcelFile(db, engine='openpyxl')

conn = sqlite3.connect("Unify.db") # name modifiable 

for sheet in xlsx.sheet_names:
    df = pd.read_excel(xlsx, sheet_name = sheet, engine='openpyxl')
    df.to_sql(sheet, conn, if_exists='replace', index = False)
    print(f"Loaded sheet '{sheet}' into table '{sheet}'")

dfs = {}
for sheet in xlsx.sheet_names:
    dfs[sheet] = pd.read_sql_query(f"SELECT * FROM '{sheet}'", conn)

conn.close()

print(dfs['student info'])


# save as Excel
dfs['student info'].to_excel('student_info.xlsx', index=False)
print(os.path.abspath("Unify.db"))

