#!/bin/bash
# args: mysql host, mysql user, mysql passwd

cd /home/jochem/code/COVID-19
git pull
cd /home/jochem/code/CoronaWatchNL
git pull
python d:/code/rand/flatten_the_curve/data_dumper/data_dumper.py $1 $2 $3  \
  '/home/jochem/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports/' \
  '/home/jochem/CoronaWatchNL/data/rivm_corona_in_nl_hosp.csv' \
  '/home/jochem/CoronaWatchNL/data/nice_ic_by_day.csv'
  >/home/jochem/code/rand/flatten_the_curve/log_data_dumper 2>&1