# Name: Dustin Segawa
# Assignment: CS336 Assignment #10
# Created: 8/18/2020
# Description: Python 10 tags page for assignment

import math
import sqlite3
import os


# global variables
reg_data = []       # array for registration dictionary
html_data = []      # array for html lines
line_total = 0      # total line counter
line_dict = {       # dictionary for html container lines
    'html': {'string': '<html', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</html>\n'},
    'body': {'string': '<body>', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</body>\n'},
    'main': {'string': '<main>', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</main>\n'},
    'page': {'string': 'class="page"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},
    'pgcol': {'string': 'class="nt10_col"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},
    'row': {'string': 'class="nt10_row"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},
    'nt': {'string': 'class="nt10"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},
    'name': {'string': 'class="name10"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},     # added for 10 tag
    'fname': {'string': 'firstname', 'ln': 0, 'sp': 0, 'head': '', 'tail': ''},
    'lname': {'string': 'lastname', 'ln': 0, 'sp': 0, 'head': '', 'tail': ''},
    'position': {'string': 'position', 'ln': 0, 'sp': 0, 'head': '', 'tail': ''},
    'coloc': {'string': 'class="co_loc"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},
    'co': {'string': 'company', 'ln': 0, 'sp': 0, 'head': '', 'tail': ''},
    'loc': {'string': 'class="loc"', 'ln': 0, 'sp': 0, 'head': '', 'tail': '</div>\n'},
    'city': {'string': 'city', 'ln': 0, 'sp': 0, 'head': '', 'tail': ''},
    'state': {'string': 'state', 'ln': 0, 'sp': 0, 'head': '', 'tail': ''}
}


# attempts to open file, terminates with error if not found
# IN: file name for opening
# OUT: variable for opened file
# CALLS: none
def open_file(file):
    try:        # loads registration data into dictionary if available
        opfile = open(file, 'r')
        print('--', file, 'FILE FOUND --')
        return opfile
    except IOError:
        exit('-- ' + file + ' FILE NOT FOUND --')

# attempts to delete old file and creates a new output file
# IN: file name for removal/creation
# OUT: variable for opened file
# CALLS: none
def del_file(file):
    try:  # tries to remove existing nametag file
        os.remove(file)
        print('-- OLD FILE REMOVED --')
    except IOError:
        print('-- OLD FILE NOT FOUND --')
    finally:
        out_file = open(file, 'w')  # creates new nametag file
        return out_file

# loads registration data from sql array into dictionary
# IN: sql array
# OUT: none, appends dictionary lines to reg_data array
# CALLS: none
def load_registration(sql):
    for line in sql:                           # loop through each line in file
        lineList = []
        for j in range(1, len(line)):   # loop through tuple removing key
            lineList.append(line[j])    # append to list
        newDict = {
            'date_of_registration': lineList[0],
            'title': lineList[1],
            'firstname': lineList[2],
            'lastname': lineList[3],
            'address1': lineList[4],
            'address2': lineList[5],
            'city': lineList[6],
            'state': lineList[7],
            'zipcode': lineList[8],
            'telephone': lineList[9],
            'email': lineList[10],
            'website': lineList[11],
            'position': lineList[12],
            'company': lineList[13],
            'meals': lineList[14],
            'billing_firstname': lineList[15],
            'billing_lastname': lineList[16],
            'card_type': lineList[17],
            'card_number': lineList[18],
            'card_csv': lineList[19],
            'exp_year': lineList[20],
            'exp_month': lineList[21],
            'session1': lineList[22],
            'session2': lineList[23],
            'session3': lineList[24]
        }                                   # store line in each field
        reg_data.append(newDict)            # append each line in dictionary

# loads html lines into array, and line locations into dictionary
# IN: file name for html data
# OUT: none, appends lines to html_data array and updates line dictionary
# CALLS: none
def load_html(file, line_dict, line_total):
    for line in file:               # loop through each line in file
        html_data.append(line)      # append each dictionary line in array
        line_total += 1             # count total lines in file

    xline = 0                               # set line counter to 0
    for item in line_dict.items():          # iterate through each item in dict once
        for xline in range(xline, len(html_data)):  # iterate through each line in file once using counter range
            if html_data[xline].find(item[1]['string']) >= 0 and item[1]['sp'] == 0:    # test for matching string
                item[1]['ln'] = xline                                                   # update line number
                item[1]['sp'] = html_data[xline].find(html_data[xline].strip())         # update tabbed spaces
                if item[1]['tail'] == '':       # update tail if empty
                    item[1]['head'] = html_data[item[1]['ln']].split(sep=item[1]['string'])[0]  # update head
                    item[1]['tail'] = html_data[item[1]['ln']].split(sep=item[1]['string'])[1]  # update tail
                break       # break if when found
            else:
                xline += 1  # increment counter

# writes open html container command to output file
# IN: file name for output, html data array, line dictionary
# OUT: none, writes to output file
# CALLS: none
def open_container(file, html, dict):
    file.write(html[dict['ln']])  # open container based on line number in dictionary

# writes tag info to output file
# IN: file name for output, registration data array, line dictionary
# OUT: none, writes to output file
# CALLS: none
def write_line(file, reg, dict):
    file.write(dict['head'] + reg[dict['string']] + dict['tail'])

# writes blank tag info to output file
# IN: file name for output, line dictionary
# OUT: none, writes to output file
# CALLS: none
def write_blank(file, dict):
    file.write(dict['head'] + dict['tail'])

# writes close html container command to output file
# IN: file name for output, line dictionary
# OUT: none, writes to output file
# CALLS: none
def close_container(file, dict):
    file.write(' ' * dict['sp'] + dict['tail'])

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


with db_connect("../database_code/conference.sqlite") as db:         # connect to database
    curs = assign_cursor(db)  # assign cursor
    curs.execute("SELECT * FROM registration")
    reg_sql = curs.fetchall()
    # rows = curs.fetchall()
    # for row in rows:
    #     print(tuple(row))

# reg_file = open_file('registrant_data.csv')
html_file = open_file('../templates/nametags10_template.html')
html_out = del_file('../templates/nametags10.html')
load_registration(reg_sql)
load_html(html_file, line_dict, line_total)

tot_tags = len(reg_data)            # total tags
tot_pg = math.ceil(tot_tags / 10)    # total pages to print

for i in range(0, line_dict['main']['ln']+1):     # writes HTML header information through <main>
    html_out.write(html_data[i])

x = 0                                   # initialize tag counter
for pg in range(0, tot_pg):             # loop creating enough page templates for all tags
    print('Generating page: ', pg+1)
    open_container(html_out, html_data, line_dict['page'])  # page container
    open_container(html_out, html_data, line_dict['pgcol'])  # col container
    for row in range(0, 5):         # 5 rows on page
        # print('Generating row: ', row+1)
        open_container(html_out, html_data, line_dict['row'])  # row container
        for col in range(0, 2):     # 2 columns of tags
            try:
                test = reg_data[x]  # test if dictionary exists
                open_container(html_out, html_data, line_dict['nt'])        # tag container
                open_container(html_out, html_data, line_dict['name'])      # added for 10 tag
                write_line(html_out, reg_data[x], line_dict['fname'])
                write_line(html_out, reg_data[x], line_dict['lname'])
                close_container(html_out, line_dict['name'])                # added for 10 tag
                write_line(html_out, reg_data[x], line_dict['position'])
                open_container(html_out, html_data, line_dict['coloc'])     # company and location container
                write_line(html_out, reg_data[x], line_dict['co'])
                open_container(html_out, html_data, line_dict['loc'])       # location container
                write_line(html_out, reg_data[x], line_dict['city'])
                write_line(html_out, reg_data[x], line_dict['state'])
                close_container(html_out, line_dict['loc'])
                close_container(html_out, line_dict['coloc'])

                close_container(html_out, line_dict['nt'])
            except IndexError:
                # print(x + 1, 'VOID TAG')
                open_container(html_out, html_data, line_dict['nt'])        # tag container
                open_container(html_out, html_data, line_dict['name'])      # name container
                write_blank(html_out, line_dict['fname'])
                write_blank(html_out, line_dict['lname'])
                close_container(html_out, line_dict['name'])
                write_blank(html_out, line_dict['position'])
                open_container(html_out, html_data, line_dict['coloc'])     # company and location container
                write_blank(html_out, line_dict['co'])
                open_container(html_out, html_data, line_dict['loc'])       # location container
                write_blank(html_out, line_dict['city'])
                write_blank(html_out, line_dict['state'])
                close_container(html_out, line_dict['loc'])
                close_container(html_out, line_dict['coloc'])
                close_container(html_out, line_dict['nt'])
            x += 1      # increment tag counter
        close_container(html_out, line_dict['row'])
    close_container(html_out, line_dict['pgcol'])
    close_container(html_out, line_dict['page'])
# close out rest of html file containers
close_container(html_out, line_dict['main'])
close_container(html_out, line_dict['body'])
close_container(html_out, line_dict['html'])
html_out.close()
