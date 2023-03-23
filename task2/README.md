***Xabier Vega Castella***
### *Requirements:*

• The script should connect to a MySQL database using the mysql-connector-python library.

• The script should retrieve data from a specified table in the database.

• The script should perform some data analysis on the retrieved data using the pandas library.

• The data analysis should include at least one of the following: sorting, filtering, grouping, 
  aggregation, or visualization.
  
• The script should log any errors encountered during the data retrieval or analysis.

• The script should be runnable as a command-line application

---
### *step by step*.

The first thing to create is a databases and some table into mysql program or other distribution.

```python

CREATE DATABASE IF NOT EXISTS `analysis` DEFAULT CHARACTER SET latin1;

USE analysis;

CREATE TABLE sales (
  id varchar(10) NOT NULL,
  product_name varchar(30) DEFAULT NULL,
  quantity integer DEFAULT NULL,
  price integer DEFAULT NULL,
  date date NOT NULL,
  PRIMARY KEY (id)
) engine=innodb;

INSERT INTO sales VALUES ('1','product3','2','20','2023-01-1');
INSERT INTO sales VALUES ('2','product2','4','40','2022-02-24');
INSERT INTO sales VALUES ('3','product1','1','10','2021-03-12');
```
Then create the user.

```python
create user 'user1'@'localhost' identified by 'User1';
grant all privileges on *.* to 'user1'@'localhost'with grant option;
```
then need install pip for `pip install`. After installation install `pip install mysql-connector-python` and `pip install pandas`. If there are any problems installing, it is advisable to create a virtual desktop to install pandas. Make sure pandas is in the same path as python.

Once all this is done, we proceed to create the script. We import the necessary libraries.

```python
import mysql.connector # To provide connectivity to the MySQL server for client programs.
import pandas as pd # To bring the pandas data analysis library 
import logging # To do the register loggin in logsfile
```
For a logs create an order that registers all the deletions and creations indicating the path of the log file.

```python
logging.basicConfig(filename='mysql_analysis.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s
```

Defines a function to connect to the database where `connect_to_db` takes 4 arguments to connect to the database.If the connection succeeds, the `conn` function will be returned using the `return` keyword and if an exception occurs during the connection attempt, the `except` block will be executed. This is assigned to the variable .
The `logging.error()` function is called with a string describing the error. This function logs the error in a log called `mysql_analysis.log`.

```python
def connect_to_db(host, user, password, database):
    try:
        conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        return conn
    except mysql.connector.Error as e:
        logging.error(f"Unable to connect to database: {e}")
        return None
```
This code defines a function called `retrieve_data` that receives two arguments: a database connection and a table name. This function executes a SQL query to select all data in the specified table and returns the retrieved data. If an error occurs it sends a message indicating the error.

```python
def retrieve_data(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as e:
        logging.error(f"Unable to retrieve data: {e}")
        return None
```

```python
def perform_data_analysis(data):
    try:
        df = pd.DataFrame(data, columns=['id', 'product_name', 'quantity', 'price', 'date'])
        sorted_data = None
        if not df.empty:
            sorted_data = df.sort_values(by=['id'], ascending=[True])
        grouped_data = None
        if not df.empty:
            grouped_data = df.groupby(['product_name'])[['quantity', 'price']].sum()
        return sorted_data, grouped_data
    except Exception as e:
        logging.error(f"Unable to perform data analysis: {e}")
        return None, None
```

```python
def main():
    host = input("Enter MySQL host name: ")
    user = input("Enter MySQL user name: ")
    password = input("Enter MySQL user password: ")
    database = input("Enter MySQL database name: ")
    table = input("Enter MySQL table name: ")

    conn = connect_to_db(host, user, password, database)
    if not conn:
        return
    data = retrieve_data(conn, table)
    if not data:
        return
    sorted_data, grouped_data = perform_data_analysis(data)
    if sorted_data is None or grouped_data is None:
        return
    print("Sorted Data:")
    print(sorted_data)
    print("\nGrouped Data:")
    print(grouped_data)
    conn.close()
```

```python
if __name__ == "__main__":
    main()
```
For a logs create an order that registers all the deletions and creations indicating the path of the log file.
```python
logging.basicConfig(filename='backup.log', level=logging.INFO)
```
The next thing to do is to create a condition for the creation of the copies.
Call the condition `directory` and tell it that if the directory exists it will create a copy with the name previously specified in `backup_p`, also register the creation into the log file, and if the copy fails, log it with an error and if the directory is not found, also log it.
```python
            logging.info(f"The backup of {directory} has been succefully created")
        except Exception as e:
           logging.error(f"{directory} has an error with the backup: {e}")
    else:
        logging.error(f'{directory} does not exist')
```

Finally the oldest backups should be deleted when a new one is registered, for this, we are going to order them from the oldest copy to the most recent one in ascending order, this function is called `backup_d`.
```python
backup_d = sorted([os.path.join(backup_location, d)
                   for d in os.listdir(backup_location) 
                   if os.path.isdir(os.path.join(backup_location, d))])
```
After that create a condition that says that if `backup_d` is greater than `max_b` a function called `oldest` is defined and it assigns the oldest backup and then deletes it with `rmtree` and the whole process is recorded in the log file.

To make the script run automatically in windows put the nex command in console `schtasks /create /tn "Daily Backup" /tr "python C:\task1\backup_script.py" /sc daily /st 02:00:00`. The above command makes a scheduled task on the system to run the command `python C:\backup_script.py` every day at 2am

In linux execute the command `crontab -e` and add a new line with `0 2 * * * python3 backup_script.py` where it is indicated that it will be executed every day at 2am

---

### Checks

![foto 1](./img/1.jpg)

![foto 2](./img/2.jpg)

![foto 3](./img/3.jpg)
