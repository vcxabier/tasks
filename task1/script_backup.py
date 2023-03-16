#import libraries
import shutil
import configparser
import os
import datetime
import logging
# Read config file
parser=configparser.ConfigParser()
parser.read("conf.conf")
#
#FROM CONFIG FILE READ
#
# The backup directories
backup_dirs = parser.get('backup', 'set_source').split(',')
#The backup location 
backup_location = parser.get('backup', 'set_destination')
#The maximum backups that can create
max_b = parser.getint('cuantity', 'max')
#
#Stablished currend timestamp.
time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#join the location and date
backup_p = os.path.join(backup_location, f'backup_{time}')
#Create the directory
os.mkdir(backup_p)
#
# Set up the register in the loggins.
logging.basicConfig(filename='backup.log', level=logging.INFO)
#
#Copy the directory to the backup location
for directory in backup_dirs:
#check if exist
    if os.path.isdir(directory):
        try:
#Create a copy of the directory in the backup location
            shutil.copytree(directory, os.path.join(backup_p, os.path.basename(directory)))
#register log            
            logging.info(f"The backup of {directory} has been succefully created")
#
        except Exception as e:
#If failed the copy register in the log
           logging.error(f"{directory} has an error with the backup: {e}")
    else:
#Log an error if directory does not exist
        logging.error(f'{directory} does not exist')
# sort the list of backup in ascendant order
backup_d = sorted([os.path.join(backup_location, d)
                   for d in os.listdir(backup_location) 
                   if os.path.isdir(os.path.join(backup_location, d))])
#If the list is greater than the maximium specified,then the oldest backup is identified as first and deleted.
if len(backup_d) > max_b:
    oldest = backup_d[0]
#Remove the directory and all its content
    shutil.rmtree(oldest)
#The deletion is registered
    logging.info(f"backup droped: {oldest}")