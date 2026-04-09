from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('postgresql://postgres:0110@localhost:5432/delivery_db', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
