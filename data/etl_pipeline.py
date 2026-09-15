import csv
import os
import snowflake.connector

# Connection Parameters
SNOWFLAKE_USER = os.getenv("SF_USER", "YOUR_USERNAME")
SNOWFLAKE_PASSWORD = os.getenv("SF_PASSWORD", "YOUR_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SF_ACCOUNT", "YOUR_ACCOUNT_LOCATOR")
SNOWFLAKE_WAREHOUSE = "COMPUTE_WH"
SNOWFLAKE_DATABASE = "DEMO_DB"
SNOWFLAKE_SCHEMA = "PUBLIC"

def extract_and_transform_csv(file_path: str) -> list:
    cleaned_rows = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            cleaned_row = (
                int(row['id']),
                row['first_name'].strip().capitalize(),
                row['last_name'].strip().capitalize(),
                row['email'].strip().lower(),
                row['signup_date'],
                row['status'].strip().upper()
            )
            cleaned_rows.append(cleaned_row)
    return cleaned_rows

def load_to_snowflake(data: list, table_name: str):
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    cursor = conn.cursor()
    try:
        insert_query = f"""
            INSERT INTO {table_name} (ID, FIRST_NAME, LAST_NAME, EMAIL, SIGNUP_DATE, STATUS)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.executemany(insert_query, data)
        conn.commit()
        print(f"Successfully loaded {cursor.rowcount} rows into {table_name}.")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    records = extract_and_transform_csv("data/sample_customers.csv")
    load_to_snowflake(records, "STG_CUSTOMERS")
