import os
import pandas as pd
import sqlalchemy
from sqlalchemy import inspect
import chardet

engine = sqlalchemy.create_engine('postgresql://fungsvluvpkkpb:01814245f16ffe16b65c49bfb4660e612c0e1445e8c12072ac6733da5369dc39@ec2-34-236-103-63.compute-1.amazonaws.com:5432/dfb9b40ghfgdkq')


folder_path = r'/Volumes/Untitled/Data/'  # replace with your folder path

# Use os.walk() to generate all file paths in the folder and subfolders
all_files = [os.path.join(root, name) for root, dirs, files in os.walk(folder_path) for name in files]

# Filter for only CSV files
data_files = [file for file in all_files if file.endswith(('.csv', '.xls'))]

# Get a list of all existing tables
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

def read_file_with_detected_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']
    
    try:
        if file_path.endswith('.csv'):
            return pd.read_csv(file_path, encoding=encoding)
        elif file_path.endswith('.xls'):
            return pd.read_excel(file_path, engine='xlrd')
    except pd.errors.ParserError:
        print(f"Skipped lines or found issues in file: {file_path}")
        return None

# Loop through each file and upload it to the database
for data_file in data_files:
    table_name = os.path.splitext(os.path.basename(data_file))[0]

    # Ensure table names are unique
    counter = 1
    original_table_name = table_name
    while table_name in existing_tables:
        table_name = original_table_name + "_" + str(counter)
        counter += 1

    df = read_file_with_detected_encoding(data_file)
    if df is None:
        continue

    # Convert columns with multiple datatypes to string
    for column in df.columns:
        if not all(isinstance(val, (type(df[column].iloc[0]), float, int)) for val in df[column]):
            df[column] = df[column].astype(str)

    # Upload the DataFrame to the PostgreSQL database
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    existing_tables.append(table_name)

print(f"Imported {len(data_files)} data files to the database.")
