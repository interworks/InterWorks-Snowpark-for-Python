
# Build Snowpipe ingest manager for Snowflake

## Import snowpipe module
from snowflake.ingest import SimpleIngestManager
from snowflake.ingest import StagedFile

## Define function to build a snowpipe ingest manager
def build_snowpipe_ingest_manager_from_connection_parameters(
      snowflake_connection_parameters: dict
    , target_pipe_name: str = None
  ):

  snowpipe_ingest_manager = SimpleIngestManager(
      account=snowflake_connection_parameters["account"]
    , host=f'{snowflake_connection_parameters["account"]}.snowflakecomputing.com'
    , user=snowflake_connection_parameters["user"]
    , pipe=target_pipe_name
    , private_key=snowflake_connection_parameters["private_key"]
  )

  return snowpipe_ingest_manager

## Define function to build a snowpipe ingest manager
## leveraging a locally-stored JSON file
## containing Snowflake connection parameters
def build_snowpipe_ingest_manager_via_parameters_json(
      snowflake_connection_parameters_json_filepath: str = 'snowflake_connection_parameters.json'
    , target_pipe_name: str = None
  ):

  from .leverage_snowflake_connection_parameters_dictionary import import_snowflake_connection_parameters_from_local_json

  snowflake_connection_parameters = import_snowflake_connection_parameters_from_local_json(snowflake_connection_parameters_json_filepath, private_key_output_format = 'snowpipe')

  snowpipe_ingest_manager = build_snowpipe_ingest_manager_from_connection_parameters(snowflake_connection_parameters, target_pipe_name)

  return snowpipe_ingest_manager

## Define function to build a snowpipe ingest manager
## leveraging a Streamlit secrets file
## containing Snowflake connection parameters
def build_snowpipe_ingest_manager_via_streamlit_secrets(
    target_pipe_name: str = None
  ):

  from .leverage_snowflake_connection_parameters_dictionary import import_snowflake_connection_parameters_from_streamlit_secrets

  snowflake_connection_parameters = import_snowflake_connection_parameters_from_streamlit_secrets(private_key_output_format = 'snowpipe')

  snowpipe_ingest_manager = build_snowpipe_ingest_manager_from_connection_parameters(snowflake_connection_parameters, target_pipe_name)

  return snowpipe_ingest_manager

## Define function to build a snowpipe ingest manager
## leveraging environment variables
## containing Snowflake connection parameters
def build_snowpipe_ingest_manager_via_environment_variables(
    target_pipe_name: str = None
  ):

  from .leverage_snowflake_connection_parameters_dictionary import import_snowflake_connection_parameters_from_environment_variables

  snowflake_connection_parameters = import_snowflake_connection_parameters_from_environment_variables(private_key_output_format = 'snowpipe')

  snowpipe_ingest_manager = build_snowpipe_ingest_manager_from_connection_parameters(snowflake_connection_parameters, target_pipe_name)

  return snowpipe_ingest_manager

## Define function to build a snowpipe ingest manager
## leveraging an inbound dictionary argument
## containing Snowflake connection parameters
def build_snowpipe_ingest_manager_via_parameters_object(
      imported_connection_parameters: dict
    , target_pipe_name: str = None
  ):

  '''
  imported_connection_parameters is expected in the following format:
  {
    "account": "<account>[.<region>][.<cloud provider>]",
    "user": "<username>",
    "default_role" : "<default role>", // Enter "None" if not required
    "default_warehouse" : "<default warehouse>", // Enter "None" if not required
    "default_database" : "<default database>", // Enter "None" if not required
    "default_schema" : "<default schema>", // Enter "None" if not required
    "private_key_path" : "path\\to\\private\\key", // Enter "None" if not required, in which case private key plain text or password will be used
    "private_key_plain_text" : "-----BEGIN PRIVATE KEY-----\nprivate\nkey\nas\nplain\ntext\n-----END PRIVATE KEY-----", // Not best practice but may be required in some cases. Ignored if private key path is provided
    "private_key_passphrase" : "<passphrase>", // Enter "None" if not required
    "password" : "<password>" // Enter "None" if not required, ignored if private key path or private key plain text is provided
  }
  '''

  from .leverage_snowflake_connection_parameters_dictionary import retrieve_snowflake_connection_parameters

  snowflake_connection_parameters = retrieve_snowflake_connection_parameters(imported_connection_parameters, private_key_output_format = 'snowpipe')

  snowpipe_ingest_manager = build_snowpipe_ingest_manager_from_connection_parameters(snowflake_connection_parameters, target_pipe_name)

  return snowpipe_ingest_manager

## Define function to build a snowpipe ingest manager
## leveraging environment variables
## containing Snowflake connection parameters,
## with the private key stored in 
## an Azure secrets vault.
## Only works if corresponding Azure packages are installed
def build_snowpipe_ingest_manager_using_stored_private_key_in_azure_secrets_vault(
      target_pipe_name: str = None
    , snowflake_user: str = None
    , snowflake_account: str = None
    , snowflake_default_role: str = None
    , snowflake_default_warehouse: str = None
    , snowflake_default_database: str = None
    , snowflake_default_schema: str = None
  ):

  ### Import required modules
  from .azure_secrets_vault_functions import retrieve_secret_from_azure_secrets
  from .leverage_snowflake_connection_parameters_dictionary import retrieve_snowflake_connection_parameters
  import os

  ### Retrieve any missing inputs from environment variables
  if snowflake_user is None or len(snowflake_user) == 0:
    snowflake_user = os.getenv("SNOWFLAKE_USER")
  if snowflake_account is None or len(snowflake_account) == 0:
    snowflake_account = os.getenv("SNOWFLAKE_ACCOUNT")
  if snowflake_default_role is None or len(snowflake_default_role) == 0:
    snowflake_default_role = os.getenv("SNOWFLAKE_DEFAULT_ROLE")
  if snowflake_default_warehouse is None or len(snowflake_default_warehouse) == 0:
    snowflake_default_warehouse = os.getenv("SNOWFLAKE_DEFAULT_WAREHOUSE")
  if snowflake_default_database is None or len(snowflake_default_database) == 0:
    snowflake_default_database = os.getenv("SNOWFLAKE_DEFAULT_DATABASE")
  if snowflake_default_schema is None or len(snowflake_default_schema) == 0:
    snowflake_default_schema = os.getenv("SNOWFLAKE_DEFAULT_SCHEMA")
  
  ### Create name of desired secret
  private_key_secret_name = f"{snowflake_user}__private_key"

  ### Retrieve private key for user from Azure Secrets Vault
  private_key = retrieve_secret_from_azure_secrets(private_key_secret_name)
  
  ### Define imported connection parameters using environment variables
  ### whilst targeting specific account
  imported_connection_parameters = {
      "account" : snowflake_account
    , "user" : snowflake_user
    , "default_role" : snowflake_default_role
    , "default_warehouse" : snowflake_default_warehouse
    , "default_database" : snowflake_default_database
    , "default_schema" : snowflake_default_schema
    , "private_key_plain_text" : private_key
  }

  ### Populate snowflake_connection_parameters from imported_connection_parameters
  snowflake_connection_parameters = retrieve_snowflake_connection_parameters(imported_connection_parameters, private_key_output_format = 'snowpipe')

  snowpipe_ingest_manager = build_snowpipe_ingest_manager_from_connection_parameters(snowflake_connection_parameters, target_pipe_name)

  return snowpipe_ingest_manager

## Define function to trigger a snowpipe ingestion
def trigger_snowpipe_ingestion(
      snowpipe_ingest_manager: SimpleIngestManager
    , relative_file_path: str = None
  ):
  """
  Download dataframe from Azure Blob Storage for given url
  Keyword arguments:
  snowpipe_ingest_manager -- the snowpipe ingest manager object that connects to the destination Snowflake pipe
  relative_file_path -- the file path of the file to ingest within blob storage, relative to the Snowflake stage target directory (default None)

  eg: retrieve_snowpipe_ingest_manager(snowpipe_ingest_manager=my_snowpipe_ingest_manager, relative_file_path="my/target/file/path.csv.gz")
  """
  try:

    if all([snowpipe_ingest_manager]):
          
      staged_file_list = []
      staged_file_list.append(
        StagedFile(relative_file_path, None)  # file size is optional but recommended, pass None if not available
      )
      snowpipe_response = snowpipe_ingest_manager.ingest_files(staged_file_list)

      # This means Snowflake has received file and will start loading
      assert(snowpipe_response['responseCode'] == 'SUCCESS')

    else:
      raise ValueError('Aborting Snowpipe connnection as function input is missing')

  except Exception as e:
    raise ValueError(e)
