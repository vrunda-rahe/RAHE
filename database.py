import sqlite3
import os


# =========================================================
# DATABASE FILE
# =========================================================

DATABASE = "hospital.db"


# =========================================================
# MAHARASHTRA DISTRICTS
# =========================================================

MAHARASHTRA_DISTRICTS = [
    "Ahmednagar",
    "Akola",
    "Amravati",
    "Aurangabad",
    "Beed",
    "Bhandara",
    "Buldhana",
    "Chandrapur",
    "Dhule",
    "Gadchiroli",
    "Gondia",
    "Hingoli",
    "Jalgaon",
    "Jalna",
    "Kolhapur",
    "Latur",
    "Mumbai City",
    "Mumbai Suburban",
    "Nagpur",
    "Nanded",
    "Nandurbar",
    "Nashik",
    "Osmanabad",
    "Palghar",
    "Parbhani",
    "Pune",
    "Raigad",
    "Ratnagiri",
    "Sangli",
    "Satara",
    "Sindhudurg",
    "Solapur",
    "Thane",
    "Wardha",
    "Washim",
    "Yavatmal"
]


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    conn = sqlite3.connect(
        DATABASE,
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    conn = get_db_connection()
    cursor = conn.cursor()

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)

    # -----------------------------------------------------
    # HOSPITALS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospitals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hospital_name TEXT NOT NULL,

            address TEXT,

            city TEXT,

            village TEXT,

            district TEXT,

            contact TEXT,

            general_beds INTEGER DEFAULT 0,

            icu_beds INTEGER DEFAULT 0,

            emergency_beds INTEGER DEFAULT 0,

            latitude REAL,

            longitude REAL,

            username TEXT,

            password TEXT

        )
    """)

    conn.commit()

    conn.close()


# =========================================================
# UPDATE OLD DATABASE
# =========================================================
# जर जुना hospital.db असेल तर नवीन columns automatically
# add होतील.
# =========================================================

def update_database_columns():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(hospitals)")

    columns = [row["name"] for row in cursor.fetchall()]

    # -----------------------------------------------------
    # Village
    # -----------------------------------------------------

    if "village" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN village TEXT
        """)

    # -----------------------------------------------------
    # District
    # -----------------------------------------------------

    if "district" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN district TEXT
        """)

    # -----------------------------------------------------
    # City
    # -----------------------------------------------------

    if "city" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN city TEXT
        """)

    # -----------------------------------------------------
    # Contact
    # -----------------------------------------------------

    if "contact" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN contact TEXT
        """)

    # -----------------------------------------------------
    # General Beds
    # -----------------------------------------------------

    if "general_beds" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN general_beds INTEGER DEFAULT 0
        """)

    # -----------------------------------------------------
    # ICU Beds
    # -----------------------------------------------------

    if "icu_beds" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN icu_beds INTEGER DEFAULT 0
        """)

    # -----------------------------------------------------
    # Emergency Beds
    # -----------------------------------------------------

    if "emergency_beds" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN emergency_beds INTEGER DEFAULT 0
        """)

    # -----------------------------------------------------
    # Latitude
    # -----------------------------------------------------

    if "latitude" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN latitude REAL
        """)

    # -----------------------------------------------------
    # Longitude
    # -----------------------------------------------------

    if "longitude" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN longitude REAL
        """)

    # -----------------------------------------------------
    # Username
    # -----------------------------------------------------

    if "username" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN username TEXT
        """)

    # -----------------------------------------------------
    # Password
    # -----------------------------------------------------

    if "password" not in columns:

        cursor.execute("""
            ALTER TABLE hospitals
            ADD COLUMN password TEXT
        """)

    conn.commit()

    conn.close()


# =========================================================
# CREATE SEARCH INDEXES
# =========================================================
# District / City / Village search fast करण्यासाठी
# =========================================================

def create_indexes():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hospitals_district
        ON hospitals(district)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hospitals_city
        ON hospitals(city)
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_hospitals_village
        ON hospitals(village)
    """)

    conn.commit()

    conn.close()


# =========================================================
# ADD SAMPLE HOSPITALS
# =========================================================

def add_sample_hospitals():

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM hospitals")

    count = cursor.fetchone()[0]

    # -----------------------------------------------------
    # Sample hospitals only if database is empty
    # -----------------------------------------------------

    if count == 0:

        hospitals = [

            (
                "City Care Hospital",
                "Baner Road",
                "Pune",
                "Baner",
                "Pune",
                "9876543210",
                25,
                8,
                5,
                18.5590,
                73.7868,
                "citycare",
                "1234"
            ),

            (
                "LifeLine Hospital",
                "Camp Area, Pune",
                "Pune",
                "Camp",
                "Pune",
                "9876543211",
                30,
                10,
                7,
                18.5018,
                73.8780,
                "lifeline",
                "1234"
            ),

            (
                "Nagpur Life Hospital",
                "Wardha Road",
                "Nagpur",
                "Wardha Road",
                "Nagpur",
                "9876545678",
                30,
                10,
                7,
                21.1458,
                79.0882,
                "nagpurlife",
                "1234"
            ),

            (
                "Nashik Care Hospital",
                "College Road",
                "Nashik",
                "College Road",
                "Nashik",
                "9876534567",
                35,
                12,
                6,
                20.0059,
                73.7900,
                "nashikcare",
                "1234"
            ),

            (
                "Sahyadri Emergency Hospital",
                "Hadapsar",
                "Pune",
                "Hadapsar",
                "Pune",
                "9876512345",
                40,
                15,
                10,
                18.5146,
                73.8344,
                "sahyadri",
                "1234"
            ),

            (
                "Solapur Emergency Hospital",
                "Hotgi Road",
                "Solapur",
                "Hotgi Road",
                "Solapur",
                "9876523456",
                20,
                6,
                4,
                17.6599,
                75.9064,
                "solapur",
                "1234"
            )

        ]

        cursor.executemany("""
            INSERT INTO hospitals (

                hospital_name,
                address,
                city,
                village,
                district,
                contact,
                general_beds,
                icu_beds,
                emergency_beds,
                latitude,
                longitude,
                username,
                password

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, hospitals)

        conn.commit()

    conn.close()


# =========================================================
# VILLAGE SEARCH FUNCTION
# =========================================================
# District + City + Village तिन्हीमध्ये hospital शोधता येईल.
# =========================================================

def search_hospitals(district=None, location=None, bed_type=None):

    conn = get_db_connection()

    query = """
        SELECT *
        FROM hospitals
        WHERE 1 = 1
    """

    params = []

    # -----------------------------------------------------
    # DISTRICT SEARCH
    # -----------------------------------------------------

    if district and district.strip():

        query += """
            AND LOWER(TRIM(district)) = LOWER(TRIM(?))
        """

        params.append(district.strip())

    # -----------------------------------------------------
    # CITY / VILLAGE SEARCH
    # -----------------------------------------------------

    if location and location.strip():

        query += """
            AND (
                LOWER(TRIM(city)) LIKE LOWER(TRIM(?))
                OR LOWER(TRIM(village)) LIKE LOWER(TRIM(?))
                OR LOWER(TRIM(address)) LIKE LOWER(TRIM(?))
            )
        """

        search_value = "%" + location.strip() + "%"

        params.append(search_value)
        params.append(search_value)
        params.append(search_value)

    # -----------------------------------------------------
    # BED TYPE SEARCH
    # -----------------------------------------------------

    if bed_type:

        bed_type = bed_type.lower().strip()

        if bed_type == "general":

            query += """
                AND general_beds > 0
            """

        elif bed_type == "icu":

            query += """
                AND icu_beds > 0
            """

        elif bed_type == "emergency":

            query += """
                AND emergency_beds > 0
            """

    # -----------------------------------------------------
    # ORDER
    # -----------------------------------------------------

    query += """
        ORDER BY hospital_name ASC
    """

    hospitals = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return hospitals


# =========================================================
# GET ALL HOSPITALS
# =========================================================

def get_all_hospitals():

    conn = get_db_connection()

    hospitals = conn.execute("""
        SELECT *
        FROM hospitals
        ORDER BY hospital_name ASC
    """).fetchall()

    conn.close()

    return hospitals


# =========================================================
# GET HOSPITAL BY ID
# =========================================================

def get_hospital_by_id(hospital_id):

    conn = get_db_connection()

    hospital = conn.execute("""
        SELECT *
        FROM hospitals
        WHERE id = ?
    """, (hospital_id,)).fetchone()

    conn.close()

    return hospital


# =========================================================
# UPDATE HOSPITAL BEDS
# =========================================================

def update_hospital_beds(
    hospital_id,
    general_beds,
    icu_beds,
    emergency_beds
):

    conn = get_db_connection()

    conn.execute("""
        UPDATE hospitals

        SET
            general_beds = ?,
            icu_beds = ?,
            emergency_beds = ?

        WHERE id = ?

    """, (
        general_beds,
        icu_beds,
        emergency_beds,
        hospital_id
    ))

    conn.commit()

    conn.close()


# =========================================================
# ADD NEW HOSPITAL
# =========================================================

def add_hospital(
    hospital_name,
    address,
    city,
    village,
    district,
    contact,
    general_beds=0,
    icu_beds=0,
    emergency_beds=0,
    latitude=None,
    longitude=None,
    username=None,
    password=None
):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO hospitals (

            hospital_name,
            address,
            city,
            village,
            district,
            contact,
            general_beds,
            icu_beds,
            emergency_beds,
            latitude,
            longitude,
            username,
            password

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

    """, (

        hospital_name,
        address,
        city,
        village,
        district,
        contact,
        general_beds,
        icu_beds,
        emergency_beds,
        latitude,
        longitude,
        username,
        password

    ))

    conn.commit()

    hospital_id = cursor.lastrowid

    conn.close()

    return hospital_id


# =========================================================
# UPDATE HOSPITAL
# =========================================================

def update_hospital(
    hospital_id,
    hospital_name,
    address,
    city,
    village,
    district,
    contact,
    latitude=None,
    longitude=None
):

    conn = get_db_connection()

    conn.execute("""
        UPDATE hospitals

        SET
            hospital_name = ?,
            address = ?,
            city = ?,
            village = ?,
            district = ?,
            contact = ?,
            latitude = ?,
            longitude = ?

        WHERE id = ?

    """, (

        hospital_name,
        address,
        city,
        village,
        district,
        contact,
        latitude,
        longitude,
        hospital_id

    ))

    conn.commit()

    conn.close()


# =========================================================
# DELETE HOSPITAL
# =========================================================

def delete_hospital(hospital_id):

    conn = get_db_connection()

    conn.execute("""
        DELETE FROM hospitals
        WHERE id = ?
    """, (hospital_id,))

    conn.commit()

    conn.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    # 1. Create tables
    create_tables()

    # 2. Update old database columns
    update_database_columns()

    # 3. Create indexes
    create_indexes()

    # 4. Add sample hospitals
    add_sample_hospitals()


# =========================================================
# RUN DIRECTLY
# =========================================================

if __name__ == "__main__":

    initialize_database()

    print("========================================")
    print("Hospital Database Ready!")
    print("========================================")
    print("Database:", DATABASE)
    print("Village search: ENABLED")
    print("District search: ENABLED")
    print("City search: ENABLED")
    print("Bed search: ENABLED")
    print("========================================")