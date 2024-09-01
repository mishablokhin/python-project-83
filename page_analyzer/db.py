import os
import psycopg2
from psycopg2.extras import NamedTupleCursor
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def open_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


def close_connection(conn):
    conn.close()


def commit_changes(conn):
    conn.commit()


def is_url_already_exists(conn, url):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id FROM urls WHERE name = %s", (url,))
        return cursor.fetchone() is not None


def get_all_urls(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute("SELECT * FROM urls ORDER BY created_at DESC")
        return cursor.fetchall()


def add_new_url_to_db(conn, url):
    with conn.cursor() as cursor:
        current_date = datetime.now().strftime('%Y-%m-%d')
        cursor.execute(
            "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
            (url, current_date)
        )
        new_id = cursor.fetchone()[0]
        commit_changes(conn)
        return new_id


def get_url_info_by_id(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            "SELECT * FROM urls WHERE id = %s",
            (int(id),)
        )
        print(f"Executing query with id: {id} of type {type(id)}")
        return cursor.fetchone()


def get_url_checks_by_id(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            """
            SELECT * FROM url_checks
            WHERE url_id = %s
            ORDER BY created_at DESC, id DESC
            """,
            (id)
        )
        return cursor.fetchall()


def add_url_check(conn, id, h1, title, description):
    current_date = datetime.now().strftime('%Y-%m-%d')
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO url_checks
            (url_id, status_code, h1, title, description, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (id, 200, h1, title, description, current_date)
        )
        commit_changes(conn)


def get_url_name_by_id(conn, id):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            "SELECT name FROM urls WHERE id = %s",
            (id)
        )
        return cursor.fetchone()[0]


def get_latest_url_check(conn):
    with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
        cursor.execute(
            """
            SELECT DISTINCT ON (url_id) url_id, status_code, created_at
            FROM url_checks
            ORDER BY url_id, created_at DESC;
            """
        )
        return cursor.fetchall()
