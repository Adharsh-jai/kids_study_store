from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3

app = Flask(__name__, static_folder=".")
CORS(app)

DB_PATH = "study_tracker.db"

# ── DB helpers ─────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                subject    TEXT    NOT NULL,
                duration   INTEGER NOT NULL DEFAULT 25,
                notes      TEXT    DEFAULT '',
                status     TEXT    NOT NULL DEFAULT 'Pending',
                date       TEXT    NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        count = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        if count == 0:
            seed = [
                ("Mathematics",  45, "Quadratic equations practice",  "Completed", "2026-08-31"),
                ("Science",      30, "Chapter 3 - Photosynthesis",     "Completed", "2026-08-31"),
                ("English",      25, "Essay writing draft",            "In Progress","2026-08-31"),
                ("History",      40, "World War II revision",          "Pending",    "2026-08-31"),
                ("Programming",  60, "Build study tracker app",        "Completed",  "2026-08-30"),
            ]
            conn.executemany(
                "INSERT INTO sessions (subject, duration, notes, status, date) VALUES (?,?,?,?,?)",
                seed
            )
        conn.commit()

init_db()

# ── Serve frontend ─────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# ── READ ALL ───────────────────────────────────────────────────────────────────
@app.route("/api/sessions", methods=["GET"])
def get_sessions():
    search = request.args.get("search", "").strip()
    status = request.args.get("status", "").strip()
    with get_db() as conn:
        query = "SELECT * FROM sessions WHERE 1=1"
        params = []
        if search:
            query += " AND (subject LIKE ? OR notes LIKE ?)"
            params += [f"%{search}%", f"%{search}%"]
        if status:
            query += " AND status = ?"
            params.append(status)
        query += " ORDER BY id DESC"
        rows = conn.execute(query, params).fetchall()
    return jsonify([dict(r) for r in rows])

# ── READ ONE ───────────────────────────────────────────────────────────────────
@app.route("/api/sessions/<int:sid>", methods=["GET"])
def get_session(sid):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
    if not row:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(dict(row))

# ── CREATE ─────────────────────────────────────────────────────────────────────
@app.route("/api/sessions", methods=["POST"])
def create_session():
    data = request.json or {}
    subject  = data.get("subject", "").strip()
    duration = data.get("duration", 25)
    notes    = data.get("notes", "").strip()
    status   = data.get("status", "Pending")
    date     = data.get("date", "")
    if not subject or not date:
        return jsonify({"error": "subject and date are required"}), 400
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO sessions (subject, duration, notes, status, date) VALUES (?,?,?,?,?)",
            (subject, int(duration), notes, status, date)
        )
        conn.commit()
        row = conn.execute("SELECT * FROM sessions WHERE id=?", (cur.lastrowid,)).fetchone()
    return jsonify(dict(row)), 201

# ── UPDATE ─────────────────────────────────────────────────────────────────────
@app.route("/api/sessions/<int:sid>", methods=["PUT"])
def update_session(sid):
    data = request.json or {}
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
        if not row:
            return jsonify({"error": "Session not found"}), 404
        e = dict(row)
        subject  = data.get("subject",  e["subject"])
        duration = data.get("duration", e["duration"])
        notes    = data.get("notes",    e["notes"])
        status   = data.get("status",   e["status"])
        date     = data.get("date",     e["date"])
        conn.execute(
            "UPDATE sessions SET subject=?, duration=?, notes=?, status=?, date=? WHERE id=?",
            (subject, int(duration), notes, status, date, sid)
        )
        conn.commit()
        updated = conn.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
    return jsonify(dict(updated))

# ── DELETE ─────────────────────────────────────────────────────────────────────
@app.route("/api/sessions/<int:sid>", methods=["DELETE"])
def delete_session(sid):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM sessions WHERE id=?", (sid,)).fetchone()
        if not row:
            return jsonify({"error": "Session not found"}), 404
        conn.execute("DELETE FROM sessions WHERE id=?", (sid,))
        conn.commit()
    return jsonify({"message": "Session deleted"})

# ── STATS ──────────────────────────────────────────────────────────────────────
@app.route("/api/stats", methods=["GET"])
def get_stats():
    with get_db() as conn:
        total    = conn.execute("SELECT COUNT(*) FROM sessions").fetchone()[0]
        done     = conn.execute("SELECT COUNT(*) FROM sessions WHERE status='Completed'").fetchone()[0]
        mins     = conn.execute("SELECT COALESCE(SUM(duration),0) FROM sessions WHERE status='Completed'").fetchone()[0]
        subjects = conn.execute("SELECT COUNT(DISTINCT subject) FROM sessions").fetchone()[0]
    return jsonify({"total": total, "completed": done, "minutes": mins, "subjects": subjects})

if __name__ == "__main__":
     app.run(host="0.0.0.0", port=5000)
