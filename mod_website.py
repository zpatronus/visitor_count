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
        cursor.execute("INSERT INTO websites (name, count) VALUES (?, 0)", (website_name,))
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

def main():
    parser = argparse.ArgumentParser(description="Manage websites in the visitor count database.")
    parser.add_argument("action", choices=["add", "delete"], help="Action to perform: add or delete a website.")
    parser.add_argument("website_name", help="Name of the website to add or delete.")

    args = parser.parse_args()

    init_db()

    if args.action == "add":
        add_website(args.website_name)
    elif args.action == "delete":
        delete_website(args.website_name)

if __name__ == "__main__":
    main()