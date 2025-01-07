import pyodbc
from config import Config

# Establish connection using configuration
connection_string = (
    f"DRIVER=ODBC Driver 18 for SQL Server;"
    f"SERVER={Config.DB_SERVER};"
    f"DATABASE={Config.DB_NAME};"
    f"UID={Config.DB_USER};"
    f"PWD={Config.DB_PASSWORD};"
    "TrustServerCertificate=Yes;"
)

try:
    # Connect to the database
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    # Ensure the schema 'CW2' exists
    cursor.execute("IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'CW2') EXEC('CREATE SCHEMA CW2');")

    # Drop all tables
    drop_tables = """
    IF OBJECT_ID('CW2.TrailFeature', 'U') IS NOT NULL DROP TABLE CW2.TrailFeature;
    IF OBJECT_ID('CW2.Feature', 'U') IS NOT NULL DROP TABLE CW2.Feature;
    IF OBJECT_ID('CW2.Trail', 'U') IS NOT NULL DROP TABLE CW2.Trail;
    IF OBJECT_ID('CW2.[User]', 'U') IS NOT NULL DROP TABLE CW2.[User];
    """
    cursor.execute(drop_tables)

    # Create Trail table
    create_trail_table = """
    CREATE TABLE CW2.Trail (
        TrailID INT IDENTITY(1,1) PRIMARY KEY,
        TrailName NVARCHAR(255) NOT NULL,
        TrailSummary NVARCHAR(1000),
        TrailDescription NVARCHAR(2000),
        Difficulty NVARCHAR(50),
        Location NVARCHAR(255),
        Length FLOAT,
        ElevationGain FLOAT,
        RouteType NVARCHAR(100),
        OwnerID INT NOT NULL,
        Pt1_Lat FLOAT,
        Pt1_Long FLOAT,
        Pt1_Desc NVARCHAR(255),
        Pt2_Lat FLOAT,
        Pt2_Long FLOAT,
        Pt2_Desc NVARCHAR(255)
    );
    """

    # Create TrailFeature table
    create_trail_feature_table = """
    CREATE TABLE CW2.TrailFeature (
        TrailID INT NOT NULL,
        TrailFeatureID INT NOT NULL,
        PRIMARY KEY (TrailID, TrailFeatureID),
        FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID) ON DELETE CASCADE,
        FOREIGN KEY (TrailFeatureID) REFERENCES CW2.Feature(TrailFeatureID) ON DELETE CASCADE
    );
    """

    # Create Feature table
    create_feature_table = """
    CREATE TABLE CW2.Feature (
        TrailFeatureID INT IDENTITY(1,1) PRIMARY KEY,
        TrailFeature NVARCHAR(255) NOT NULL
    );
    """

    # Create User table
    create_user_table = """
    CREATE TABLE CW2.[User] (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        Email_address NVARCHAR(255) NOT NULL UNIQUE,
        Role NVARCHAR(50) NOT NULL,
        PasswordHash NVARCHAR(255) NOT NULL
    );
    """

    # Execute SQL to create tables
    cursor.execute(create_trail_table)
    cursor.execute(create_feature_table)
    cursor.execute(create_trail_feature_table)
    cursor.execute(create_user_table)

    # Commit the changes
    connection.commit()
    print("All tables created successfully.")

except pyodbc.Error as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
