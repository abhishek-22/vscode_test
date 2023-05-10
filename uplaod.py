from google.cloud import storage, bigquery
import pandas as pd
import os

# Set up GCS client and bucket
storage_client = storage.Client()
bucket_name = 'your_bucket_name'
bucket = storage_client.get_bucket(bucket_name)

# Set up BigQuery client and dataset
bq_client = bigquery.Client()
dataset_id = 'your_dataset_id'
dataset_ref = bq_client.dataset(dataset_id)

# Define function to drop empty columns and upload to BigQuery
def upload_to_bq(filename):
    # Read CSV from GCS bucket into pandas dataframe
    blob = bucket.blob(filename)
    df = pd.read_csv(blob.download_as_text(), low_memory=False)
    
    # Drop empty columns from dataframe
    df = df.loc[:, ~df.isnull().all(axis=0)]
    
    # Set table name as filename (without extension)
    table_name = os.path.splitext(filename)[0]
    
    # Upload dataframe to BigQuery
    table_ref = dataset_ref.table(table_name)
    job_config = bigquery.LoadJobConfig(schema=list(df.columns))
    job = bq_client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # Wait for job to complete
    
    # Move file to "uploaded files" folder in GCS bucket
    uploaded_blob = bucket.blob('uploaded files/{}'.format(filename))
    blob.move(uploaded_blob)

# Loop through files in GCS bucket and upload to BigQuery
for blob in bucket.list_blobs():
    if blob.name.endswith('.csv'):
        upload_to_bq(blob.name)
