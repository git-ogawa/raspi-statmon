# Appendix

## Database location 
The database "raspi" for managing user logins is created in the top. You can directly check the content of the database and table from mysql.

```sql
MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| raspi              |
+--------------------+
4 rows in set (0.003 sec)


MariaDB [(none)]> select * from raspi.user;
+---------+----------+--------------------------------------------------------------+
| user_id | username | password                                                     |
+---------+----------+--------------------------------------------------------------+
| 000     | admin    | $2b$12$qrnmyL03i4dXdraHgqwZ2./cTQLzuoZL3hZMqAQIf57hkhV6StUKq |
+---------+----------+--------------------------------------------------------------+
1 row in set (0.001 sec)
```
Each row of the table consists of user_id, username and hashed password of the registered user. Newly registered users' information will also be added to the table.



## Data store
The RStatMon stores the obtained data in log files. The obtained data are written to csv and stored as data log. The csv is stored to `stat_data` directory in the `data`. The dirctory contains sub-directory whose dir name is the data `yyyymm` The log has the file name of `yymmdd.csv` and is stored in the sub-directory.

```bash
data
└-- stat_data
    └-- yyyymm
        └-- yymmdd.csv
```

The csv contains the header in the first line and the data in subsequent lines. so this can be used for other purposes (for example plotting graph with pandas and matplotlib as shown below).

:::{figure-md} fig-target
:class: myclass

<img src="../img/graph_example.png" width="400px">

Plotting CPU temperature change using matplotlib
:::


## User log
The operations about user account such as login, logout, create and delete account are written to user log. In the log, The result of process, date, IP address of the PC accessing the machine, the detailed message are shown according to the following format.
```
[<log_level> <date>] <ip_address> : <message>
```
The example are shown as below.
```python
pi@raspberrypi:~/raspi_statmon/rstatmon/data $ cat log/202106/20210603.log 
[SUCCESS 2021-06-03 02:26:43:502] 127.0.0.1 : login success
[SUCCESS 2021-06-03 02:49:32:669] 127.0.0.1 : login success
[SUCCESS 2021-06-03 17:02:24:807] 127.0.0.1 : login success
```