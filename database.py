from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.orm import sessionmaker

SQLDATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLDATABASE_URL, 
    connect_args={"check_same_thread": False}
    )

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String)
    author = Column(String)
    date_posted = Column(String)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()