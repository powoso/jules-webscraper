import sqlite3

DB_NAME = "scraper.db"

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            selector TEXT NOT NULL,
            interval_minutes INTEGER NOT NULL,
            last_run TIMESTAMP,
            is_active BOOLEAN DEFAULT 1
        )
    ''')

    c.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER NOT NULL,
            content TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')

    conn.commit()
    conn.close()

def add_job(url, selector, interval_minutes):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO jobs (url, selector, interval_minutes) VALUES (?, ?, ?)',
              (url, selector, interval_minutes))
    job_id = c.lastrowid
    conn.commit()
    conn.close()
    return job_id

def get_jobs():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM jobs').fetchall()
    conn.close()
    return rows

def get_job(job_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM jobs WHERE id = ?', (job_id,)).fetchone()
    conn.close()
    return row

def delete_job(job_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('DELETE FROM results WHERE job_id = ?', (job_id,))
    c.execute('DELETE FROM jobs WHERE id = ?', (job_id,))
    conn.commit()
    conn.close()

def add_result(job_id, content):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO results (job_id, content) VALUES (?, ?)', (job_id, content))
    c.execute('UPDATE jobs SET last_run = CURRENT_TIMESTAMP WHERE id = ?', (job_id,))
    conn.commit()
    conn.close()

def get_latest_result(job_id):
    conn = get_db_connection()
    row = conn.execute('SELECT * FROM results WHERE job_id = ? ORDER BY timestamp DESC LIMIT 1', (job_id,)).fetchone()
    conn.close()
    return row

def get_job_results(job_id):
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM results WHERE job_id = ? ORDER BY timestamp DESC', (job_id,)).fetchall()
    conn.close()
    return rows
