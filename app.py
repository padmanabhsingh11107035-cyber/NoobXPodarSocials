import os
import csv
import sys

try:
    import pymysql
except ImportError:
    print("Missing dependency. Run: pip install pymysql --break-system-packages")
    sys.exit(1)


def get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Missing required environment variable: {name}")
        print("Set it before running this script — see the instructions at the top of this file.")
        sys.exit(1)
    return value


def main():
    host = get_required_env("MYSQL_HOST")
    port = int(os.environ.get("MYSQL_PORT", "3306"))
    user = get_required_env("MYSQL_USER")
    password = get_required_env("MYSQL_PASSWORD")
    database = get_required_env("MYSQL_DATABASE")

    print(f"Connecting to {host}:{port}/{database} ...")
    conn = pymysql.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,
        ssl={"ssl": {}},
    )

    try:
        with conn.cursor() as cur:
            # Deliberately NOT selecting the password column.
            cur.execute(
                """
                SELECT user_id, username, full_name, bio, email, contact_number,
                       account_type, robotics_specialty, age, gender, verified,
                       created_at
                FROM users
                ORDER BY user_id ASC
                """
            )
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]

        output_path = "user_profiles_export.csv"
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

        print(f"Done. Exported {len(rows)} profiles to {output_path}")
        print("Note: passwords were NOT included, by design.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
