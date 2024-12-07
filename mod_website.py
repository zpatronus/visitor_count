import sqlite3
import argparse

DB_NAME = "visitor_count.db"


def init_db():
    """Initialize the database if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS websites (
            name TEXT PRIMARY KEY,
            count INTEGER DEFAULT 0
        )
        """
    )
    conn.commit()
    conn.close()


def add_website(website_name):
    """Add a new website to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO websites (name, count) VALUES (?, 0)", (website_name,)
        )
        conn.commit()
        print(f"Website '{website_name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Website '{website_name}' already exists in the database.")
    finally:
        conn.close()


def delete_website(website_name):
    """Delete a website from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM websites WHERE name = ?", (website_name,))
    if cursor.rowcount > 0:
        print(f"Website '{website_name}' deleted successfully.")
    else:
        print(f"Website '{website_name}' not found in the database.")
    conn.commit()
    conn.close()


def modify_visitor_count(website_name, new_count):
    """Modify the visitor count for an existing website."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT count FROM websites WHERE name = ?", (website_name,))
    result = cursor.fetchone()

    if result is None:
        print(f"Website '{website_name}' not found in the database.")
    else:
        cursor.execute(
            "UPDATE websites SET count = ? WHERE name = ?",
            (new_count, website_name),
        )
        conn.commit()
        print(
            f"Visitor count for website '{website_name}' updated to {new_count}."
        )
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Manage websites in the visitor count database."
    )
    parser.add_argument(
        "action",
        choices=["add", "delete", "modify"],
        help="Action to perform: add, delete, or modify a website.",
    )
    parser.add_argument(
        "website_name", help="Name of the website to add, delete, or modify."
    )
    parser.add_argument(
        "--new_count",
        type=int,
        help="New visitor count (required for modify action).",
        default=None,
    )

    args = parser.parse_args()

    init_db()

    if args.action == "add":
        add_website(args.website_name)
    elif args.action == "delete":
        delete_website(args.website_name)
    elif args.action == "modify":
        if args.new_count is None:
            print("Error: --new_count is required for the modify action.")
        else:
            modify_visitor_count(args.website_name, args.new_count)


if __name__ == "__main__":
    main()
