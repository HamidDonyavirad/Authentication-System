from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
from confy import DATABASE_URL

engine = create_engine(DATABASE_URL)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()