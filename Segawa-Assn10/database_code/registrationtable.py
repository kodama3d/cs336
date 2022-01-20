#   Name: Dustin Segawa
#   Assignment: CS336 Assignment #10
#   Created: 8/18/2020
#   Description: Registration Table Python/SQL

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
    except Exception as err:
        exit(err)

# attempts to assign cursor to the database connection
# IN: opened database connection
# OUT: cursor to database
# CALLS: cursor method
def assign_cursor(db_connection):
    try:                                # tries to assign cursor to db
        c = db_connection.cursor()
        return c
    except Exception as err:
        exit(err)

# deletes and creates the table, force updates the db
# IN: opened database connection, table sql commands, array data from file
# OUT: none
# CALLS: database execute and commit methods
def recreate_table(db_connection, del_table, add_table):
    db_connection.execute(del_table)    # deletes table if it exists
    db_connection.execute(add_table)    # adds blank formatted table
    db_connection.commit()              # force update database

# loads registration data from open file into array of classes
# IN: registration file name
# OUT: array of classes
# CALLS: none
def load_registration(file):
    Registrant_data = []
    for line in file:                           # loop through each line in file
        lineList = line.strip().split(sep=',')  # split lines by comma
        newClass = Registrant(lineList)
        Registrant_data.append(newClass)        # append each line in dictionary
    return Registrant_data

# populates database table line by line from array of classes
# IN: opened file variable, sql template, db connection and cursors
# OUT: none
# CALLS: sql execute and commit methods
def load_array_to_db(array, template, db_connection, cursor):
    for i in array:
        # cursor.execute(template, list(i.values()))  # populates sql table per dictionary line
        cursor.execute(template, i.data_array())    # populates sql table per class in array
    db_connection.commit()                          # force update database

class Registrant:
    def __init__(self, arr):  # initiates data class fields from an array
        self.date_of_registration = arr[0]
        self.title = arr[1]
        self.firstname = arr[2]
        self.lastname = arr[3]
        self.address1 = arr[4]
        self.address2 = arr[5]
        self.city = arr[6]
        self.state = arr[7]
        self.zipcode = arr[8]
        self.telephone = arr[9]
        self.email = arr[10]
        self.website = arr[11]
        self.position = arr[12]
        self.company = arr[13]
        self.meals = arr[14]
        self.billing_firstname = arr[15]
        self.billing_lastname = arr[16]
        self.card_type = arr[17]
        self.card_number = arr[18]
        self.card_csv = arr[19]
        self.exp_year = arr[20]
        self.exp_month = arr[21]
        self.session1 = arr[22]
        self.session2 = arr[23]
        self.session3 = arr[24]

    def __str__(self):  # just to test data was read in
        return "Class for registered name: % s % s" % (self.firstname, self.lastname)

    def data_array(self):  # returns an array like it was initiated from
        arr = []
        arr.append(self.date_of_registration)
        arr.append(self.title)
        arr.append(self.firstname)
        arr.append(self.lastname)
        arr.append(self.address1)
        arr.append(self.address2)
        arr.append(self.city)
        arr.append(self.state)
        arr.append(self.zipcode)
        arr.append(self.telephone)
        arr.append(self.email)
        arr.append(self.website)
        arr.append(self.position)
        arr.append(self.company)
        arr.append(self.meals)
        arr.append(self.billing_firstname)
        arr.append(self.billing_lastname)
        arr.append(self.card_type)
        arr.append(self.card_number)
        arr.append(self.card_csv)
        arr.append(self.exp_year)
        arr.append(self.exp_month)
        arr.append(self.session1)
        arr.append(self.session2)
        arr.append(self.session3)
        return arr

with db_connect("conference.sqlite") as db:         # connect to database
    # SQL command templates
    delete_registration_table = '''DROP TABLE IF EXISTS registration'''
    create_registration_table = '''CREATE TABLE IF NOT EXISTS registration (
                                    id integer PRIMARY KEY AUTOINCREMENT,
                                    reg_date date,
                                    title char(3),
                                    first_name text,
                                    last_name text,
                                    add1 text,
                                    add2 text,
                                    city text,
                                    st char(2),
                                    zip smallint,
                                    telephone text,
                                    email varchar(255),
                                    website varchar(255),
                                    co_position text,
                                    co text,
                                    meals text,
                                    bill_first_name text,
                                    bill_last_name text,
                                    card_type text,
                                    card_number integer,
                                    card_csv smallint,
                                    exp_year year,
                                    exp_month month,
                                    session_1 text,
                                    session_2 text,
                                    session_3 text);'''
    registration_template = '''INSERT INTO registration (
                                    reg_date,title,first_name,last_name,add1,add2,city,st,zip,telephone,email,website,
                                    co_position,co,meals,bill_first_name,bill_last_name,card_type,card_number,card_csv,
                                    exp_year,exp_month,session_1,session_2,session_3) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?,
                                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''

    curs = assign_cursor(db)                                                    # assign cursor
    registration_file = open_file('registrant_data.csv')                        # open data file
    recreate_table(db, delete_registration_table, create_registration_table)    # clear old table and recreate
    reg_arr = load_registration(registration_file)                              # loads award nominee data into array
    load_array_to_db(reg_arr, registration_template, db, curs)                  # load array into sql table




