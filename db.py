
import os
import psycopg


def get_connection():
    return psycopg.connect(os.environ["DATABASE_URL"])



def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS visits (
                    id SERIAL PRIMARY KEY,
                    visited_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cur.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL DEFAULT ''
                )
            """)



def record_visit():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO visits DEFAULT VALUES RETURNING id"
            )
            return cur.fetchone()[0]


def get_visit_count():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM visits")
            return cur.fetchone()[0]


def create_note(title, content):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id",
                (title, content)
            )
            return cur.fetchone()[0]


def get_notes():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, title, content FROM notes ORDER BY id")
            return [
                {"id": row[0], "title": row[1], "content": row[2]}
                for row in cur.fetchall()
            ]


def update_note(note_id, title, content):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE notes SET title=%s, content=%s WHERE id=%s RETURNING id",
                (title, content, note_id)
            )
            return cur.fetchone() is not None


def delete_note(note_id):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM notes WHERE id=%s RETURNING id",
                (note_id,)
            )
            return cur.fetchone() is not None