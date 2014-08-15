#!/bin/sh
sudo -u postgres psql -c "create database test_jmbo_twitter encoding 'UTF8' template template_postgis"
sudo -u postgres psql -c "create user test"
sudo -u postgres psql -c "alter user test createdb"
./ve/bin/python setup.py test
