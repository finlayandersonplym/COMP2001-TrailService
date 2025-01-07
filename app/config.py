import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class Config:
    DB_SERVER = os.getenv('DB_SERVER', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'YourDB')
    DB_USER = os.getenv('DB_USER', 'sa')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    AUTH_API_URL = os.getenv('AUTH_API_URL')
    
    # Example DSN with ODBC Driver for SQL Server
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
        f"?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
    )
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
