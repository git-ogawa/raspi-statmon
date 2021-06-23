# Getting started

This chapter describes the procedure for monitoring the status of raspberry pi on 
the web browser step by step.


## Directory structure
The directory tree of this project is as follows. `rstatmon` is root directory, `db_setup.py` and `rstatmon.py` are the python scripts to be executed by the user. There are other files and sub-directories in the `rstatmon`

```bash
rstatmon
└-- db_setup.py
└-- rstatmon.py
└-- [others]
```

rstatmon.py
: The main script that runs the server by `flask`

db_setup.py
: The script for database setup.



## Mysql setup 
:::{note}
If you have been already using mysql (or mariaDB), you can skip this step and proceed to [Database setup](#database-setup).
:::
This section describes the steps needed to use the database for the first time.


### 1. Disable unix_socket
At first, make sure that mysql is installed and that you can log in. 

```
sudo mysql
```

If you can log in, you will see the following message. 

```
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 11
Server version: 10.0.28-MariaDB-2+b1 Raspbian testing-staging

Copyright (c) 2000, 2016, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> 
```

Next, make sure that unix sock is enabled. To do this, type `use mysql;`, then `select host,user,password,plugin from user;`

```sql
MariaDB [(none)]> use mysql;
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed
MariaDB [mysql]> select host, user,password,plugin from user;
+-----------+------+----------+-------------+
| host      | user | password | plugin      |
+-----------+------+----------+-------------+
| localhost | root |          | unix_socket |
+-----------+------+----------+-------------+
1 row in set (0.00 sec)
```
From the above message, you can see that the unix_socket is activated. Disable this by typing `UPDATE user SET plugin='' WHERE User='root';`

### 2. Set the password for the root user
Set a password for root to log in using the password method. Set the password by typing the following command (where `***` is the password you want to set)
```
update mysql.user set password=password('***') where user = 'root';
```
If the password is set correctly, you will see the following message.

```sql
MariaDB [(none)]> update mysql.user set password=password('***') where user = 'root';
Query OK, 0 rows affected (0.00 sec)
Rows matched: 1  Changed: 0  Warnings: 0
```
After this, exit from mysql by typing `exit` and then restart mysql and update the changes by the following commands in the terminal.
```
sudo systemctl restart mysql
```
Finally, make sure that you can login as the root user with the password (here `***` is the password you set above).
```
mysql -u root -p***
```


## Database setup
At first, you need create the database and table for user account management. The rstatmon uses `mysql`or `mariadb` to access databases through`flask-SQLAlchemy`. What you have to do at first is that set what user will be used when access to the database. To register the user, exceute `db_setup.py` with "register" ( `-r` )and "password" ( `-p` ) options as follows.
```
python db_setup.py -r [-u <username>] -p <password> 
```

Here is a list of options related to the user registration. Only password option need to be specified. For the other options, the default values are used if not to be specified.

| Option | Description        | Required | Default   |
| ------ | ------------------ | -------- | --------- |
| -u     | User name          | Optional | root      |
| -p     | Password           | Required | -         |
| --port | Port used in mysql | Optional | 3306      |
| -s     | Server             | Optional | localhost |


For example, you want to access database as the root user with password "1234", execute as below.
```
python db_setup.py -r -p 1234 
```
Or set below if you want to use another user "test" and password "foo".
```
python db_setup.py -r -u test -p foo
```
This settings is stored as the json file in the `config/database.json`.


:::{warning}
When creating the database, login as root user with the password. If you have't set up yet, you need setup before this step (see [Set the password for the root user](#set-the-password-for-the-root-user)).
:::


Next, Execute `rstatmon.py` with `-c` option to create database and table for managing users.
```bash
>> python rstatmon.py -c
Create 'user' table in database 'raspi'
Create admin user.
```
Executing with this option creates the new database `raspi`, tabel `user` in the database (shown at first line), adds the default user `admin` in the table (shown at second line). You can also add other user from the register page. Since the admin's password is vulnable, adding other user is recommended.


## Start app
To start the application, execute the `rstatmon.py` in the terminal. Once starting the app, the server will be started and you can enter to login page in the browser.

```bash
>> python rstatmon.py 
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```
In the above case, you can access the page by `http://0.0.0.0:5000/` from the same machine where the app is running (that is raspberry pi). In case that access from other PC with the same network, access by `https://[ip_addr]:5000/`, here [ip_addr] is the IP address of the raspberry pi. From here, keep the server running.



## Login & add user
When access to project root page, you are required to login. You can login as the user `admin` with the password of `admin`, but adds other user is recommended for secure. Clicking the sign up button to redirect the sign up page for creating new account. As shown below, The button is shown only when accessing the page from the machine running the app (thus the button is hidden when access from another PC).

:::{figure-md} fig-target
:class: myclass

<img src="../img/login.png" width="400px">

The button is hidden (when connected from other PC).
:::

:::{figure-md} fig-target
:class: myclass

<img src="../img/signup.png" width="400px">

The button is displayed (when connected from the raspberry pi).
:::


## Monitoring
As the login procedure is success, you will be redirected to home page. In the top of the page, you see the list of information about hardware running the app (that is raspberry pi). You also see the five graphs showing the current values of getting from raspberry pi. Each graph shows the change in the data below over time.

- CPU temperature
- CPU usage
- Allocated memory
- Frequency
- Load average

The update cycle of the graphs is 1 seconds. The duration displayed on each graph is set to 10 seconds by default, which can be changed from the setting page (see below).


## Graph setting
In setting page, you can change the settings of the graphs. To change the current settings, input the value in each box, then click save button to submit the form. If the input values are valid, a message will appear letting you know that the changes are accepted, then the graphs on the home page will be updated. 


| Field | Attribute | Type | Description |
| :-- | :-- | :-- | :-- |
| y-axes | min | int | Minimum of y axis | 
| y-axes | max | int | Maximum of y axis | 
| y-axes | step | int | Step size of tick in y axis | 
| streaming | duration | int | The duration that the data will be displayed on the graph | 

The acceptable range of these values is as follows

- min, max and step

| Graph       | Range     |
| :---------- | :-------- |
| temperature | 0 ~ 1000  |
| usage       | 0 ~ 1000  |
| memory      | 0 ~ 10000 |
| frequency   | 0 ~ 10000 |
| usage       | 0 ~ 100   |

- duration

| Graph | Range         |
| :---- | :------------ |
| all   | 1000 ~ 600000 |

