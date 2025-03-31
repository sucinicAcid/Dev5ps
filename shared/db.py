from sqlalchemy import create_engine
from shared.config import POSTGRES_URL

engine = create_engine(POSTGRES_URL)