import pandas as pd

def extract_data(file_path: str) -> pd.DataFrame:    
    """
    Extract data from a parquet file and load it into a pandas DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data.
    """
    try:
        df = pd.read_parquet(file_path)
        return df
    except Exception as e:
        print(f"Error reading the CSV file: {e}")
        return pd.DataFrame()
    
if __name__ == "__main__":
    # Example usage
    file_path = "data/2023 DE_case_dataset.gz.parquet"
    df = extract_data(file_path)
    print(df.head())
    print(type(df["holes"][0]))