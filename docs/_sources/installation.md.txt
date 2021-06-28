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


## Uninstallation
You can uninstall the application by `pip` but the database and data files need to be deleted before doing that. To do this is to execute `rstatmon --remove`. Typing `yes` to the prompt delete the files as follows.
```bash
$ rstatmon --remove
Do you really remove the all data? (yes/[no]):yes
Deleted raspi database
Database delete sucessfully completed.
Delete /home/username/.local/lib/python3.8/site-packages/rstatmon/static
Delete /home/username/.local/lib/python3.8/site-packages/rstatmon/templates
Delete /home/username/.local/lib/python3.8/site-packages/rstatmon/data
Delete /home/username/.local/lib/python3.8/site-packages/rstatmon/config
Delete process sucessfully completed.
```

Then, uninstall the app by pip.
```
pip uninstall rstatmon
```