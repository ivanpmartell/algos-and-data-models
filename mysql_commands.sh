#!/bin/sh
## Install mysql-server
sudo apt install mysql-server
## Start mysql service
sudo service mysql start
## Secure the installation
sudo mysql_secure_installation
## Connect to local mysql server
sudo mysql
CREATE USER 'ivan'@'localhost' IDENTIFIED BY 'CSC501@ssignments';
CREATE DATABASE assignment1;
USE assignment1;
GRANT FILE ON *.* TO ivan@localhost;
GRANT ALL PRIVILEGES ON `assignment1`.* TO ivan@localhost;
GRANT ALL PRIVILEGES ON `assignment1`.* TO ivan@'%' IDENTIFIED BY 'CSC501@ssignments';
# Remote access
# /etc/mysql/mysql.conf.d/mysqld.cnf CHANGE TO bind-address = 0.0.0.0
# sudo service mysql restart
