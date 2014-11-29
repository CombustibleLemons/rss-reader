#! /bin/sh
sudo -u postgres -H sh -c "psql -f flush_database.postgresql"
./manage.py migrate
./manage.py installwatson
./manage.py buildwatson
./manage.py shell < init_script.py
