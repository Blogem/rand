import csv
import sqlite3
import pymysql
import os
import datetime
import argparse


def create_db_and_table(host,user,passwd,db,create_q=None):
    """
    Create database and table
    """
    
    #conn = sqlite3.connect(db_name)
    conn = pymysql.connect(host,user,passwd,db)
    c = conn.cursor()

    c.execute(create_q)

    conn.commit()
    return c,conn

def csv_to_table(dir,file,c,insert_q):
    """
    Read CSV to table
    """
    filename = file

    #get report date from filename
    reportdate = filename.split('.')[0]
    reportdate = datetime.datetime.strptime(reportdate, "%m-%d-%Y").strftime("%Y-%m-%d")
    
    # read csv to tuple, insert each element along with metadata
    file = dir+file
    with open(file,'rt') as read_obj:
        reader = csv.reader(read_obj)
        # skip first row with headers
        next(reader)
        #data = list(map(tuple, reader))

        print('Dumping {}'.format(filename))
        for line in reader:
            line.insert(0,reportdate)
            line.insert(0,filename)
            line = [None if v == '' else v for v in line]

            c.execute(insert_q,line)
        conn.commit()

def read_covid(dir):
    """
    Loop through all covid CSVs in dir and dump in db

    Needs better schema detection
    """

    # full load, so delete everything first
    c.execute('DELETE FROM covid')

    # loop through all files in directory, skip non-csv
    cnt = 0
    for file in os.listdir(dir):
        if file.endswith('.csv'):
            cnt += 1
            # create correct query for schema of the file (ugly)
            if(file.startswith('01-') or file.startswith('02-')):
                # insert_q = '''INSERT INTO covid(file,report_date,province_state,country_region,last_update,confirmed,
                #                 death,recovered) VALUES("{}","{}",?,?,?,?,?,?)'''
                insert_q = '''INSERT INTO covid(file,report_date,province_state,country_region,last_update,confirmed,
                                death,recovered) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)'''
            elif(file.startswith('03-0') or
                    file.startswith('03-1') or
                    file.startswith('03-20') or
                    file.startswith('03-21')):
                insert_q = '''INSERT INTO covid(file,report_date,province_state,country_region,last_update,confirmed,
                    death,recovered,lat,lon) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''
            else:
                insert_q = 'INSERT INTO covid VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            csv_to_table(dir,file,c,insert_q)
    return cnt



parser = argparse.ArgumentParser()

# Required positional arguments
parser.add_argument("host", help="MySQL host")
parser.add_argument("user", help="MySQL user")
parser.add_argument("passwd", help="MySQL passwd")
parser.add_argument("dir", help="COVID data dir")
args = parser.parse_args()

# connect to DB and create table
host = args.host
user = args.user
passwd = args.passwd
db = 'covid_data'
create_q = '''CREATE TABLE IF NOT EXISTS covid
                (file varchar(255),report_date date,fips int,city varchar(255),province_state varchar(255)
                ,country_region varchar(255),last_update varchar(255),lat decimal(10,8),lon decimal(11,8),confirmed int
                ,death int,recovered int,active int,combined_key varchar(255))'''
c,conn = create_db_and_table(host,user,passwd,db,create_q=create_q)

# read all CSVs to db
cnt = read_covid(args.dir) #'D:/code/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/' # https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
print('Inserted {} files'.format(cnt))

conn.close()