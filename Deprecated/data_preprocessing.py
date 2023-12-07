import sqlite3
import csv
import pandas as pd
from sklearn.impute import KNNImputer
import time

start_time = time.time()

# Function to create the database and import data from CSV
def create_database(csv_file : str, db_file : str, columns : list):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create a table in the database
    cursor.execute("DROP TABLE IF EXISTS speed_dating")
    create_table_query = f"CREATE TABLE IF NOT EXISTS speed_dating ({', '.join(columns)})"
    cursor.execute(create_table_query)

    # Read the CSV file and insert data into the table
    with open(csv_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            values = [row[column] if row[column] != "" else None for column in columns]
            placeholders = ', '.join(['?'] * len(columns))
            insert_query = f"INSERT INTO speed_dating ({', '.join(columns)}) VALUES ({placeholders})"
            cursor.execute(insert_query, values)

    # Commit the changes
    conn.commit()

    # Close the database connection
    conn.close()

# Function to delete rows with 3 or more NULL values in a particular set of columns
def delete_rows_with_null_values(db_file : str):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Define the attribute columns
    attribute_columns_o = ['attr_o', 'sinc_o', 'intel_o', 'fun_o', 'amb_o']
    attribute_columns_3_1 = ['attr3_1', 'sinc3_1', 'intel3_1', 'fun3_1', 'amb3_1']

    # Construct the conditions for NULL values in _o columns
    conditions_o = []
    for column in attribute_columns_o:
        conditions_o.append(f"({column} IS NULL)")

    # Construct the conditions for NULL values in 3_1 columns
    conditions_3_1 = []
    for column in attribute_columns_3_1:
        conditions_3_1.append(f"({column} IS NULL)")

    # For new attributes, use the same code as above and define the attributes in a list.
    # For loop can be used to append to base names (attr, sinc, intel, fun, amb) but these shortened
    # words are inconsistentin the database
    
    # Combine the conditions for _o columns using AND
    condition_query_o = f"({' + '.join(conditions_o)}) >= 3"

    # Combine the conditions for 3_1 columns using AND
    condition_query_3_1 = f"({' + '.join(conditions_3_1)}) >= 3"

    # Construct the delete query
    delete_query = f"DELETE FROM speed_dating WHERE ({condition_query_o}) OR ({condition_query_3_1})"

    # Execute the query to find rows to be deleted
    cursor.execute(delete_query)

    # Get the count of deleted rows
    deleted_rows = cursor.rowcount

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    # Print the number of rows deleted
    print(f"Deleted {deleted_rows} rows.")



# Deletes rows that are missing their corresponding (iid, pid), (pid, iid) pair
def delete_rows_with_missing_pairs(db_file : str):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Delete rows with missing pairs
    delete_query = '''
        DELETE FROM speed_dating
        WHERE NOT EXISTS (
            SELECT 1
            FROM speed_dating AS s2
            WHERE speed_dating.iid = s2.pid AND speed_dating.pid = s2.iid
        )
    '''

    # Execute the delete query
    cursor.execute(delete_query)

    # Get the count of deleted rows with missing pairs
    deleted_missing_pairs = cursor.rowcount

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    # Print the number of rows with missing pairs deleted
    print(f"Deleted {deleted_missing_pairs} rows with missing pairs.")

# Function to perform data imputation on remaining NULL values
def perform_data_imputation(db_file : str):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query('SELECT * FROM speed_dating', conn)
    conn.close()

    # Select only the columns ending in "_o". Change this to suit other attributes
    cols_to_impute = [col for col in df.columns if col.endswith('_o')]

    # Convert the selected columns to numeric
    df[cols_to_impute] = df[cols_to_impute].apply(pd.to_numeric, errors='coerce')

    # Perform KNN imputation
    knn_imputer = KNNImputer()
    df_imputed = pd.DataFrame(knn_imputer.fit_transform(df[cols_to_impute]), columns=cols_to_impute)

    # Update the original DataFrame with the imputed values
    df[cols_to_impute] = df_imputed

    # Save the updated data back to the database
    conn = sqlite3.connect('speed_dating.db')
    df.to_sql('speed_dating', conn, if_exists='replace', index=False)
    print('Remaining NULL values have had data imputation performed on them.')
    conn.close()

# Columns to be included in the database table
columns = ['iid', 'gender', 'pid', 'match', 'dec_o', 'attr_o', 'sinc_o', 'intel_o', 'fun_o',
           'amb_o', 'attr3_1', 'sinc3_1', 'fun3_1', 'intel3_1', 'amb3_1']

# Call the functions

create_database('Speed Dating Data.csv', 'speed_dating.db', columns)
delete_rows_with_null_values('speed_dating.db')
delete_rows_with_missing_pairs('speed_dating.db')
perform_data_imputation('speed_dating.db')
print(f'Operations complete. It took {round(time.time() - start_time, 4)} seconds.')
