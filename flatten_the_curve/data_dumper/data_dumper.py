import csv
import sqlite3
import pymysql
import os
import datetime
import argparse
import pandas

def connect_db(host,user,passwd,db):
    """
    Connect to mysql db
    """
    conn = pymysql.connect(host,user,passwd,db)
    c = conn.cursor

    return c,conn

def create_table(c,conn,create_q=None):
    """
    Create database and table
    """
    c = conn.cursor()
    c.execute(create_q)

    conn.commit()
    return c,conn

def covidcsv_to_table(dir,file,c,insert_q):
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

            elif(file.startswith('03-22') or
                    file.startswith('03-23') or
                    file.startswith('03-24') or
                    file.startswith('03-25') or
                    file.startswith('03-26') or
                    file.startswith('03-27') or
                    file.startswith('03-28') or
                    file.startswith('03-29') or
                    file.startswith('03-30') or
                    file.startswith('03-31') or
                    file.startswith('04-') or
                    file.startswith('05-0') or
                    file.startswith('05-1') or
                    file.startswith('05-20') or
                    file.startswith('05-21') or
                    file.startswith('05-22') or
                    file.startswith('05-23') or
                    file.startswith('05-24') or
                    file.startswith('05-25') or
                    file.startswith('05-26') or
                    file.startswith('05-27') or
                    file.startswith('05-28')):
                insert_q = '''INSERT INTO covid(file,report_date,fips,city,province_state,country_region,last_update,
                    lat,lon,confirmed,death,recovered,active,combined_key) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            else:
                insert_q = 'INSERT INTO covid VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

            covidcsv_to_table(dir,file,c,insert_q)
    return cnt

def read_covid_national_nl(file):
    """
    Read RIVM_NL_national.csv file to db
    """

    # full load, so delete everything first
    c.execute('DELETE FROM covid_hosp_nl')
    insert_q = '''INSERT INTO covid_hosp_nl(Datum,Aantal) VALUES(%s,%s)'''

    # read data to pandas df and pivot to keep cumulative values per date
    df = pandas.read_csv(file)
    df = df.pivot(index='Datum',columns='Type',values='AantalCumulatief')

    # write data to table
    filename = os.path.basename(file)
    print('Dumping {}'.format(filename))
    for row in df.iterrows():
        date = row[0]
        total_hosp = row[1]['Ziekenhuisopname']
        total_hosp = int(total_hosp.astype(int))

        # int() converts nan to -2147483648
        if total_hosp == -2147483648:
            total_hosp = None
        
        values = (date,total_hosp)
        print(values)
        c.execute(insert_q,values)

    conn.commit()

    return True

def read_covid_ic_nl(file):
    """
    Read nice_ic_by_day.csv file to db
    """
    # full load, so delete everything first
    c.execute('DELETE FROM covid_ic_nl')
    insert_q = '''INSERT INTO covid_ic_nl(date, icCount, newIntake, intakeCount, intakeCumulative,
                    survivedCumulative, diedCumulative, newSuspected, dischargedTotal) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

    # write data to table
    filename = os.path.basename(file)
    with open(file,'rt') as read_obj:
        reader = csv.reader(read_obj)
        # skip first row with headers
        next(reader)

        print('Dumping {}'.format(filename))
        for line in reader:
            line = [None if v == '' else v for v in line]
            c.execute(insert_q,line)
        conn.commit()
    
    return True


parser = argparse.ArgumentParser()

# Required positional arguments
parser.add_argument("host", help="MySQL host")
parser.add_argument("user", help="MySQL user")
parser.add_argument("passwd", help="MySQL passwd")
parser.add_argument("dir", help="COVID global data dir")
parser.add_argument("file_hosp_nl", help="COVID hosp NL data file")
parser.add_argument("file_ic_nl", help="COVID IC NL data file")
args = parser.parse_args()

# connect to DB
host = args.host
user = args.user
passwd = args.passwd
db = 'covid_data'
c,conn = connect_db(host,user,passwd,db)

# create table for Covid global
create_q = '''CREATE TABLE IF NOT EXISTS covid
                (file varchar(255),report_date date,fips int,city varchar(255),province_state varchar(255)
                ,country_region varchar(255),last_update varchar(255),lat decimal(10,8),lon decimal(11,8),confirmed int
                ,death int,recovered int,active int,combined_key varchar(255))'''
c,conn = create_table(c,conn,create_q=create_q)

# create table for Covid hosp NL
create_q = '''CREATE TABLE IF NOT EXISTS covid_hosp_nl
                (Datum date,Aantal int)'''
c,conn = create_table(c,conn,create_q=create_q)

# create table for NICE data
create_q = '''CREATE TABLE IF NOT EXISTS covid_ic_nl
                (date date, newIntake int, intakeCount int, intakeCumulative int, icCount int,
                 diedCumulative int, survivedCumulative int)'''
c,conn = create_table(c,conn,create_q=create_q)


# read all CSVs to db
cnt = read_covid(args.dir) #'D:/code/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/' # https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports
print('Inserted {} files'.format(cnt))

read_covid_national_nl(args.file_hosp_nl) # /d/code/CoronaWatchNL/data-geo/data-national/RIVM_NL_national.csv
print('Inserted {}'.format(args.file_hosp_nl))

read_covid_ic_nl(args.file_ic_nl) #'D:/code/CoronaWatchNL/data/nice_ic_by_day.csv' # https://github.com/J535D165/CoronaWatchNL/tree/master/data
print('Inserted {}'.format(args.file_ic_nl))

read_covid_national_nl(args.file_hosp_nl)

conn.close()
