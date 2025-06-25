from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy
from src.api.config import settings

# credentials from environment variables
db_user = settings.DB_USER
db_pass = settings.DB_PASS_SECRET
db_name = settings.DB_NAME
instance_connection_name = settings.INSTANCE_CONNECTION_NAME


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
        future=True,
    ),
)

# pool = sqlalchemy.create_engine(
#     f"postgresql+pg8000://{db_user}:{db_pass}@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}",
#     future=True,
#     echo=False,
# )