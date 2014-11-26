#! /bin/sh
sudo -u postgres -H sh -c "psql -f flush_database.postgresql"
#cd rss_reader
./manage.py migrate
./manage.py installwatson
./manage.py buildwatson
./manage.py shell < init_script.py
