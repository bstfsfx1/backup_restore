import psycopg2
import json
import os
from datetime import datetime

# === CONFIGURATION ===
DB_NAME = "education_db"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_PASSWORD = os.getenv("DB_PASSWORD")

# JSON files and their target tables
IMPORT_CONFIG = [
    {
        "file": "tutors_export.json",
        "table": "tutors_tutor",
        "columns": [
            "id", "name", "photo", "description", "phone", "email",
            "is_mvp", "hire_date", "course_subject", "photo_1", "photo_2", "photo_3", "experience", "rating", "taught_students"
        ]
    },
    {
        "file": "schools_export.json",
        "table": "schools_school",
        "columns": [
            "id", "title", "address", "district", "room_num",
            "photo_main", "photo_1", "photo_2", "is_published", "office_hr"
        ]
    },
    {
        "file": "courses_export.json",
        "table": "courses_course",
        "columns": [
            "id", "students_enrolled", "rating", "price", "class_type",
            "created_at", "tutor_id", "title", "class_time", "total_classes",
            "max_students", "photo_1", "photo_2", "photo_3", "photo_main",
            "district", "duration", "subject", "school_id", "description"
        ]
    }
]

# Secure password prompt
# DB_PASSWORD = getpass(f"Enter password for {DB_USER}@{DB_HOST}:{DB_PORT}: ")

def import_all_data():
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
        conn.autocommit = False  # Use transaction
        cur = conn.cursor()

        total_imported = 0

        for config in IMPORT_CONFIG:
            file_path = config["file"]
            table_name = config["table"]
            columns = config["columns"]

            print(f"\nImporting '{file_path}' → `{table_name}`...")

            # Read JSON
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print(f"Warning: File '{file_path}' not found. Skipping.")
                continue
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in '{file_path}': {e}")
                continue

            if not data:
                print(f"No data in '{file_path}'. Skipping.")
                continue

            print(f"Found {len(data)} record(s).")

            # Build placeholders: %s, %s, ...
            placeholders = ", ".join(["%s"] * len(columns))
            cols_str = ", ".join(columns)

            # ON CONFLICT DO UPDATE for upsert
            set_clause = ", ".join([f"{col} = EXCLUDED.{col}" for col in columns if col != "id"])
            insert_query = f"""
                INSERT INTO {table_name} ({cols_str})
                VALUES ({placeholders})
                ON CONFLICT (id) DO UPDATE SET {set_clause};
            """

            imported = 0
            for record in data:
                # Prepare values in column order
                values = []
                for col in columns:
                    val = record.get(col)
                    # Handle special types
                    if val is None:
                        values.append(None)
                    elif col in ["hire_date", "created_at"] and isinstance(val, str):
                        values.append(val)  # Already ISO string
                    elif col == "is_mvp" or col == "is_published":
                        values.append(bool(val))
                    elif col in ["rating", "price"]:
                        values.append(float(val) if val != "" else 0.0)
                    elif col in ["students_enrolled", "total_classes", "max_students", "room_num", "duration", "tutor_id", "school_id"]:
                        values.append(int(val))
                    else:
                        values.append(val)
                try:
                    cur.execute(insert_query, values)
                    imported += 1
                except psycopg2.Error as e:
                    print(f"Failed to insert record ID {record.get('id')}: {e}")
                    conn.rollback()
                    raise

            total_imported += imported
            print(f"Success: {imported} record(s) imported/updated in `{table_name}`.")

        # Commit all
        conn.commit()
        print(f"\nAll done! Total {total_imported} records imported across all tables.")

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    import_all_data()