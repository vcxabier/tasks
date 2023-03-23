import mysql.connector
import pandas as pd
import logging
#
# Add logging configuration to the script to log any errors encountered during the data retrieval or analysis:
logging.basicConfig(filename='mysql_analysis.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')
#
# Define a function to connect to the database:
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
#
# Define a function to retrieve data from the table:
def retrieve_data(conn, table):
    try:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        data = cursor.fetchall()
        return data
    except mysql.connector.Error as e:
        logging.error(f"Unable to retrieve data: {e}")
        return None
#
# Define a function to perform data analysis using pandas:
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
#
# Define a function to run the script as a command-line application:
def main():
    host = input("Enter MySQL host name: ") # Enter the domain, localhost or ipserver
    user = input("Enter MySQL user name: ") # Enter the user that have permissions on the database
    password = input("Enter MySQL user password: ") # The password of the user
    database = input("Enter MySQL database name: ") # Enter the name of the database
    table = input("Enter MySQL table name: ") # Enter the table name
#
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
#
#
#
# Call the main function when the script is executed from the command line:
if __name__ == "__main__":
    main()
