# scripts/clear_data.py
import psycopg2
import os

DB_NAME = "education_db"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = os.getenv("DB_PASSWORD")

TABLES = ["courses_course", "schools_school", "tutors_tutor"]

def clear_data():
    conn = None
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        print("Clearing all data...")
        for table in TABLES:
            print(f"  → TRUNCATE {table}...")
            cur.execute(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;")

        conn.commit()
        print("All data cleared successfully!")

    except Exception as e:
        print(f"Error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Connection closed.")

if __name__ == "__main__":
    clear_data()