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

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

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
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024


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
        DB_PATH,
        timeout=20
    )

    conn.row_factory = sqlite3.Row

    return conn


# =========================================================
# CHECK COLUMN
# =========================================================

def column_exists(conn, table, column):

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

    # =====================================================
    # DEMO HOSPITALS
    # =====================================================

    count = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM hospitals
        """
    ).fetchone()["c"]

    if count == 0:

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

        conn.executemany(
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
            demo_hospitals
        )

    conn.commit()

    conn.close()


# =========================================================
# INITIALIZE DATABASE
# =========================================================

create_tables()


# =========================================================
# USER LOGIN CHECK
# =========================================================

def login_required():

    return "user_id" in session


# =========================================================
# HOSPITAL LOGIN CHECK
# =========================================================

def hospital_login_required():

    return "hospital_id" in session


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
# USER DASHBOARD
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

    district = request.values.get(
        "district",
        ""
    ).strip()

    city = request.values.get(
        "city",
        ""
    ).strip()

    bed_type = request.values.get(
        "bed_type",
        ""
    ).strip()

    query = """
        SELECT *
        FROM hospitals
        WHERE 1 = 1
    """

    params = []

    if district:

        query += """
            AND district LIKE ?
        """

        params.append(
            "%" + district + "%"
        )

    if city:

        query += """
            AND (
                city LIKE ?
                OR village LIKE ?
            )
        """

        params.extend(
            [
                "%" + city + "%",
                "%" + city + "%"
            ]
        )

    if bed_type == "General":

        query += """
            AND general_beds > 0
        """

    elif bed_type == "ICU":

        query += """
            AND icu_beds > 0
        """

    elif bed_type == "Emergency":

        query += """
            AND emergency_beds > 0
        """

    query += """
        ORDER BY hospital_name
    """

    conn = get_db_connection()

    hospitals = conn.execute(
        query,
        params
    ).fetchall()

    conn.close()

    return render_template(
        "hospital.html",
        hospitals=hospitals,
        districts=MAHARASHTRA_DISTRICTS,
        district=district,
        city=city,
        bed_type=bed_type
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

    conn = get_db_connection()

    hospitals = conn.execute(
        """
        SELECT *
        FROM hospitals

        WHERE emergency_beds > 0

        ORDER BY emergency_beds DESC
        """
    ).fetchall()

    conn.close()

    return render_template(
        "emergency_bed_now.html",
        hospitals=hospitals
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

        lat1, lon1, lat2, lon2 = map(
            float,
            [
                lat1,
                lon1,
                lat2,
                lon2
            ]
        )

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
            "latitude"
        )

        user_lon = request.form.get(
            "longitude"
        )

    else:

        user_lat = request.args.get(
            "latitude"
        )

        user_lon = request.args.get(
            "longitude"
        )

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

        if (
            user_lat
            and user_lon
            and row["latitude"] is not None
            and row["longitude"] is not None
        ):

            item["distance"] = haversine(
                user_lat,
                user_lon,
                row["latitude"],
                row["longitude"]
            )

        hospitals.append(item)

    if user_lat and user_lon:

        hospitals.sort(
            key=lambda h:
            h["distance"]
            if h["distance"] is not None
            else 999999
        )

    return render_template(
        "nearest.html",
        hospitals=hospitals,
        user_lat=user_lat,
        user_lon=user_lon
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

            session["hospital_id"] = hospital_user["id"]

            session["hospital_name"] = (
                hospital_user["hospital_name"]
            )

            session["hospital_username"] = (
                hospital_user["username"]
            )

            return redirect(
                url_for("hospital_dashboard")
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
                url_for("hospital_register")
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
                    url_for("hospital_login")
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
                url_for("hospital_login")
            )

        except sqlite3.IntegrityError:

            conn.rollback()

            flash(
                "Hospital username already exists.",
                "error"
            )

            return redirect(
                url_for("hospital_login")
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

    hospital_id = session["hospital_id"]

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
                url_for("hospital_dashboard")
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
            url_for("hospital_login")
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
        url_for("hospital_login")
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
        url_for("emergency_contact")
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
# REPORT ACCIDENT
# =========================================================

@app.route(
    "/report",
    methods=["GET", "POST"]
)
def report():

    if not login_required():

        return redirect(
            url_for("login")
        )

    if request.method == "POST":

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

            image.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
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
                session["user_id"],
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

        return redirect(
            url_for("history")
        )

    return render_template(
        "report_accident.html"
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

    conn = get_db_connection()

    accidents = conn.execute(
        """
        SELECT *
        FROM accidents

        WHERE user_id = ?

        ORDER BY id DESC
        """,
        (
            session["user_id"],
        )
    ).fetchall()

    conn.close()

    return render_template(
        "history.html",
        accidents=accidents
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

    if request.method == "POST":

        location = request.form.get(
            "location",
            ""
        ).strip()

        if location:

            flash(
                "SOS request sent successfully. "
                "Location: " + location,
                "success"
            )

        else:

            flash(
                "SOS request sent successfully.",
                "success"
            )

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "sos.html"
    )


# =========================================================
# LOCATION
# =========================================================

@app.route("/location")
def location():

    return render_template(
        "location.html"
    )


# =========================================================
# PROFILE
# =========================================================

@app.route("/profile")
def profile():

    if not login_required():

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    user = conn.execute(
        """
        SELECT *
        FROM users

        WHERE id = ?
        """,
        (
            session["user_id"],
        )
    ).fetchone()

    conn.close()

    return render_template(
        "profile.html",
        user=user
    )


# =========================================================
# ADMIN
# =========================================================

@app.route("/admin")
def admin():

    if not login_required():

        return redirect(
            url_for("login")
        )

    conn = get_db_connection()

    accidents = conn.execute(
        """
        SELECT *
        FROM accidents

        ORDER BY id DESC
        """
    ).fetchall()

    total = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM accidents
        """
    ).fetchone()["c"]

    pending = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM accidents

        WHERE status = 'Pending'
        """
    ).fetchone()["c"]

    completed = conn.execute(
        """
        SELECT COUNT(*) AS c
        FROM accidents

        WHERE status = 'Completed'
        """
    ).fetchone()["c"]

    conn.close()

    return render_template(
        "admin_dashboard.html",
        accidents=accidents,
        total=total,
        pending=pending,
        completed=completed
    )


# =========================================================
# UPDATE ACCIDENT STATUS
# =========================================================

@app.route(
    "/admin/update/<int:accident_id>",
    methods=["POST"]
)
def update_accident(accident_id):

    if not login_required():

        return redirect(
            url_for("login")
        )

    status = request.form.get(
        "status",
        "Pending"
    )

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

    return redirect(
        url_for("admin")
    )


# =========================================================
# UPLOADS
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
# 404
# =========================================================

@app.errorhandler(404)
def page_not_found(error):

    return """
    <!DOCTYPE html>

    <html>

    <head>

        <title>RAHE - Page Not Found</title>

    </head>

    <body style="
        font-family: Arial;
        text-align: center;
        padding: 60px;
    ">

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
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )