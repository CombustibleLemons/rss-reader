#! /bin/sh
sudo -u postgres -H sh -c "psql -f flush_database.postgresql"
