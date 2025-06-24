import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

# credentials from environment variables
db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS_SECRET"]
db_name = os.environ["DB_NAME"]
instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

connector = Connector()

# create a connection pool
pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=lambda: connector.connect(
        instance_connection_name,
        "pg8000",
        user=db_user,
        password=db_pass,
        db=db_name,
        ip_type=IPTypes.PRIVATE,
    ),
)

# pool = sqlalchemy.create_engine(
#     f"postgresql+pg8000://{db_user}:{db_pass}@localhost:xxxx/{db_name}"
# )