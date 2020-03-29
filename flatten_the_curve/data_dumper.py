import csv
import sqlite3
import os
import datetime


def create_db_and_table(db_name=':memory:',create_q=None):
    """
    Create database and table
    """
    
    conn = sqlite3.connect(db_name)
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
        data = list(map(tuple, reader))

    for line in data:
        c.execute(insert_q.format(filename,reportdate),line)
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
                insert_q = '''INSERT INTO covid(file,report_date,province_state,country_region,last_update,confirmed,
                                death,recovered) VALUES("{}","{}",?,?,?,?,?,?)'''
            elif(file.startswith('03-0') or
                    file.startswith('03-1') or
                    file.startswith('03-20') or
                    file.startswith('03-21')):
                insert_q = '''INSERT INTO covid(file,report_date,province_state,country_region,last_update,confirmed,
                    death,recovered,lat,long) VALUES("{}","{}",?,?,?,?,?,?,?,?)'''
            else:
                insert_q = 'INSERT INTO covid VALUES("{}","{}",?,?,?,?,?,?,?,?,?,?,?,?)'

            csv_to_table(dir,file,c,insert_q)
    return cnt

# create DB + table
db_name = 'covid_data.db'
create_q = '''CREATE TABLE IF NOT EXISTS covid
                (file text,report_date date,fips integer,city text,province_state text,country_region text,last_update datetime,
                lat numeric,long numeric,confirmed int,death int,recovered int,active int,combined_key text)'''
c,conn = create_db_and_table(db_name,create_q=create_q)


# read all CSVs to db
dir = 'D:/code/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/'
cnt = read_covid(dir)
print('Inserted {} files'.format(cnt))

conn.close()