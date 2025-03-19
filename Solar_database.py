import os 
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from appdirs import user_data_dir

# Get the user-specific directory for storing application data
app_name = "KivySolarApp"
app_author = "YourName"
data_dir = user_data_dir("Solac", "Ohere, Kingsley Ohere")

# Ensure the directory exists
os.makedirs(data_dir, exist_ok=True)

# Define the path to the database file
db_path = os.path.join(data_dir, 'files.db')

# Print the database path for debugging
print(f"Database path: {db_path}")

Base = declarative_base()
engine = create_engine(f'sqlite:///{db_path}')
Session = sessionmaker(bind=engine)
session = Session()

class File(Base):
    __tablename__ = 'files'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)

Base.metadata.create_all(engine)

def insert_file(name, path):
    new_file = File(name=name, path=path)
    session.add(new_file)
    session.commit()

def get_files():
    return session.query(File).all()