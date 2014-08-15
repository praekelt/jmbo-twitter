#!/bin/sh
#sudo -u postgres psql -c "create database test_jmbo_twitter encoding 'UTF8' template template_postgis"
sudo -u postgres psql -c "create user test"
sudo -u postgres psql -c "alter user test createdb"
sudo -u postgres psql -c "create database test_jmbo_twitter with owner test encoding 'UTF8'"
sudo -u postgres psql -d test_jmbo_twitter -c "create extension postgis"
sudo -u postgres psql -d test_jmbo_twitter -c "create extension postgis_topology"

./ve/bin/python setup.py test
