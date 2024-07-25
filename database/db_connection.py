from sqlalchemy import create_engine, StaticPool, NullPool
from sqlalchemy.orm import sessionmaker, declarative_base
from loguru import logger

URL_DATABASE = "postgresql://postgres:abhi@localhost/crud"

engine = create_engine(URL_DATABASE, pool_size=10 ,)
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
