import pyodbc as py
import pandas as pd


def get_sec_ID(identifiers):
        # Set up the database connection parameters
        server = 'PROD-SQL-RO'
        database = 'LM'
        username = 'ARBFUND\matthewray'
        password = 'Uhglbk547895207&'
        driver = '{ODBC Driver 17 for SQL Server}'
        

        # Create the connection string
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};Trusted_Connection=yes;TrustServerCertificate=yes;MultiSubnetFailover=yes'

        # Connect to the database
        conn = py.connect(conn_str)

        # Create a cursor object to execute the SQL statements
        cursor = conn.cursor()

        cursor.execute('SET QUERY_GOVERNOR_COST_LIMIT 300')

        # Execute a SQL query
        query = f'''
        SELECT   Cusip,ID
        FROM securitymaster
        WHERE Cusip IN ({identifiers})
        '''

        cursor.execute(query)

        # Fetch all the rows from the query result
        cursor.fetchall()
        df = pd.read_sql(query,conn)

        # Close the cursor and the connection
        cursor.close()
        conn.close()
  

        return df, print("SQL executed within the timeout period")
