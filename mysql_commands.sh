#!/bin/sh
## Install mysql-server
sudo apt install mysql-server
## Start mysql service
service mysql start
## Secure the installation
sudo mysql_secure_installation
## Connect to local mysql server
sudo mysql
CREATE USER 'ivan'@'localhost' IDENTIFIED BY 'CSC501@ssignments';
CREATE DATABASE assignment1;
USE assignment1;
GRANT ALL PRIVILEGES ON `assignment1`.* TO ivan@localhost;
GRANT FILE ON *.* TO ivan@localhost;