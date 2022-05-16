#! /bin/zsh
# Get the most recent solar data from my logger application.
d=`date "+%Y-%m-%d"`
scp pi@solarpi.local:solardata/solardata.csv local-solardata-$d.csv