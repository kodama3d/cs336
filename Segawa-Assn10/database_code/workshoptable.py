#   Name: Dustin Segawa
#   Assignment: CS336 Assignment #10
#   Created: 8/18/2020
#   Description: Workshops Table Python/SQL

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

# populates file data into array of dictionaries
# IN: opened file variable
# OUT: array of dictionaries from file
# CALLS: none
def load_file_to_dict(file):
    dict = []                                   # declare array
    for line in file:                           # loop through each line in file
        strip_line = line.rstrip('\n')          # strip off end of line marker
        lineList = strip_line.split(sep=',')    # split lines by comma
        newDict = {
            'title': lineList[0].strip(),
            'session_num': lineList[1].strip(),
            'room_num': lineList[2].strip(),
            'start_time': lineList[3].strip(),
            'stop_time': lineList[4].strip()}
        dict.append(newDict)                    # append each line in dictionary
    return dict

# populates database table line by line from array of dictionaries
# IN: opened file variable, sql template, db connection and cursors
# OUT: none
# CALLS: sql execute and commit methods
def load_array_to_db(array, template, db_connection, cursor):
    for i in array:
        cursor.execute(template, list(i.values()))  # populates sql table per dictionary line
        # cursor.execute(template, i.data_array())    # populates sql table per class in array
    db_connection.commit()                          # force update database

with db_connect("conference.sqlite") as db:     # connect to database
    # SQL command templates
    delete_workshops_table = '''DROP TABLE IF EXISTS workshops'''
    create_workshops_table = ''' CREATE TABLE IF NOT EXISTS workshops (
                                id integer PRIMARY KEY AUTOINCREMENT,
                                title text,
                                session_num integer,
                                room_num text,
                                start_time time,
                                end_time time);'''
    workshops_template = '''INSERT INTO workshops (
                            title,session_num,room_num,start_time,end_time) VALUES (?, ?, ?, ?, ?);'''

    curs = assign_cursor(db)                                            # assign cursor
    workshops_file = open_file('workshops.csv')                         # open data file
    recreate_table(db, delete_workshops_table, create_workshops_table)  # clear old table and recreate
    workshops_arr = load_file_to_dict(workshops_file)                   # loads data into array if dictionaries
    load_array_to_db(workshops_arr, workshops_template, db, curs)       # loads array into sql table



