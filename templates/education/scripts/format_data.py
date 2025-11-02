# scripts/format_data.py
import psycopg2
import os

DB_NAME = "education_db"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = os.getenv("DB_PASSWORD")

def format_data():
    conn = None
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
        cur = conn.cursor()

        print("Formatting tutors_tutor...")
        cur.execute("""
            UPDATE tutors_tutor
            SET 
                name = TRIM(name),
                email = LOWER(TRIM(email)),
                phone = REGEXP_REPLACE(phone, '[^0-9]', '', 'g'),
                description = TRIM(description),
                course_subject = INITCAP(TRIM(course_subject))
            WHERE name IS NOT NULL;
        """)

        print("Formatting schools_school...")
        cur.execute("""
            UPDATE schools_school
            SET 
                title = TRIM(title),
                address = TRIM(address),
                district = TRIM(district),
                office_hr = TRIM(office_hr)
            WHERE title IS NOT NULL;
        """)

        print("Formatting courses_course...")
        cur.execute("""
            UPDATE courses_course
            SET 
                title = TRIM(title),
                description = TRIM(description),
                subject = INITCAP(TRIM(subject)),
                district = TRIM(district),
                class_time = TRIM(class_time)
            WHERE title IS NOT NULL;
        """)

        conn.commit()
        print("All data formatted successfully!")

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
    format_data()