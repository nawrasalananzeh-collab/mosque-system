def init_db():
    conn = db()

    # USERS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    # STUDENTS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        phone TEXT,
        national_id TEXT,
        sheikh_group TEXT,
        address TEXT,
        parent_phone TEXT,
        image TEXT,
        juz_count INTEGER DEFAULT 0,
        umrah_count INTEGER DEFAULT 0,
        umrah_dates TEXT
    )
    """)

    # TEACHERS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        age TEXT,
        address TEXT,
        specialization TEXT,
        join_date TEXT,
        students_count INTEGER DEFAULT 0,
        status TEXT
    )
    """)

    # SESSIONS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        session_time TEXT,
        supervisor TEXT
    )
    """)

    # HAFAZ
    conn.execute("""
    CREATE TABLE IF NOT EXISTS hafaz (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT,
        juz_count INTEGER,
        sheikh TEXT,
        khatma_date TEXT,
        khatma_place TEXT
    )
    """)

    # TESTS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT,
        test_type TEXT,
        score TEXT,
        date TEXT,
        notes TEXT,
        pdf_file TEXT
    )
    """)

    # UMRAH
    conn.execute("""
    CREATE TABLE IF NOT EXISTS umrah_memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        umrah_year TEXT,
        umrah_date TEXT,
        description TEXT,
        file_name TEXT
    )
    """)

    # COMPETITIONS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS competitions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        prize TEXT,
        status TEXT DEFAULT 'active'
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS competition_participants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competition_id INTEGER,
    student_id INTEGER,
    score INTEGER DEFAULT 0,
    rank INTEGER DEFAULT 0
);
    )
    """)

    # SETTINGS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        setting_name TEXT,
        setting_value TEXT
    )
    """)

    # NOTIFICATIONS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        message TEXT,
        created_at TEXT
    )
    """)

    # PHONE DIRECTORY
    conn.execute("""
    CREATE TABLE IF NOT EXISTS phone_directory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        phone TEXT,
        notes TEXT
    )
    """)

    # BACKUPS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS backups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        created_at TEXT
    )
    """)

    # REPORTS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_name TEXT,
        created_at TEXT
    )
    """)

    # TRANSPORT CARS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS transport_cars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_name TEXT,
        driver_name TEXT,
        driver_phone TEXT,
        seats INTEGER,
        notes TEXT
    )
    """)

    # TRANSPORT REQUESTS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS transport_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        car_id INTEGER,
        trip_date TEXT,
        pickup_location TEXT,
        destination TEXT
    )
    """)

    # MOSQUE SETTINGS
    conn.execute("""
    CREATE TABLE IF NOT EXISTS mosque_settings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mosque_name TEXT,
        mosque_logo TEXT,
        mosque_address TEXT,
        mosque_phone TEXT
    )
    """)

    conn.commit()
    conn.close()