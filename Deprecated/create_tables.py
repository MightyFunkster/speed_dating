import sqlite3
import time

start_time = time.time()

def create_tables(cursor):
    
    # Drop the participants table if it exists
    cursor.execute("DROP TABLE IF EXISTS participants")

    # Create the participants table
    create_participants_table_query = '''
        CREATE TABLE participants (
            iid SMALLINT UNSIGNED PRIMARY KEY,
            gender TINYINT
        )
    '''

    # Execute the query to create the participants table
    cursor.execute(create_participants_table_query)

    # Create indexes on iid column in the participants table
    cursor.execute('CREATE INDEX idx_participants_iid ON participants (iid)')

    # Insert data into the participants table
    insert_participants_data_query = '''
        INSERT INTO participants (iid, gender)
        SELECT DISTINCT iid, gender
        FROM speed_dating;
    '''

    # Execute the query to insert data into the participants table
    cursor.execute(insert_participants_data_query)



    # Drop the dates table if it exists
    cursor.execute("DROP TABLE IF EXISTS dates")

    # Create the dates table
    create_dates_table_query = '''
        CREATE TABLE dates (
            date_id INTEGER PRIMARY KEY AUTOINCREMENT,
            iid SMALLINT UNSIGNED,
            pid SMALLINT UNSIGNED,
            match TINYINT,
            dec_o TINYINT,
            FOREIGN KEY (iid) REFERENCES participants (iid),
            FOREIGN KEY (pid) REFERENCES participants (iid)
        )
    '''

    # Execute the query to create the dates table
    cursor.execute(create_dates_table_query)

    # Create indexes on date_id column in the dates table
    cursor.execute('CREATE INDEX idx_dates_date_id ON dates (date_id)')

    # Insert data from "speed_dating" table into "dates" table
    insert_dates_data_query = '''
        INSERT INTO dates (iid, pid, match, dec_o)
        SELECT iid, pid, match, dec_o
        FROM speed_dating
    '''

    # Execute the query to insert data into the dates table
    cursor.execute(insert_dates_data_query)



    # Drop the attributes table if it exists
    cursor.execute("DROP TABLE IF EXISTS attributes")

    # Create the attributes table
    cursor.execute("CREATE TABLE attributes (attr_id TINYINT UNSIGNED PRIMARY KEY, attribute_name TEXT)")

    # Create indexes on attr_id column in the attributes table
    cursor.execute('CREATE INDEX idx_attributes_attr_id ON attributes (attr_id)')

    # Attribute names
    attribute_columns = ['attr', 'sinc', 'intel', 'fun', 'amb']

    # Insert attribute names into the attributes table
    for index, column in enumerate(attribute_columns, start = 1):
        cursor.execute("INSERT INTO attributes (attr_id, attribute_name) VALUES (?, ?)", (index, column))



    # Drop the ratings table if it exists
    cursor.execute("DROP TABLE IF EXISTS ratings")

    # Create the ratings table
    create_ratings_table_query = '''
        CREATE TABLE ratings (
            rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_id INTEGER UNSIGNED,
            attr_id TINYINT UNSIGNED,
            rating_value TINYINT UNSIGNED,
            FOREIGN KEY (date_id) REFERENCES dates (date_id),
            FOREIGN KEY (attr_id) REFERENCES attributes (attr_id)
        )
    '''

    # Execute the query to create the ratings table
    cursor.execute(create_ratings_table_query)

    # Create indexes on date_id and attr_id columns in the ratings table
    cursor.execute('CREATE INDEX idx_ratings_date_id ON ratings (date_id)')
    cursor.execute('CREATE INDEX idx_ratings_attr_id ON ratings (attr_id)')

    # Insert data into the ratings table for each column
    for column_name in attribute_columns:
        column_name = column_name + '_o'
        # Insert data into the ratings table using a single query
        insert_data_query = '''
            INSERT INTO ratings (date_id, attr_id, rating_value)
            SELECT d.date_id, a.attr_id, s.{}
            FROM dates AS d
            JOIN speed_dating AS s ON d.iid = s.iid AND d.pid = s.pid
            JOIN attributes AS a ON a.attribute_name || '_o' = lower(?)
        '''.format(column_name)

        # Execute the query to insert data into the ratings table
        cursor.execute(insert_data_query, (column_name.lower(),))



    # Drop the self_ratings table if it exists
    cursor.execute("DROP TABLE IF EXISTS self_ratings")

    # Create the self_ratings table
    create_self_ratings_table_query = '''
        CREATE TABLE self_ratings (
            self_rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
            iid SMALLINT UNSIGNED,
            attr_id TINYINT UNSIGNED,
            self_rating_value TINYINT UNSIGNED,
            FOREIGN KEY (iid) REFERENCES participants(iid),
            FOREIGN KEY (attr_id) REFERENCES attributes(attr_id)
        )
    '''

    # Execute the query to create the self_ratings table
    cursor.execute(create_self_ratings_table_query)

    # Create indexes on date_id columns in the dates table
    cursor.execute('CREATE INDEX idx_self_ratings_iid ON self_ratings (iid)')
    cursor.execute('CREATE INDEX idx_self_ratings_attr_id ON self_ratings (attr_id)')

    # Insert data into the ratings table for each column
    for column_name in attribute_columns:
        column_name = column_name + '3_1'
        # Insert data into the ratings table using a single query
        insert_data_query = '''
            INSERT INTO self_ratings (iid, attr_id, self_rating_value)
            SELECT p.iid, a.attr_id, s.{}
            FROM participants AS p
            JOIN speed_dating AS s ON p.iid = s.iid
            JOIN attributes AS a ON a.attribute_name || '3_1' = lower(?)
        '''.format(column_name)

        # Execute the query to insert data into the ratings table
        cursor.execute(insert_data_query, (column_name.lower(),))


# Execute the function
conn = sqlite3.connect('speed_dating.db')
cursor = conn.cursor()

create_tables(cursor)

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print(f"Participants, Dates, Attributes, Ratings and Self_Ratings tables created successfully. It took {round(time.time() - start_time, 4)} seconds.")
