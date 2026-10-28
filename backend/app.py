
from flask import Flask, jsonify, request
import os
import time
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

REGNO = os.getenv("REGNO", "202401100100083")


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST", "db"),
        dbname=os.getenv("POSTGRES_DB", "festdb"),
        user=os.getenv("POSTGRES_USER", "festuser"),
        password=os.environ["POSTGRES_PASSWORD"],
        connect_timeout=5,
        row_factory=dict_row,
    )


def initialize_database():
    for attempt in range(20):
        try:
            with get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS registrations (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        email VARCHAR(255) NOT NULL UNIQUE,
                        created_at TIMESTAMPTZ DEFAULT NOW()
                    )
                """)
            print("Database table is ready")
            return
        except psycopg.OperationalError:
            if attempt == 19:
                raise
            time.sleep(2)


@app.get("/api/health")
def health():
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return jsonify({
            "status": "healthy",
            "regno": REGNO,
            "database": True
        })
    except psycopg.Error:
        return jsonify({
            "status": "unhealthy",
            "regno": REGNO,
            "database": False
        }), 503


@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip().lower()

    if not name or not email:
        return jsonify({"error": "Name and email are required"}), 400

    try:
        with get_connection() as conn:
            row = conn.execute("""
                INSERT INTO registrations (name, email)
                VALUES (%s, %s)
                RETURNING id, name, email, created_at
            """, (name, email)).fetchone()

        return jsonify(row), 201

    except psycopg.errors.UniqueViolation:
        return jsonify({"error": "Email already registered"}), 409
    except psycopg.Error:
        app.logger.exception("Registration database error")
        return jsonify({"error": "Database error"}), 500


@app.get("/api/registrations")
def registrations():
    try:
        with get_connection() as conn:
            rows = conn.execute("""
                SELECT id, name, email, created_at
                FROM registrations
                ORDER BY id
            """).fetchall()

        return jsonify(rows)
    except psycopg.Error:
        app.logger.exception("Could not retrieve registrations")
        return jsonify({"error": "Database error"}), 500


@app.get("/")
def home():
    return jsonify({"message": "Fest backend", "version": "0.1"})


initialize_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
