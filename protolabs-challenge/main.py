from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

if __name__ == "__main__":
    # Extract the data
    df = extract_data("data/2023 DE_case_dataset.gz.parquet")
    # Transform the data
    df = transform_data(df)
    # Load the data
    load_data(df)