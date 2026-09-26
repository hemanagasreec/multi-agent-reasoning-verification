import sqlite3


DB_NAME = "database/fraud_detection.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    # ==========================================
    # TRANSACTIONS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            amount REAL,
            location TEXT,
            device TEXT,
            timestamp TEXT,
            transaction_type TEXT DEFAULT 'CURRENT'
        )
    """)

    # ==========================================
    # TASKS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            transaction_id TEXT,
            final_decision TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)

    # ==========================================
    # AGENT RUNS / AUDIT LOG
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            agent_name TEXT,
            risk_level TEXT,
            reason TEXT,
            evidence TEXT,
            confidence REAL,
            revision INTEGER
        )
    """)

    # ==========================================
    # VERIFICATION RESULTS
    # ==========================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS verification_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT,
            status TEXT,
            reason TEXT,
            confidence REAL,
            revision INTEGER
        )
    """)

    conn.commit()
    conn.close()


# ==========================================
# SAVE TRANSACTION
# ==========================================

def save_transaction(
    transaction,
    transaction_type="CURRENT"
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO transactions
        (
            transaction_id,
            amount,
            location,
            device,
            timestamp,
            transaction_type
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        transaction.transaction_id,
        transaction.amount,
        transaction.location,
        transaction.device,
        transaction.timestamp,
        transaction_type
    ))

    conn.commit()
    conn.close()


# ==========================================
# GET HISTORICAL TRANSACTION AMOUNTS
# ==========================================

def get_transaction_history(transaction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT amount
        FROM transactions
        WHERE transaction_type = 'HISTORICAL'
        AND transaction_id != ?
        ORDER BY timestamp DESC
    """, (transaction_id,))

    rows = cursor.fetchall()

    conn.close()

    return [
        row[0]
        for row in rows
    ]


# ==========================================
# SAVE TASK
# ==========================================

def save_task(
    task_id,
    transaction_id,
    decision,
    confidence,
    timestamp
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO tasks
        (
            task_id,
            transaction_id,
            final_decision,
            confidence,
            timestamp
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        task_id,
        transaction_id,
        decision,
        confidence,
        timestamp
    ))

    conn.commit()
    conn.close()


# ==========================================
# SAVE AGENT RESULT
# ==========================================

def save_agent_result(
    task_id,
    result
):

    conn = get_connection()
    cursor = conn.cursor()

    evidence_text = " | ".join(
        result.evidence
    )

    cursor.execute("""
        INSERT INTO agent_runs
        (
            task_id,
            agent_name,
            risk_level,
            reason,
            evidence,
            confidence,
            revision
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        task_id,
        result.agent_name,
        result.risk_level,
        result.reason,
        evidence_text,
        result.confidence,
        result.revision
    ))

    conn.commit()
    conn.close()


# ==========================================
# SAVE VERIFICATION
# ==========================================

def save_verification(
    task_id,
    result
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO verification_results
        (
            task_id,
            status,
            reason,
            confidence,
            revision
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        task_id,
        result.status,
        result.reason,
        result.confidence,
        result.revision
    ))

    conn.commit()
    conn.close()
