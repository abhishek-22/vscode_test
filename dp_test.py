from google.cloud import datacatalog_v1beta1
from google.cloud import bigquery

# Set up BigQuery client
bigquery_client = bigquery.Client()

# Set up Data Catalog client
datacatalog_client = datacatalog_v1beta1.DataCatalogClient()

# Set up variables for the business glossary and business term
glossary_id = 'your-glossary-id'
term_id = 'your-term-id'

# Set up variables for the BigQuery table and column
table_project_id = 'your-project-id'
table_dataset_id = 'your-dataset-id'
table_name = 'your-table-name'
column_name = 'your-column-name'

# Look up the Data Plex resources for the glossary and term
glossary_resource_name = datacatalog_client.glossary_path(
    project='your-project-id',
    location='us-central1',
    glossary=glossary_id)
term_resource_name = datacatalog_client.term_path(
    project='your-project-id',
    location='us-central1',
    glossary=glossary_id,
    taxonomy='data_plex',
    term=term_id)

# Look up the BigQuery table and column
table_reference = bigquery_client.dataset(table_dataset_id, project=table_project_id).table(table_name)
table = bigquery_client.get_table(table_reference)
column = next((c for c in table.schema if c.name == column_name), None)

# Create the BusinessMetadata entry for the column in Data Catalog
metadata = datacatalog_v1beta1.types.BusinessMetadata()
metadata.entries['glossary_term'] = datacatalog_v1beta1.types.TypedValue(
    string_value=term_resource_name)
datacatalog_client.update_entry(name=column_name, business_metadata=metadata)

print(f'Successfully assigned the business term "{term_id}" in the glossary "{glossary_id}" to the column "{column_name}" in the table "{table_name}".')
