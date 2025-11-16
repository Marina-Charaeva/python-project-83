import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def add_url(url):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO urls (name) VALUES (%s) RETURNING id",
            (url,)
        )
        url_id = cur.fetchone()[0]
        conn.commit()
        return url_id
    except psycopg2.IntegrityError:
        conn.rollback()
        cur.execute("SELECT id FROM urls WHERE name = %s", (url,))
        result = cur.fetchone()
        return result[0] if result else None
    finally:
        cur.close()
        conn.close()


def get_url_by_id(url_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE id = %s", (url_id,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def get_url_by_name(url):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM urls WHERE name = %s", (url,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def get_all_urls():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT urls.*, 
               MAX(url_checks.created_at) as last_check,
               url_checks.status_code
        FROM urls 
        LEFT JOIN url_checks ON urls.id = url_checks.url_id
        GROUP BY urls.id, url_checks.status_code
        ORDER BY urls.id DESC
    """)
    urls = cur.fetchall()
    cur.close()
    conn.close()
    return urls


def add_url_check(url_id, status_code=None, h1=None, title=None, description=None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO url_checks 
        (url_id, status_code, h1, title, description) 
        VALUES (%s, %s, %s, %s, %s)""",
        (url_id, status_code, h1, title, description)
    )
    conn.commit()
    cur.close()
    conn.close()


def get_url_checks(url_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM url_checks 
        WHERE url_id = %s 
        ORDER BY id DESC
    """, (url_id,))
    checks = cur.fetchall()
    cur.close()
    conn.close()
    return checks