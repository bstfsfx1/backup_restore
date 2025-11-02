import psycopg2
import json
from datetime import datetime
import os

# === CONFIGURATION ===
DB_NAME = "education_db"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Tables and their export settings
EXPORT_CONFIG = [
    {
        "table": "tutors_tutor",
        "file": "tutors_export.json",
        "columns": [
            "id", "name", "photo", "description", "phone", "email",
            "is_mvp", "hire_date", "course_subject", "photo_1", "photo_2", "photo_3", "experience", "rating", "taught_students"
        ],
        "order_by": "id"
    },

    {
        "table": "schools_school",
        "file": "schools_export.json",
        "columns": [
            "id", "title", "address", "district", "room_num",
            "photo_main", "photo_1", "photo_2", "is_published", "office_hr"
        ],
        "order_by": "id"
    },

    {
        "table": "courses_course",
        "file": "courses_export.json",
        "columns": [
            "id", "students_enrolled", "rating", "price", "class_type",
            "created_at", "tutor_id", "title", "class_time", "total_classes",
            "max_students", "photo_1", "photo_2", "photo_3", "photo_main",
            "district", "duration", "subject", "school_id", "description"
        ],
        "order_by": "id"
    }
]

# Secure password prompt
# DB_PASSWORD = getpass(f"Enter password for {DB_USER}@{DB_HOST}:{DB_PORT}: ")

def export_all_data():
    conn = None
    try:
        print(f"Connecting to PostgreSQL database '{DB_NAME}'...")
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        cur = conn.cursor()

        total_exported = 0

        for config in EXPORT_CONFIG:
            table_name = config["table"]
            file_path = config["file"]
            columns = config["columns"]
            order_by = config.get("order_by", "id")

            print(f"\nExporting `{table_name}` → '{file_path}'...")

            # Build SELECT query
            cols_str = ", ".join(columns)
            query = f"SELECT {cols_str} FROM {table_name} ORDER BY {order_by};"

            cur.execute(query)
            rows = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]

            # Convert to list of dicts with proper type handling
            records = []
            for row in rows:
                record = {}
                for i, value in enumerate(row):
                    key = col_names[i]
                    if isinstance(value, datetime):
                        record[key] = value.isoformat()
                    elif value is None:
                        record[key] = ""
                    elif key in ["is_mvp", "is_published"]:
                        record[key] = bool(value)
                    elif key in ["rating", "price"]:
                        record[key] = float(value)
                    elif key in ["id", "students_enrolled", "total_classes", "max_students", "room_num", "duration", "tutor_id", "school_id"]:
                        record[key] = int(value)
                    else:
                        record[key] = str(value)
                records.append(record)

            # Write to JSON file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(records, f, indent=2, ensure_ascii=False, default=str)

            count = len(records)
            total_exported += count
            print(f"Success: {count} record(s) exported to '{file_path}'")

        print(f"\nAll done! Total {total_exported} records exported.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    export_all_data()