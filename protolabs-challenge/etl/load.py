import sqlite3

def load_data(df, db_path="data/cases.db", table_name="cases"):
    """
    Load the transformed DataFrame into a SQLite database.

    Args:
        df (pd.DataFrame): The transformed DataFrame to be loaded.
        db_path (str): The path to the SQLite database file.
        table_name (str): The name of the table to load data into.
    """
    try:
        # Connect to SQLite database (it will be created if it doesn't exist)
        conn = sqlite3.connect(db_path)
        
        # Load DataFrame into the specified table
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        
        print(f"Data loaded successfully into {table_name} table in {db_path} database.")
    except Exception as e:
        print(f"Error loading data into database: {e}")
    finally:
        conn.close()