import sqlalchemy
from sqlalchemy import create_engine, text, MetaData, Table, Column, String
import os
import pandas as pd
import csv

engine = sqlalchemy.create_engine('postgresql://fungsvluvpkkpb:01814245f16ffe16b65c49bfb4660e612c0e1445e8c12072ac6733da5369dc39@ec2-34-236-103-63.compute-1.amazonaws.com:5432/dfb9b40ghfgdkq')
csv_file_path='/Volumes/Untitled/Data-20231026T061813Z-001/Data/parts_hmda_2017_nationwide_all-records_labels/part_3_of_3_hmda_2017_nationwide_all-records_labels.csv'
csv_file_path2='/Volumes/Untitled/Data-20231026T061813Z-001/Data/parts_hmda_2017_nationwide_all-records_labels/part_1_of_3_hmda_2017_nationwide_all-records_labels.csv'
table_name = 'table1'

metadata = MetaData()

# Reflect the current state of the database
metadata.reflect(bind=engine)
# Check if table exists
if table_name not in metadata.tables:
    # 1. Read the first row of the CSV to get the column names
    with open(csv_file_path2, 'r') as file:
        csv_reader = csv.reader(file)
        column_names = next(csv_reader)

    # 2. Create a table in PostgreSQL based on those column names
    columns = [Column(name, String) for name in column_names]
    table = Table(table_name, metadata, *columns)
    metadata.create_all(engine, [table])

# Load the data from the CSV into the PostgreSQL table
def load_data_from_csv_to_db(file_path):
    with engine.connect() as connection:
        # Use the raw connection to execute the COPY command
        raw_connection = connection.connection
        cursor = raw_connection.cursor()

        with open(file_path, 'r') as file:
            cursor.copy_expert(f"COPY {table_name} FROM STDIN WITH CSV HEADER", file)
            raw_connection.commit()

# 3. Load the data using the COPY command
load_data_from_csv_to_db(csv_file_path)
