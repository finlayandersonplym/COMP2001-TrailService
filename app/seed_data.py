import pyodbc

from app.models import User
from config import Config

connection_string = (f"DRIVER=ODBC Driver 18 for SQL Server;SERVER={Config.DB_SERVER};DATABASE={Config.DB_NAME};UID={Config.DB_USER};PWD={Config.DB_PASSWORD};TrustServerCertificate=Yes;")

try:
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    raw_user_data = [
        ("grace@plymouth.ac.uk", "admin", "ISAD123!"),
        ("tim@plymouth.ac.uk", "user", "COMP2001!"),
        ("ada@plymouth.ac.uk", "user", "insecurePassword")
    ]

    # Prepare user data with hashed passwords using set_password
    user_data = []
    for email, role, password in raw_user_data:
        user = User(Email_address=email, Role=role)
        user.set_password(password)  
        user_data.append((user.Email_address, user.Role, user.PasswordHash))

    # Bulk insert into the database
    cursor.executemany(
        "INSERT INTO CW2.[User] (Email_address, Role, PasswordHash) VALUES (?, ?, ?)",
        user_data
    )

    feature_data = [
        ("Waterfront View",),
        ("Forest Trail",),
        ("Historical Site",),
        ("Mountain Path",)
    ]
    cursor.executemany("INSERT INTO CW2.Feature (TrailFeature) VALUES (?)", feature_data)

    trail_data = [
        (
            "Plymouth Waterfront and Plymouth Hoe Circular",
            "Enjoy this 4.8-km loop trail near Plymouth, Devon. Generally considered an easy route...",
            "A scenic trail along the Plymouth Hoe with historical significance.",
            "Easy",
            "Plymouth, Devon, England",
            4.8,
            83,
            "Loop",
            1,              # OwnerID
            50.3646,
            -4.1431,
            "Start point by the Hoe",
            50.3692,
            -4.1427,
            "End point at Barbican"
        ),
        (
            "Dartmoor Tors and Moors Circular",
            "A scenic 10-km circular trail across Dartmoor's tors and moors. Rated moderate...",
            "A challenging route across scenic moorland and rocky tors.",
            "Moderate",
            "Dartmoor, Devon, England",
            10.0,
            350,
            "Loop",
            2,              # OwnerID
            50.5781,
            -3.9235,
            "Start point at Haytor",
            50.5843,
            -3.9112,
            "End point at Hound Tor"
        )
    ]

    cursor.executemany(
        """
        INSERT INTO CW2.Trail (
            TrailName,
            TrailSummary,
            TrailDescription,
            Difficulty,
            Location,
            Length,
            ElevationGain,
            RouteType,
            OwnerID,
            Pt1_Lat,
            Pt1_Long,
            Pt1_Desc,
            Pt2_Lat,
            Pt2_Long,
            Pt2_Desc
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        trail_data
    )

    trail_feature_data = [
        (1, 1),  # TrailID=1, FeatureID=1
        (1, 3),  # TrailID=1, FeatureID=3
        (2, 2),  # TrailID=2, FeatureID=2
        (2, 4)   # TrailID=2, FeatureID=4
    ]
    cursor.executemany(
        "INSERT INTO CW2.TrailFeature (TrailID, TrailFeatureID) VALUES (?, ?)",
        trail_feature_data
)

    connection.commit()
    print("Fake data inserted successfully.")

except pyodbc.Error as e:
    print(f"Error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()
