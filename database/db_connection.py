from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger

from config.settings import settings


engine = create_engine(settings.DATABASE_URL)
SessionMaker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

logger.add(
    "loguru.log",
    rotation="15 second"
)

def get_db():
    db = SessionMaker()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(engine)
    logger.info("table created")
