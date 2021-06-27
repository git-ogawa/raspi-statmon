Installation
============

## The project
You can install the project by `pip`
```bash
pip install git+https://github.com/git-ogawa/raspi-statmon.git
```

## MySQL

The project uses MySQL, so install them with apt
```
sudo apt install mysql-server
```
you maybe can't install mysql in the version of your machine. In that case, try to install mariaDB instead.
```
sudo apt install mariadb-server-10.0
```

## pandas
The prohect uses `pandas` but the installation by pip doesn't seem to be working in raspberry pi OS. Thus, Install by following with apt.
```
sudo apt install python3-pandas
```