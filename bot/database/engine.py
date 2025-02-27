import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = f"sqlite:///{settings.BASE_DIR / 'sqlite.db'}"
engine = create_engine(url=url, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)
