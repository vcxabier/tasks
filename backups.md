<center>

# 


</center>

*Name: Xabier vega castellà*

### *Requirements:*

• The script should be able to create a backup of all files and directories specified in a configuration file.

• The configuration file should allow specifying multiple directories to be backed up, and where the backups should be stored.

• The script should create a new backup directory for each backup run with the current timestamp in the directory name.

• The script should keep a configurable number of backups and delete the oldest backups when the maximum number is reached.

• The script should log the backup process, including any errors encountered during the backup.

• The script should be runnable as a scheduled task.

### *step by step*.

The first thing to create is a configuration file named `conf.ini`

```python

[backup]
# set up the paths to be backed up
set_source= /test1, /test2
# set de destination of backups.
set_destination= /Backups/

[cuantity]
# set the maximum cuantity of backup that be store
max = 10
```
Then create the script with python. The first thing to do is to know which libraries to use. I use these libraries:

```python

import datetime # To set the time in the backup
import os #solves compatibility problems between operative systems.
import shutil # To do the new directory and create all 
import configparser # To read the cofiguration file
import logging # To do the register loggin in logsfile

```


Creamos la conexion con el servidor.
+ Para ello vamos a la maquina cliente y aseguramos que el nombre de equipo y de dominio este bien puesto. 

![2](./img/2.jpg)


To make the script run i do schedule a task in the operating system with Windows Task Scheduler. Open the program --> go to create task --> choose time interval, in this case daily al 2am--> choose execute a program--> choose the root path of the script

In linux execute the command `crontab -e` and add a new line with `0 2 * * * python /path/to/your/backup_script.py` where it is indicated that it will be executed every day at 2am
