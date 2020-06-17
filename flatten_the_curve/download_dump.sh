#!/bin/bash
# args: mysql host, mysql user, mysql passwd

cd /home/jochem/code/COVID-19
git pull
cd /home/jochem/code/CoronaWatchNL
git pull
python3 /home/jochem/code/rand/flatten_the_curve/data_dumper/data_dumper.py $1 $2 $3  \
  '/home/jochem/code/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/' \
  '/home/jochem/code/CoronaWatchNL/data-geo/data-national/RIVM_NL_national.csv' \
  '/home/jochem/code/CoronaWatchNL/data/nice_ic_by_day.csv'
  >/home/jochem/code/rand/flatten_the_curve/log_data_dumper 2>&1
