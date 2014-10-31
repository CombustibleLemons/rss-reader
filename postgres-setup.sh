#! /bin/sh
sudo -u postgres -H sh -c "createdb feeddb"
sudo -u postgres -H sh -c "createuser -P combustible"
sudo -u postgres -H sh -c "psql -c 'GRANT ALL PRIVLEGES ON DATABASE feeddb TO combustible;'"
