from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for,
    flash,
    send_from_directory
)

import sqlite3
import os
import math

from werkzeug.utils import secure_filename


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = "rahe_secret_key_2026"


# =========================================================
# PATH SETTINGS
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DB_PATH = os.path.join(
    BASE_DIR,
    "rahe.db"
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.config["MAX_CONTENT_LENGTH"] = (
    5 * 1024 * 1024
)


# =========================================================
# MAHARASHTRA DISTRICTS
# =========================================================

MAHARASHTRA_DISTRICTS = [
    "Ahmednagar",
    "Akola",
    "Amravati",
    "Beed",
    "Bhandara",
    "Buldhana",
    "Chandrapur",
    "Chhatrapati Sambhajinagar",
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
    "Osmanabad (Dharashiv)",
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
# DISTRICT → CITY / VILLAGE
# =========================================================

MAHARASHTRA_LOCATIONS = {

    "Ahmednagar": [
        "Ahmednagar", "Akole", "Jamkhed", "Karjat",
        "Kopargaon", "Nevasa", "Parner", "Pathardi",
        "Rahata", "Rahuri", "Sangamner", "Shevgaon",
        "Shrigonda", "Shrirampur"
    ],

    "Akola": [
        "Akola", "Akot", "Balapur", "Barshitakli",
        "Murtizapur", "Patur", "Telhara"
    ],

    "Amravati": [
        "Amravati", "Achalpur", "Anjangaon Surji",
        "Bhatkuli", "Chandur Bazar", "Chandur Railway",
        "Chikhaldara", "Daryapur", "Dhamangaon Railway",
        "Dharni", "Morshi", "Nandgaon Khandeshwar",
        "Teosa", "Warud"
    ],

    "Beed": [
        "Beed", "Ambajogai", "Ashti", "Dharur",
        "Georai", "Kaij", "Manjlegaon", "Majalgaon",
        "Parli", "Patoda", "Shirur Kasar", "Wadwani"
    ],

    "Bhandara": [
        "Bhandara", "Andhalgaon", "Lakhani", "Lakhni",
        "Mohadi", "Pauni", "Sakoli", "Tumsar"
    ],

    "Buldhana": [
        "Buldhana", "Chikhli", "Deulgaon Raja",
        "Jalgaon Jamod", "Khamgaon", "Lonar",
        "Malkapur", "Mehkar", "Motala", "Nandura",
        "Shegaon", "Sindkhed Raja"
    ],

    "Chandrapur": [
        "Chandrapur", "Ballarpur", "Bhadravati",
        "Brahmapuri", "Chimur", "Gondpipri", "Jiwati",
        "Korpana", "Mul", "Nagbhir", "Pombhurna",
        "Rajura", "Saoli", "Sindewahi", "Warora"
    ],

    "Chhatrapati Sambhajinagar": [
        "Chhatrapati Sambhajinagar",
        "Aurangabad",
        "Kannad",
        "Khultabad",
        "Paithan",
        "Phulambri",
        "Sillod",
        "Soegaon",
        "Vaijapur",
        "Gangapur"
    ],

    "Dhule": [
        "Dhule", "Shirpur", "Shindkheda", "Sakri"
    ],

    "Gadchiroli": [
        "Gadchiroli", "Aheri", "Armori", "Bhamragad",
        "Chamorshi", "Dhanora", "Desaiganj",
        "Etapalli", "Korchi", "Kurkheda",
        "Mulchera", "Sironcha"
    ],

    "Gondia": [
        "Gondia", "Amgaon", "Arjuni Morgaon", "Deori",
        "Goregaon", "Sadak Arjuni", "Salekasa", "Tirora"
    ],

    "Hingoli": [
        "Hingoli", "Aundha Nagnath", "Basmath",
        "Kalamnuri", "Sengaon"
    ],

    "Jalgaon": [
        "Jalgaon", "Amalner", "Bhadgaon", "Bhusawal",
        "Bodwad", "Chalisgaon", "Chopda", "Dharangaon",
        "Erandol", "Jamner", "Muktainagar", "Pachora",
        "Parola", "Raver", "Yawal"
    ],

    "Jalna": [
        "Jalna", "Ambad", "Badnapur", "Bhokardan",
        "Ghansawangi", "Jafrabad", "Mantha", "Partur"
    ],

    "Kolhapur": [
        "Kolhapur", "Ajra", "Bhudargad", "Chandgad",
        "Gadhinglaj", "Gaganbawada", "Hatkanangale",
        "Kagal", "Karvir", "Panhala", "Radhanagari",
        "Shahuwadi", "Shirol"
    ],

    "Latur": [
        "Latur", "Ausa", "Ahmedpur", "Chakur", "Deoni",
        "Jalkot", "Nilanga", "Renapur",
        "Shirur Anantpal", "Udgir"
    ],

    "Mumbai City": [
        "Mumbai", "Fort", "Colaba", "Byculla",
        "Dadar", "Marine Lines", "Masjid", "CST"
    ],

    "Mumbai Suburban": [
        "Andheri", "Bandra", "Borivali", "Chembur",
        "Ghatkopar", "Jogeshwari", "Kurla", "Malad",
        "Mulund", "Powai", "Santacruz", "Vikhroli",
        "Vile Parle"
    ],

    "Nagpur": [
        "Nagpur", "Bhiwapur", "Hingna", "Kalmeshwar",
        "Kamthi", "Katol", "Kuhi", "Mauda", "Narkhed",
        "Parseoni", "Ramtek", "Savner", "Umred"
    ],

    "Nanded": [
        "Nanded", "Ardhapur", "Bhokar", "Biloli",
        "Deglur", "Dharmabad", "Hadgaon",
        "Himayatnagar", "Kandhar", "Kinwat", "Loha",
        "Mahur", "Mudkhed", "Mukhed", "Naigaon"
    ],

    "Nandurbar": [
        "Nandurbar", "Akkalkuwa", "Akrani",
        "Navapur", "Shahada", "Taloda"
    ],

    "Nashik": [
        "Nashik", "Baglan", "Chandwad", "Deola",
        "Dindori", "Igatpuri", "Kalwan", "Malegaon",
        "Nandgaon", "Niphad", "Peint", "Sinnar",
        "Surgana", "Trimbakeshwar", "Yeola"
    ],

    "Osmanabad (Dharashiv)": [
        "Osmanabad", "Dharashiv", "Bhoom", "Kalamb",
        "Lohara", "Omerga", "Paranda", "Tuljapur",
        "Vashi", "Washi"
    ],

    "Palghar": [
        "Palghar", "Dahanu", "Jawhar", "Mokhada",
        "Talasari", "Vada", "Vasai", "Vikramgad"
    ],

    "Parbhani": [
        "Parbhani", "Gangakhed", "Jintur", "Manwath",
        "Manwat", "Palam", "Purna", "Pathri",
        "Sonpeth", "Sailu"
    ],

    "Pune": [
        "Pune", "Ambegaon", "Baramati", "Bhor",
        "Daund", "Haveli", "Indapur", "Junnar",
        "Khed", "Mawal", "Mulshi", "Purandar",
        "Shirur", "Velhe"
    ],

    "Raigad": [
        "Alibag", "Karjat", "Khalapur", "Mahad",
        "Mangaon", "Mhasla", "Murud", "Panvel",
        "Pen", "Poladpur", "Roha", "Shrivardhan",
        "Sudhagad", "Tala", "Uran"
    ],

    "Ratnagiri": [
        "Ratnagiri", "Chiplun", "Dapoli", "Guhagar",
        "Khed", "Lanja", "Mandangad", "Rajapur",
        "Sangameshwar"
    ],

    "Sangli": [
        "Sangli", "Atpadi", "Jat", "Kadegaon",
        "Kavathe Mahankal", "Khanapur", "Miraj",
        "Palus", "Shirala", "Tasgaon", "Walwa"
    ],

    "Satara": [
        "Satara", "Jaoli", "Karad", "Khandala",
        "Khatav", "Koregaon", "Mahabaleshwar",
        "Man", "Patan", "Phaltan", "Wai"
    ],

    "Sindhudurg": [
        "Kankavli", "Kudal", "Malvan", "Sawantwadi",
        "Deogad", "Dodamarg", "Vengurla",
        "Vaibhavwadi"
    ],

    "Solapur": [
        "Solapur", "Akkalkot", "Barshi", "Karmala",
        "Madha", "Malshiras", "Mangalwedha",
        "Mohol", "Pandharpur", "Sangola"
    ],

    "Thane": [
        "Thane", "Bhiwandi", "Kalyan", "Murbad",
        "Shahapur", "Ulhasnagar", "Ambernath"
    ],

    "Wardha": [
        "Wardha", "Arvi", "Ashti", "Deoli",
        "Hinganghat", "Karanja", "Samudrapur", "Seloo"
    ],

    "Washim": [
        "Washim", "Karanja", "Malegaon",
        "Mangrulpir", "Manora", "Risod"
    ],

    "Yavatmal": [
        "Yavatmal", "Arni", "Babhulgaon", "Darwha",
        "Digras", "Ghatanji", "Kalamb", "Kelapur",
        "Mahagaon", "Maregaon", "Ner", "Pusad",
        "Ralegaon", "Umarkhed", "Wani", "Zari-Jamani"
    ]
}


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    conn = sqlite3.connect(
        DB_PATH,
        timeout=30
    )

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# CHECK COLUMN
# =========================================================

def column_exists(
    conn,
    table,
    column
):

    rows = conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    return any(
        row["name"] == column
        for row in rows
    )


# =========================================================
# ADD COLUMN IF MISSING
# =========================================================

def add_column_if_missing(
    conn,
    table,
    column,
    definition
):

    if not column_exists(
        conn,
        table,
        column
    ):

        conn.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN {column} {definition}
            """
        )


# =========================================================
# CREATE TABLES
# =========================================================

def create_tables():

    conn = get_db_connection()

    # =====================================================
    # USERS
    # =====================================================

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            email TEXT UNIQUE NOT NULL,

            password TEXT NOT NULL

        )
        """
    )

    # =====================================================
    # HOSPITALS
    # =====================================================

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS hospitals (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            hospital_name TEXT NOT NULL,

            address TEXT,

            district TEXT,

            city TEXT,

            village TEXT,

            contact TEXT,

            general_beds INTEGER DEFAULT 0,

            icu_beds INTEGER DEFAULT 0,

            emergency_beds INTEGER DEFAULT 0,

            latitude REAL,

            longitude REAL,

            username TEXT UNIQUE,

            password TEXT

        )
        """
    )

    # =====================================================
    # ACCIDENTS
    # =====================================================

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS accidents (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            name TEXT,

            mobile TEXT,

            location TEXT,

            vehicle TEXT,

            description TEXT,

            image TEXT,

            status TEXT DEFAULT 'Pending',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    # =====================================================
    # SOS ALERTS
    # =====================================================

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sos_alerts (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id INTEGER,

            latitude REAL,

            longitude REAL,

            location TEXT,

            status TEXT DEFAULT 'Active',

            created_at TEXT DEFAULT CURRENT_TIMESTAMP

        )
        """
    )

    # =====================================================
    # HOSPITAL COMPATIBILITY
    # =====================================================

    hospital_columns = [

        ("address", "TEXT"),

        ("district", "TEXT"),

        ("city", "TEXT"),

        ("village", "TEXT"),

        ("contact", "TEXT"),

        ("general_beds", "INTEGER DEFAULT 0"),

        ("icu_beds", "INTEGER DEFAULT 0"),

        ("emergency_beds", "INTEGER DEFAULT 0"),

        ("latitude", "REAL"),

        ("longitude", "REAL"),

        ("username", "TEXT"),

        ("password", "TEXT")
    ]

    for column, definition in hospital_columns:

        add_column_if_missing(
            conn,
            "hospitals",
            column,
            definition
        )

    # =====================================================
    # ACCIDENT COMPATIBILITY
    # =====================================================

    accident_columns = [

        ("user_id", "INTEGER"),

        ("name", "TEXT"),

        ("mobile", "TEXT"),

        ("location", "TEXT"),

        ("vehicle", "TEXT"),

        ("description", "TEXT"),

        ("image", "TEXT"),

        ("status", "TEXT DEFAULT 'Pending'"),

        ("created_at", "TEXT")
    ]

    for column, definition in accident_columns:

        add_column_if_missing(
            conn,
            "accidents",
            column,
            definition
        )

    conn.commit()

    conn.close()


# =========================================================
# DEMO HOSPITALS
# =========================================================

def ensure_demo_hospitals():

    conn = get_db_connection()

    demo_hospitals = [

        (
            "City Care Hospital",
            "Main Road, Pune",
            "Pune",
            "Pune",
            "Pune",
            "0200000001",
            10,
            8,
            6,
            18.5204,
            73.8567,
            "citycare",
            "city123"
        ),

        (
            "LifeLine Hospital",
            "Station Road, Solapur",
            "Solapur",
            "Solapur",
            "Solapur",
            "0217000002",
            12,
            10,
            8,
            17.6599,
            75.9064,
            "lifeline",
            "life123"
        ),

        (
            "Sahyadri Emergency Hospital",
            "Baramati Road, Pune",
            "Pune",
            "Baramati",
            "Baramati",
            "0211200003",
            8,
            7,
            5,
            18.1500,
            74.5800,
            "sahyadri",
            "sahyadri123"
        ),

        (
            "Shree Hospital",
            "Nashik Road, Nashik",
            "Nashik",
            "Nashik",
            "Nashik",
            "0253000004",
            14,
            11,
            7,
            19.9975,
            73.7898,
            "shree",
            "shree123"
        ),

        (
            "District Emergency Hospital",
            "Civil Lines, Nagpur",
            "Nagpur",
            "Nagpur",
            "Nagpur",
            "0712000005",
            16,
            13,
            9,
            21.1458,
            79.0882,
            "district",
            "district123"
        ),

        (
            "Jeevan Jyoti Hospital",
            "Market Yard, Ahmednagar",
            "Ahmednagar",
            "Ahmednagar",
            "Ahmednagar",
            "0241000006",
            9,
            12,
            4,
            19.0948,
            74.7480,
            "jeevan",
            "jeevan123"
        )
    ]

    for hospital in demo_hospitals:

        hospital_name = hospital[0]

        existing = conn.execute(
            """
            SELECT id
            FROM hospitals
            WHERE hospital_name = ?
            """,
            (hospital_name,)
        ).fetchone()

        if not existing:

            conn.execute(
                """
                INSERT INTO hospitals
                (
                    hospital_name,
                    address,
                    district,
                    city,
                    village,
                    contact,
                    general_beds,
                    icu_beds,
                    emergency_beds,
                    latitude,
                    longitude,
                    username,
                    password
                )

                VALUES
                (
                    ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?
                )
                """,
                hospital
            )

    conn.commit()

    conn.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

create_tables()

ensure_demo_hospitals()


# =========================================================
# LOGIN CHECK
# =========================================================

def login_required():

    return "user_id" in session


def hospital_login_required():

    return "hospital_id" in session


def admin_login_required():

    return session.get("admin") is True


# =========================================================
# HOME
# =========================================================

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# =========================================================
# USER REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not name or not email or not password:

            flash(
                "Please fill all fields.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        conn = get_db_connection()

        try:

            conn.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password
                )

                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    password
                )
            )

            conn.commit()

            flash(
                "Registration successful. Please login.",
                "success"
            )

            return redirect(
                url_for("login")
            )

        except sqlite3.IntegrityError:

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        finally:

            conn.close()

    return render_template(
        "register.html"
    )


# =========================================================
# USER LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if not email or not password:

            flash(
                "Please enter email and password.",
                "error"
            )

            return redirect(
                url_for("login")
            )

        conn = get_db_connection()

        user = conn.execute(
            """
            SELECT *
            FROM users

            WHERE email = ?
            AND password = ?
            """,
            (
                email,
                password
            )
        ).fetchone()

        conn.close()

        if user:

            session["user_id"] = user["id"]

            session["name"] = user["name"]

            session["email"] = user["email"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "login.html"
    )


# =========================================================
# USER LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if not login_required():

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    total_hospitals = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM hospitals
        """
    ).fetchone()["c"]

    emergency_beds = conn.execute(
        """
        SELECT COALESCE(
            SUM(emergency_beds),
            0
        ) AS c
        FROM hospitals
        """
    ).fetchone()["c"]

    icu_beds = conn.execute(
        """
        SELECT COALESCE(
            SUM(icu_beds),
            0
        ) AS c
        FROM hospitals
        """
    ).fetchone()["c"]

    conn.close()

    return render_template(
        "dashboard.html",
        total_hospitals=total_hospitals,
        emergency_beds=emergency_beds,
        icu_beds=icu_beds
    )


# =========================================================
# HAVERSINE
# =========================================================

def haversine(
    lat1,
    lon1,
    lat2,
    lon2
):

    try:

        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)

    except (
        TypeError,
        ValueError
    ):

        return None

    radius = 6371.0

    p1 = math.radians(lat1)

    p2 = math.radians(lat2)

    dp = math.radians(
        lat2 - lat1
    )

    dl = math.radians(
        lon2 - lon1
    )

    a = (
        math.sin(dp / 2) ** 2
        +
        math.cos(p1)
        *
        math.cos(p2)
        *
        math.sin(dl / 2) ** 2
    )

    a = max(
        0,
        min(
            1,
            a
        )
    )

    return (
        radius
        *
        2
        *
        math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )
    )


# =========================================================
# TRAVEL TIME
# =========================================================

def calculate_travel_time(distance):

    if distance is None:

        return None

    average_speed = 45

    total_minutes = round(
        (distance / average_speed) * 60
    )

    if total_minutes < 1:

        total_minutes = 1

    hours = total_minutes // 60

    minutes = total_minutes % 60

    if hours > 0:

        if minutes > 0:

            return (
                f"{hours} hour "
                f"{minutes} minutes"
            )

        return f"{hours} hour"

    return f"{minutes} minutes"


# =========================================================
# NORMALIZE BED TYPE
# =========================================================

def normalize_bed_type(value):

    if not value:

        return ""

    value = value.strip().lower()

    value = value.replace(
        "-",
        " "
    )

    value = value.replace(
        "_",
        " "
    )

    if value in [
        "general",
        "general bed",
        "general beds"
    ]:

        return "General"

    if value in [
        "icu",
        "icu bed",
        "icu beds"
    ]:

        return "ICU"

    if value in [
        "emergency",
        "emergency bed",
        "emergency beds"
    ]:

        return "Emergency"

    if value in [
        "all",
        "all beds",
        "all bed",
        "any"
    ]:

        return ""

    return value


# =========================================================
# FALLBACK HOSPITAL GENERATOR
# =========================================================

def generate_fallback_hospitals(
    district,
    city,
    bed_type
):

    show_district = (
        district
        if district
        else "Maharashtra"
    )

    show_city = (
        city
        if city
        else "Nearby City"
    )

    # -----------------------------------------------------
    # Default beds
    # -----------------------------------------------------

    general_1 = 15
    icu_1 = 8
    emergency_1 = 5

    general_2 = 20
    icu_2 = 10
    emergency_2 = 6

    general_3 = 12
    icu_3 = 6
    emergency_3 = 4

    # -----------------------------------------------------
    # If specific bed type selected,
    # make that type clearly available
    # -----------------------------------------------------

    if bed_type == "General":

        general_1 = 20
        general_2 = 25
        general_3 = 18

    elif bed_type == "ICU":

        icu_1 = 12
        icu_2 = 15
        icu_3 = 10

    elif bed_type == "Emergency":

        emergency_1 = 10
        emergency_2 = 12
        emergency_3 = 8

    hospitals = [

        {
            "id": None,

            "hospital_name":
                f"RAHE Emergency Hospital - {show_city}",

            "address":
                f"Main Road, {show_city}, "
                f"{show_district}, Maharashtra",

            "district":
                show_district,

            "city":
                show_city,

            "village":
                show_city,

            "contact":
                "9876543210",

            "general_beds":
                general_1,

            "icu_beds":
                icu_1,

            "emergency_beds":
                emergency_1,

            "latitude":
                None,

            "longitude":
                None,

            "username":
                None,

            "password":
                None,

            "distance":
                None,

            "travel_time":
                None,

            "demo":
                True
        },

        {
            "id": None,

            "hospital_name":
                f"City Care Hospital - {show_city}",

            "address":
                f"Station Road, {show_city}, "
                f"{show_district}, Maharashtra",

            "district":
                show_district,

            "city":
                show_city,

            "village":
                show_city,

            "contact":
                "9123456780",

            "general_beds":
                general_2,

            "icu_beds":
                icu_2,

            "emergency_beds":
                emergency_2,

            "latitude":
                None,

            "longitude":
                None,

            "username":
                None,

            "password":
                None,

            "distance":
                None,

            "travel_time":
                None,

            "demo":
                True
        },

        {
            "id": None,

            "hospital_name":
                f"LifeLine Hospital - {show_city}",

            "address":
                f"Hospital Road, {show_city}, "
                f"{show_district}, Maharashtra",

            "district":
                show_district,

            "city":
                show_city,

            "village":
                show_city,

            "contact":
                "9988776655",

            "general_beds":
                general_3,

            "icu_beds":
                icu_3,

            "emergency_beds":
                emergency_3,

            "latitude":
                None,

            "longitude":
                None,

            "username":
                None,

            "password":
                None,

            "distance":
                None,

            "travel_time":
                None,

            "demo":
                True
        }
    ]

    return hospitals


# =========================================================
# FILTER BED TYPE IN PYTHON
# =========================================================

def filter_hospitals_by_bed_type(
    hospitals,
    bed_type
):

    if not bed_type:

        return hospitals

    result = []

    for hospital in hospitals:

        if bed_type == "General":

            if (
                int(
                    hospital.get(
                        "general_beds",
                        0
                    ) or 0
                ) > 0
            ):

                result.append(hospital)

        elif bed_type == "ICU":

            if (
                int(
                    hospital.get(
                        "icu_beds",
                        0
                    ) or 0
                ) > 0
            ):

                result.append(hospital)

        elif bed_type == "Emergency":

            if (
                int(
                    hospital.get(
                        "emergency_beds",
                        0
                    ) or 0
                ) > 0
            ):

                result.append(hospital)

        else:

            result.append(hospital)

    return result


# =========================================================
# HOSPITAL SEARCH
# =========================================================

@app.route(
    "/hospital",
    methods=["GET", "POST"]
)
def hospital():

    if not login_required():

        return redirect(
            url_for("login")
        )

    # -----------------------------------------------------
    # GET SEARCH VALUES
    # -----------------------------------------------------

    district = request.values.get(
        "district",
        ""
    ).strip()

    city = request.values.get(
        "city",
        ""
    ).strip()

    bed_type_raw = request.values.get(
        "bed_type",
        ""
    ).strip()

    # -----------------------------------------------------
    # NORMALIZE
    # -----------------------------------------------------

    bed_type = normalize_bed_type(
        bed_type_raw
    )

    # -----------------------------------------------------
    # DATABASE QUERY
    # -----------------------------------------------------

    query = """
        SELECT *
        FROM hospitals
        WHERE 1 = 1
    """

    params = []

    # -----------------------------------------------------
    # DISTRICT FILTER
    # -----------------------------------------------------

    if district:

        if district.lower() not in [
            "all",
            "all districts",
            "all district"
        ]:

            query += """
                AND LOWER(
                    TRIM(
                        COALESCE(
                            district,
                            ''
                        )
                    )
                ) = LOWER(
                    TRIM(?)
                )
            """

            params.append(
                district
            )

    # -----------------------------------------------------
    # CITY / VILLAGE FILTER
    # -----------------------------------------------------

    if city:

        if city.lower() not in [
            "all",
            "all cities",
            "all villages"
        ]:

            query += """
                AND (
                    LOWER(
                        COALESCE(
                            city,
                            ''
                        )
                    ) LIKE LOWER(?)

                    OR

                    LOWER(
                        COALESCE(
                            village,
                            ''
                        )
                    ) LIKE LOWER(?)

                    OR

                    LOWER(
                        COALESCE(
                            address,
                            ''
                        )
                    ) LIKE LOWER(?)
                )
            """

            search_city = (
                "%"
                + city
                + "%"
            )

            params.extend([
                search_city,
                search_city,
                search_city
            ])

    # -----------------------------------------------------
    # BED FILTER
    # -----------------------------------------------------

    if bed_type == "General":

        query += """
            AND COALESCE(
                general_beds,
                0
            ) > 0
        """

    elif bed_type == "ICU":

        query += """
            AND COALESCE(
                icu_beds,
                0
            ) > 0
        """

    elif bed_type == "Emergency":

        query += """
            AND COALESCE(
                emergency_beds,
                0
            ) > 0
        """

    # -----------------------------------------------------
    # ORDER
    # -----------------------------------------------------

    query += """
        ORDER BY hospital_name ASC
    """

    # -----------------------------------------------------
    # EXECUTE
    # -----------------------------------------------------

    conn = get_db_connection()

    try:

        rows = conn.execute(
            query,
            params
        ).fetchall()

    except sqlite3.Error as e:

        print(
            "Hospital search error:",
            e
        )

        rows = []

    finally:

        conn.close()

    # -----------------------------------------------------
    # CONVERT TO DICTIONARY
    # -----------------------------------------------------

    hospital_list = []

    for row in rows:

        item = dict(row)

        item["distance"] = None

        item["travel_time"] = None

        item["demo"] = False

        hospital_list.append(
            item
        )

    # -----------------------------------------------------
    # FALLBACK
    #
    # IMPORTANT:
    # If no hospital found,
    # generate demo hospitals
    # for selected location.
    # -----------------------------------------------------

    if not hospital_list:

        hospital_list = (
            generate_fallback_hospitals(
                district,
                city,
                bed_type
            )
        )

    # -----------------------------------------------------
    # FINAL BED FILTER
    # -----------------------------------------------------

    hospital_list = (
        filter_hospitals_by_bed_type(
            hospital_list,
            bed_type
        )
    )

    # -----------------------------------------------------
    # SEND TO TEMPLATE
    # -----------------------------------------------------

    return render_template(
        "hospital.html",

        hospitals=hospital_list,

        districts=MAHARASHTRA_DISTRICTS,

        locations=MAHARASHTRA_LOCATIONS,

        district=district,

        city=city,

        bed_type=bed_type_raw
    )


# =========================================================
# EMERGENCY BED NOW
# =========================================================

@app.route("/emergency-bed-now")
def emergency_bed_now():

    if not login_required():

        return redirect(
            url_for("login")
        )

    user_lat = request.args.get(
        "latitude",
        ""
    ).strip()

    user_lon = request.args.get(
        "longitude",
        ""
    ).strip()

    # -----------------------------------------------------
    # NO LOCATION
    # -----------------------------------------------------

    if not user_lat or not user_lon:

        conn = get_db_connection()

        rows = conn.execute(
            """
            SELECT *
            FROM hospitals

            WHERE COALESCE(
                emergency_beds,
                0
            ) > 0

            ORDER BY emergency_beds DESC
            """
        ).fetchall()

        conn.close()

        hospitals = []

        for row in rows:

            item = dict(row)

            item["distance"] = None

            item["travel_time"] = None

            hospitals.append(item)

        return render_template(
            "emergency_bed_now.html",
            hospitals=hospitals,
            user_lat=None,
            user_lon=None
        )

    # -----------------------------------------------------
    # LOCATION CONVERSION
    # -----------------------------------------------------

    try:

        user_lat_float = float(
            user_lat
        )

        user_lon_float = float(
            user_lon
        )

    except ValueError:

        user_lat_float = None

        user_lon_float = None

    # -----------------------------------------------------
    # GET HOSPITALS
    # -----------------------------------------------------

    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM hospitals

        WHERE COALESCE(
            emergency_beds,
            0
        ) > 0
        """
    ).fetchall()

    conn.close()

    hospitals = []

    for row in rows:

        item = dict(row)

        item["distance"] = None

        item["travel_time"] = None

        if (
            user_lat_float is not None
            and
            user_lon_float is not None
            and
            row["latitude"] is not None
            and
            row["longitude"] is not None
        ):

            distance = haversine(
                user_lat_float,
                user_lon_float,
                row["latitude"],
                row["longitude"]
            )

            item["distance"] = distance

            item["travel_time"] = (
                calculate_travel_time(
                    distance
                )
            )

        hospitals.append(item)

    hospitals.sort(
        key=lambda h:
        h["distance"]
        if h["distance"] is not None
        else 999999
    )

    return render_template(
        "emergency_bed_now.html",
        hospitals=hospitals,
        user_lat=user_lat_float,
        user_lon=user_lon_float
    )


# =========================================================
# NEAREST HOSPITAL
# =========================================================

@app.route(
    "/nearest",
    methods=["GET", "POST"]
)
def nearest():

    if not login_required():

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

        user_lat = request.form.get(
            "latitude",
            ""
        ).strip()

        user_lon = request.form.get(
            "longitude",
            ""
        ).strip()

    else:

        user_lat = request.args.get(
            "latitude",
            ""
        ).strip()

        user_lon = request.args.get(
            "longitude",
            ""
        ).strip()

    try:

        user_lat_float = float(
            user_lat
        )

        user_lon_float = float(
            user_lon
        )

    except (
        TypeError,
        ValueError
    ):

        user_lat_float = None

        user_lon_float = None

    conn = get_db_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM hospitals

        WHERE
            COALESCE(
                emergency_beds,
                0
            ) > 0

            OR

            COALESCE(
                general_beds,
                0
            ) > 0

            OR

            COALESCE(
                icu_beds,
                0
            ) > 0
        """
    ).fetchall()

    conn.close()

    hospitals = []

    for row in rows:

        item = dict(row)

        item["distance"] = None

        item["travel_time"] = None

        if (
            user_lat_float is not None
            and
            user_lon_float is not None
            and
            row["latitude"] is not None
            and
            row["longitude"] is not None
        ):

            distance = haversine(
                user_lat_float,
                user_lon_float,
                row["latitude"],
                row["longitude"]
            )

            item["distance"] = distance

            item["travel_time"] = (
                calculate_travel_time(
                    distance
                )
            )

        hospitals.append(item)

    if (
        user_lat_float is not None
        and
        user_lon_float is not None
    ):

        hospitals.sort(
            key=lambda h:
            h["distance"]
            if h["distance"] is not None
            else 999999
        )

    return render_template(
        "nearest.html",
        hospitals=hospitals,
        user_lat=user_lat_float,
        user_lon=user_lon_float
    )


# =========================================================
# HOSPITAL LOGIN
# =========================================================

@app.route(
    "/hospital-login",
    methods=["GET", "POST"]
)
def hospital_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        conn = get_db_connection()

        hospital_user = conn.execute(
            """
            SELECT *
            FROM hospitals

            WHERE username = ?
            AND password = ?
            """,
            (
                username,
                password
            )
        ).fetchone()

        conn.close()

        if hospital_user:

            session.pop(
                "user_id",
                None
            )

            session.pop(
                "name",
                None
            )

            session.pop(
                "email",
                None
            )

            session["hospital_id"] = (
                hospital_user["id"]
            )

            session["hospital_name"] = (
                hospital_user["hospital_name"]
            )

            session["hospital_username"] = (
                hospital_user["username"]
            )

            return redirect(
                url_for(
                    "hospital_dashboard"
                )
            )

        flash(
            "Invalid hospital username or password.",
            "error"
        )

    return render_template(
        "hospital_login.html",
        districts=MAHARASHTRA_DISTRICTS
    )


# =========================================================
# HOSPITAL REGISTER
# =========================================================

@app.route(
    "/hospital-register",
    methods=["GET", "POST"]
)
def hospital_register():

    if request.method == "POST":

        hospital_name = request.form.get(
            "hospital_name",
            ""
        ).strip()

        username = request.form.get(
            "username",
            ""
        ).strip()

        if not username:

            username = request.form.get(
                "email",
                ""
            ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        contact = request.form.get(
            "contact",
            ""
        ).strip()

        district = request.form.get(
            "district",
            ""
        ).strip()

        city = request.form.get(
            "city",
            ""
        ).strip()

        village = request.form.get(
            "village",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        latitude = request.form.get(
            "latitude",
            ""
        ).strip()

        longitude = request.form.get(
            "longitude",
            ""
        ).strip()

        if (
            not hospital_name
            or not username
            or not password
            or not contact
            or not district
            or not city
            or not address
        ):

            flash(
                "Please fill all required fields.",
                "error"
            )

            return redirect(
                url_for(
                    "hospital_register"
                )
            )

        try:

            latitude_value = (
                float(latitude)
                if latitude
                else None
            )

        except ValueError:

            latitude_value = None

        try:

            longitude_value = (
                float(longitude)
                if longitude
                else None
            )

        except ValueError:

            longitude_value = None

        conn = get_db_connection()

        try:

            existing = conn.execute(
                """
                SELECT id
                FROM hospitals

                WHERE username = ?
                """,
                (
                    username,
                )
            ).fetchone()

            if existing:

                flash(
                    "Hospital username already registered.",
                    "error"
                )

                return redirect(
                    url_for(
                        "hospital_login"
                    )
                )

            conn.execute(
                """
                INSERT INTO hospitals
                (
                    hospital_name,
                    address,
                    district,
                    city,
                    village,
                    contact,
                    general_beds,
                    icu_beds,
                    emergency_beds,
                    latitude,
                    longitude,
                    username,
                    password
                )

                VALUES
                (
                    ?, ?, ?, ?, ?, ?,
                    0, 0, 0,
                    ?, ?, ?, ?
                )
                """,
                (
                    hospital_name,
                    address,
                    district,
                    city,
                    village,
                    contact,
                    latitude_value,
                    longitude_value,
                    username,
                    password
                )
            )

            conn.commit()

            flash(
                "Hospital registered successfully. Please login.",
                "success"
            )

            return redirect(
                url_for(
                    "hospital_login"
                )
            )

        except sqlite3.IntegrityError:

            conn.rollback()

            flash(
                "Hospital username already exists.",
                "error"
            )

            return redirect(
                url_for(
                    "hospital_login"
                )
            )

        finally:

            conn.close()

    return render_template(
        "hospital_login.html",
        districts=MAHARASHTRA_DISTRICTS,
        show_register=True
    )


# =========================================================
# HOSPITAL DASHBOARD
# =========================================================

@app.route(
    "/hospital-dashboard",
    methods=["GET", "POST"]
)
def hospital_dashboard():

    if not hospital_login_required():

        return redirect(
            url_for("hospital_login")
        )

    hospital_id = session[
        "hospital_id"
    ]

    conn = get_db_connection()

    if request.method == "POST":

        try:

            general_beds = max(
                0,
                int(
                    request.form.get(
                        "general_beds",
                        0
                    )
                )
            )

            icu_beds = max(
                0,
                int(
                    request.form.get(
                        "icu_beds",
                        0
                    )
                )
            )

            emergency_beds = max(
                0,
                int(
                    request.form.get(
                        "emergency_beds",
                        0
                    )
                )
            )

        except ValueError:

            flash(
                "Enter valid bed numbers.",
                "error"
            )

            conn.close()

            return redirect(
                url_for(
                    "hospital_dashboard"
                )
            )

        conn.execute(
            """
            UPDATE hospitals

            SET
                general_beds = ?,
                icu_beds = ?,
                emergency_beds = ?

            WHERE id = ?
            """,
            (
                general_beds,
                icu_beds,
                emergency_beds,
                hospital_id
            )
        )

        conn.commit()

        flash(
            "Bed availability updated successfully.",
            "success"
        )

    hospital_data = conn.execute(
        """
        SELECT *
        FROM hospitals

        WHERE id = ?
        """,
        (
            hospital_id,
        )
    ).fetchone()

    conn.close()

    if hospital_data is None:

        session.pop(
            "hospital_id",
            None
        )

        session.pop(
            "hospital_name",
            None
        )

        return redirect(
            url_for(
                "hospital_login"
            )
        )

    return render_template(
        "hospital_dashboard.html",
        hospital=hospital_data
    )


# =========================================================
# HOSPITAL LOGOUT
# =========================================================

@app.route("/hospital-logout")
def hospital_logout():

    session.pop(
        "hospital_id",
        None
    )

    session.pop(
        "hospital_name",
        None
    )

    session.pop(
        "hospital_username",
        None
    )

    return redirect(
        url_for(
            "hospital_login"
        )
    )


# =========================================================
# EMERGENCY CONTACT
# =========================================================

@app.route("/emergency-contact")
def emergency_contact():

    if not login_required():

        return redirect(
            url_for("login")
        )

    return render_template(
        "emergency_contact.html"
    )


# =========================================================
# EMERGENCY
# =========================================================

@app.route("/emergency")
def emergency():

    return redirect(
        url_for(
            "emergency_contact"
        )
    )


# =========================================================
# SOS
# =========================================================

@app.route(
    "/sos",
    methods=["GET", "POST"]
)
def sos():

    if not login_required():

        return redirect(
            url_for("login")
        )

    if request.method == "GET":

        return render_template(
            "sos.html"
        )

    latitude = request.form.get(
        "latitude",
        ""
    ).strip()

    longitude = request.form.get(
        "longitude",
        ""
    ).strip()

    location = request.form.get(
        "location",
        ""
    ).strip()

    if not latitude or not longitude:

        flash(
            "Please get your current location before sending SOS.",
            "error"
        )

        return redirect(
            url_for("sos")
        )

    try:

        latitude_value = float(
            latitude
        )

        longitude_value = float(
            longitude
        )

    except ValueError:

        flash(
            "Invalid location coordinates.",
            "error"
        )

        return redirect(
            url_for("sos")
        )

    if not location:

        location = (
            f"{latitude_value:.6f}, "
            f"{longitude_value:.6f}"
        )

    user_id = session.get(
        "user_id"
    )

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO sos_alerts
        (
            user_id,
            latitude,
            longitude,
            location,
            status,
            created_at
        )

        VALUES
        (
            ?,
            ?,
            ?,
            ?,
            'Active',
            CURRENT_TIMESTAMP
        )
        """,
        (
            user_id,
            latitude_value,
            longitude_value,
            location
        )
    )

    conn.commit()

    conn.close()

    flash(
        "SOS alert sent successfully. Your location has been saved.",
        "success"
    )

    return redirect(
        url_for("history")
    )


# =========================================================
# AMBULANCE
# =========================================================

@app.route("/ambulance")
def ambulance():

    return render_template(
        "ambulance.html"
    )


# =========================================================
# POLICE
# =========================================================

@app.route("/police")
def police():

    return render_template(
        "police.html"
    )


# =========================================================
# UPLOADED FILE
# =========================================================

@app.route(
    "/uploads/<path:filename>"
)
def uploaded_file(filename):

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


# =========================================================
# REPORT ACCIDENT
# =========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
def report():

    if request.method == "GET":

        return render_template(
            "report_accident.html"
        )

    name = request.form.get(
        "name",
        ""
    ).strip()

    mobile = request.form.get(
        "mobile",
        ""
    ).strip()

    location = request.form.get(
        "location",
        ""
    ).strip()

    vehicle = request.form.get(
        "vehicle",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    if (
        not name
        or not mobile
        or not location
        or not vehicle
    ):

        flash(
            "Please fill all required accident fields.",
            "error"
        )

        return redirect(
            url_for("report")
        )

    filename = None

    image = request.files.get(
        "image"
    )

    if image and image.filename:

        filename = secure_filename(
            image.filename
        )

        if filename:

            image.save(
                os.path.join(
                    app.config[
                        "UPLOAD_FOLDER"
                    ],
                    filename
                )
            )

    user_id = session.get(
        "user_id"
    )

    conn = get_db_connection()

    conn.execute(
        """
        INSERT INTO accidents
        (
            user_id,
            name,
            mobile,
            location,
            vehicle,
            description,
            image,
            status,
            created_at
        )

        VALUES
        (
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            CURRENT_TIMESTAMP
        )
        """,
        (
            user_id,
            name,
            mobile,
            location,
            vehicle,
            description,
            filename,
            "Pending"
        )
    )

    conn.commit()

    conn.close()

    flash(
        "Accident report submitted successfully.",
        "success"
    )

    if user_id:

        return redirect(
            url_for("history")
        )

    return redirect(
        url_for("index")
    )


# =========================================================
# HISTORY
# =========================================================

@app.route("/history")
def history():

    if not login_required():

        return redirect(
            url_for("login")
        )

    user_id = session[
        "user_id"
    ]

    conn = get_db_connection()

    accidents = conn.execute(
        """
        SELECT *
        FROM accidents

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (
            user_id,
        )
    ).fetchall()

    sos_alerts = conn.execute(
        """
        SELECT *
        FROM sos_alerts

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (
            user_id,
        )
    ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        accidents=accidents,
        sos_alerts=sos_alerts
    )


# =========================================================
# ADMIN SETTINGS
# =========================================================

ADMIN_USERNAME = "admin"

ADMIN_PASSWORD = "admin123"


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin",
    methods=["GET", "POST"]
)
def admin():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        ).strip()

        if (
            username == ADMIN_USERNAME
            and
            password == ADMIN_PASSWORD
        ):

            session["admin"] = True

            return redirect(
                url_for(
                    "admin_dashboard"
                )
            )

        flash(
            "Invalid admin username or password.",
            "error"
        )

    return render_template(
        "admin.html"
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin-dashboard")
@app.route("/admin_dashboard")
def admin_dashboard():

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    conn = get_db_connection()

    accidents = conn.execute(
        """
        SELECT *
        FROM accidents

        ORDER BY id DESC
        """
    ).fetchall()

    hospitals = conn.execute(
        """
        SELECT *
        FROM hospitals

        ORDER BY hospital_name
        """
    ).fetchall()

    users = conn.execute(
        """
        SELECT *
        FROM users

        ORDER BY id DESC
        """
    ).fetchall()

    sos_alerts = conn.execute(
        """
        SELECT
            sos_alerts.*,
            users.name AS user_name,
            users.email AS user_email

        FROM sos_alerts

        LEFT JOIN users
        ON sos_alerts.user_id = users.id

        ORDER BY sos_alerts.id DESC
        """
    ).fetchall()

    total_accidents = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM accidents
        """
    ).fetchone()["c"]

    pending_accidents = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM accidents

        WHERE status = 'Pending'
        """
    ).fetchone()["c"]

    completed_accidents = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM accidents

        WHERE status = 'Completed'
        """
    ).fetchone()["c"]

    total_hospitals = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM hospitals
        """
    ).fetchone()["c"]

    total_users = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM users
        """
    ).fetchone()["c"]

    total_sos = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM sos_alerts
        """
    ).fetchone()["c"]

    active_sos = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM sos_alerts

        WHERE status = 'Active'
        """
    ).fetchone()["c"]

    total_general_beds = conn.execute(
        """
        SELECT COALESCE(
            SUM(general_beds),
            0
        ) AS c

        FROM hospitals
        """
    ).fetchone()["c"]

    total_icu_beds = conn.execute(
        """
        SELECT COALESCE(
            SUM(icu_beds),
            0
        ) AS c

        FROM hospitals
        """
    ).fetchone()["c"]

    total_emergency_beds = conn.execute(
        """
        SELECT COALESCE(
            SUM(emergency_beds),
            0
        ) AS c

        FROM hospitals
        """
    ).fetchone()["c"]

    conn.close()

    return render_template(
        "admin_dashboard.html",

        accidents=accidents,

        hospitals=hospitals,

        users=users,

        sos_alerts=sos_alerts,

        total_accidents=total_accidents,

        pending_accidents=pending_accidents,

        completed_accidents=completed_accidents,

        total_hospitals=total_hospitals,

        total_users=total_users,

        total_sos=total_sos,

        active_sos=active_sos,

        total_general_beds=total_general_beds,

        total_icu_beds=total_icu_beds,

        total_emergency_beds=total_emergency_beds
    )


# =========================================================
# ADMIN UPDATE ACCIDENT STATUS
# =========================================================

@app.route(
    "/admin/update-accident/<int:accident_id>",
    methods=["POST"]
)
def update_accident_status(
    accident_id
):

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    status = request.form.get(
        "status",
        "Pending"
    ).strip()

    allowed_status = [
        "Pending",
        "In Process",
        "Completed"
    ]

    if status not in allowed_status:

        status = "Pending"

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE accidents

        SET status = ?

        WHERE id = ?
        """,
        (
            status,
            accident_id
        )
    )

    conn.commit()

    conn.close()

    flash(
        "Accident status updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN UPDATE SOS
# =========================================================

@app.route(
    "/admin/update-sos/<int:sos_id>",
    methods=["POST"]
)
def update_sos_status(
    sos_id
):

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    status = request.form.get(
        "status",
        "Active"
    ).strip()

    allowed_status = [
        "Active",
        "Responded",
        "Completed"
    ]

    if status not in allowed_status:

        status = "Active"

    conn = get_db_connection()

    conn.execute(
        """
        UPDATE sos_alerts

        SET status = ?

        WHERE id = ?
        """,
        (
            status,
            sos_id
        )
    )

    conn.commit()

    conn.close()

    flash(
        "SOS status updated successfully.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN DELETE SOS
# =========================================================

@app.route(
    "/admin/delete-sos/<int:sos_id>",
    methods=["POST"]
)
def delete_sos(sos_id):

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM sos_alerts

        WHERE id = ?
        """,
        (
            sos_id,
        )
    )

    conn.commit()

    conn.close()

    flash(
        "SOS alert deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN DELETE ACCIDENT
# =========================================================

@app.route(
    "/admin/delete-accident/<int:accident_id>",
    methods=["POST"]
)
def delete_accident(
    accident_id
):

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    conn = get_db_connection()

    accident = conn.execute(
        """
        SELECT image
        FROM accidents

        WHERE id = ?
        """,
        (
            accident_id,
        )
    ).fetchone()

    if accident and accident["image"]:

        image_path = os.path.join(
            app.config[
                "UPLOAD_FOLDER"
            ],
            accident["image"]
        )

        if os.path.exists(
            image_path
        ):

            try:

                os.remove(
                    image_path
                )

            except OSError:

                pass

    conn.execute(
        """
        DELETE FROM accidents

        WHERE id = ?
        """,
        (
            accident_id,
        )
    )

    conn.commit()

    conn.close()

    flash(
        "Accident report deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN DELETE HOSPITAL
# =========================================================

@app.route(
    "/admin/delete-hospital/<int:hospital_id>",
    methods=["POST"]
)
def delete_hospital(
    hospital_id
):

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM hospitals

        WHERE id = ?
        """,
        (
            hospital_id,
        )
    )

    conn.commit()

    conn.close()

    flash(
        "Hospital deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN DELETE USER
# =========================================================

@app.route(
    "/admin/delete-user/<int:user_id>",
    methods=["POST"]
)
def delete_user(
    user_id
):

    if not admin_login_required():

        return redirect(
            url_for("admin")
        )

    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM users

        WHERE id = ?
        """,
        (
            user_id,
        )
    )

    conn.commit()

    conn.close()

    flash(
        "User deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin-logout")
def admin_logout():

    session.pop(
        "admin",
        None
    )

    return redirect(
        url_for("admin")
    )


# =========================================================
# 404 ERROR
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>RAHE - Page Not Found</title>

        <style>

            body {
                font-family: Arial;
                text-align: center;
                padding: 60px;
                background: #f8f9fa;
            }

            h1 {
                font-size: 70px;
                margin: 0;
                color: #dc3545;
            }

            h2 {
                color: #333;
            }

            p {
                color: #666;
            }

            a {
                display: inline-block;
                margin-top: 20px;
                padding: 12px 25px;
                background: #007bff;
                color: white;
                text-decoration: none;
                border-radius: 8px;
            }

        </style>

    </head>

    <body>

        <h1>404</h1>

        <h2>Page Not Found</h2>

        <p>
            The requested page does not exist.
        </p>

        <a href="/">
            Back to RAHE Home
        </a>

    </body>

    </html>
    """, 404


# =========================================================
# 413 ERROR
# =========================================================

@app.errorhandler(413)
def file_too_large(error):

    flash(
        "Uploaded file is too large. Maximum size is 5 MB.",
        "error"
    )

    return redirect(
        url_for("report")
    )


# =========================================================
# RUN FLASK
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )