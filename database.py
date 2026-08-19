import sqlite3
import os


# ==========================================
# DATABASE FILE
# ==========================================

DATABASE = "hospital.db"


# ==========================================
# MAHARASHTRA DISTRICTS
# ==========================================

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


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db_connection():

    conn = sqlite3.connect(
        DATABASE,
        timeout=30,
        check_same_thread=False
    )

    conn.row_factory = sqlite3.Row

    return conn


# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    conn = get_db_connection()

    cursor = conn.cursor()

    # --------------------------------------
    # USERS TABLE
    # --------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
    """)


    # --------------------------------------
    # HOSPITALS TABLE
    # --------------------------------------

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


# ==========================================
# ADD SAMPLE HOSPITALS
# ==========================================

def add_sample_hospitals():

    conn = get_db_connection()

    cursor = conn.cursor()


    # Check whether hospitals already exist

    cursor.execute("SELECT COUNT(*) FROM hospitals")

    count = cursor.fetchone()[0]


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


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def initialize_database():

    create_tables()

    add_sample_hospitals()


# ==========================================
# RUN DIRECTLY
# ==========================================

if __name__ == "__main__":

    initialize_database()

    print("Database created successfully!")
