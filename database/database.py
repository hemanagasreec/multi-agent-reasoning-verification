import sqlite3


DB_NAME = "database/fraud_detection.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            transaction_id TEXT,
            final_decision TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            agent_name TEXT,
            risk_level TEXT,
            reason TEXT,
            confidence REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            status TEXT,
            reason TEXT,
            confidence REAL
        )
    """)

    conn.commit()
    conn.close()


def save_task(task_id, transaction_id, decision, confidence, timestamp):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (task_id, transaction_id, final_decision, confidence, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (task_id, transaction_id, decision, confidence, timestamp))

    conn.commit()
    conn.close()


def save_agent_result(task_id, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO agent_runs
        (task_id, agent_name, risk_level, reason, confidence)
        VALUES (?, ?, ?, ?, ?)
    """, (
        task_id,
        result.agent_name,
        result.risk_level,
        result.reason,
        result.confidence
    ))

    conn.commit()
    conn.close()


def save_verification(task_id, result):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO verification_results
        (task_id, status, reason, confidence)
        VALUES (?, ?, ?, ?)
    """, (
        task_id,
        result.status,
        result.reason,
        result.confidence
    ))

    conn.commit()
    conn.close()