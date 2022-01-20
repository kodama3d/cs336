9#   Name: Dustin Segawa
#   Assignment: CS336 Assignment #10
#   Created: 8/18/2020
#   Description: Award Table Python/SQL

import sqlite3

# attempts to open file, terminates with error if not found
# IN: file name for opening
# OUT: variable for opened file
# CALLS: none
def open_file(file):
    try:                                # tries to open file
        opfile = open(file, 'r')
        print('--', file, 'FILE FOUND --')
        return opfile
    except IOError:
        exit('-- ' + file + ' FILE NOT FOUND --')

# attempts to open connection to database
# IN: opened file variable
# OUT: connection to database
# CALLS: sqlite3 connection method
def db_connect(file):
    try:                                # tries to open connection to db file
        db_connection = sqlite3.connect(file)
        db_connection.row_factory = sqlite3.Row
        return db_connection
    except Error as err:
        exit(err)

# attempts to assign cursor to the database connection
# IN: opened database connection
# OUT: cursor to database
# CALLS: cursor method
def assign_cursor(db_connection):
    try:                                # tries to assign cursor to db
        c = db_connection.cursor()
        return c
    except Error as err:
        exit(err)

# deletes and creates the table, force updates the db
# IN: opened database connection, table sql commands, array data from file
# OUT: none
# CALLS: database execute and commit methods
def recreate_table(db_connection, del_table, add_table):
    db_connection.execute(del_table)    # deletes table if it exists
    db_connection.execute(add_table)    # adds blank formatted table
    db_connection.commit()              # force update database

# populates file data line by line into database
# IN: opened file variable, sql template, db connection and cursors
# OUT: none
# CALLS: sql execute and commit methods
def load_file_line_to_db(file, template, db_connection, cursor):
    for line in file:                           # loop through each line in file
        strip_line = line.rstrip('\n')          # strip off end of line marker
        split_line = strip_line.split(',')
        x = 0
        for i in split_line:
            split_line[x] = i.strip().strip('"').strip("'")     # strip all whitespace and quotes around strings
            x += 1
        cursor.execute(template, split_line)    # populates table
    db_connection.commit()                      # force update database

# this is not used due to assignment requirements
# populates file data into array for executemany command
# IN: opened file variable
# OUT: array of data from file
# CALLS: none
def load_file_to_array(file):
    array = []                                  # declare array
    for line in file:                           # loop through each line in file
        strip_line = line.rstrip('\n')          # strip off end of line marker
        split_line = strip_line.split(',')
        x = 0
        for i in split_line:
            split_line[x] = i.strip().strip('"').strip("'")       # strip all whitespace and quotes around strings
            x += 1
        array.append(split_line)     # split objects by comma
    return array

with db_connect("conference.sqlite") as db:     # connect to database
    # SQL command templates
    delete_nominee_table = '''DROP TABLE IF EXISTS nominees'''
    create_nominee_table = ''' CREATE TABLE IF NOT EXISTS nominees (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                nominee text,
                                description text,
                                img_name text,
                                current_votes integer);'''
    awards_template = '''INSERT INTO nominees (nominee,description,img_name,current_votes) VALUES (?, ?, ?, ?);'''

    curs = assign_cursor(db)                                        # assign cursor
    awards_file = open_file('awards.csv')                           # open data file
    recreate_table(db, delete_nominee_table, create_nominee_table)  # clear old table and recreate
    load_file_line_to_db(awards_file, awards_template, db, curs)    # load table from csv file
