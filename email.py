from google.cloud import storage
from google.cloud import bigquery
import pandas as pd

# Set the credentials for Google Cloud
credentials = "path/to/credentials.json"
storage_client = storage.Client.from_service_account_json(credentials)
bigquery_client = bigquery.Client.from_service_account_json(credentials)

# Set the bucket name and folder names
bucket_name = "your-bucket-name"
source_folder = "source_folder"
backup_folder = "backup_folder"

# Set the table names
table_names = {
    "FB": "my_fb_table",
    "Linked": "my_linked_table",
    "twt": "my_twt_table",
    "inst": "my_inst_table"
}

# Get the list of all files in the source folder that match the pattern
blob_list = storage_client.list_blobs(bucket_name, prefix=source_folder)
files = [blob.name for blob in blob_list if ".csv" in blob.name and any(s in blob.name for s in ["FB", "Linked", "twt", "inst"])]

# Load each file into a pandas dataframe and push it to BigQuery
for file in files:
    # Load the CSV file into a pandas dataframe
    blob = storage_client.bucket(bucket_name).get_blob(file)
    df = pd.read_csv(blob.download_as_text())

    # Get the table name based on the file name
    table_name = next((name for keyword, name in table_names.items() if keyword in file), None)
    if not table_name:
        continue

    # Create the table in BigQuery
    dataset_id = "your_dataset_id"
    dataset_ref = bigquery_client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_name)
    schema = [bigquery.SchemaField(name, "STRING") for name in df.columns]

    try:
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)  # create the table
    except:
        table = bigquery_client.get_table(table_ref)  # if the table already exists, get the table instead

    # Load the data into the table
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = "WRITE_TRUNCATE"  # overwrite the table if it already exists
    job = bigquery_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()

    # Move the file to the backup folder
    source_blob = storage_client.bucket(bucket_name).blob(file)
    destination_blob = storage_client.bucket(bucket_name).rename_blob(source_blob, backup_folder + "/" + file.split("/")[-1])
