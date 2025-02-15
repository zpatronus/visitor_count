from flask import Flask, abort, request
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

CORS(
    app,
    supports_credentials=True,
    resources={
        r"/*": {
            "origins": [
                "https://zijuny.dev",
                "https://zjyang.dev",
                "https://goa.zijuny.dev",
                "https://ekatheria.me",
            ]
        }
    },
)


def init_db():
    """Initialize the database if it doesn't exist."""
    conn = sqlite3.connect("visitor_count.db")
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


@app.route("/visitor_count/<string:website_name>/", methods=["GET"])
def visitor_count(website_name):
    """Get or increase the visitor count for a specific website."""
    conn = sqlite3.connect("visitor_count.db")
    cursor = conn.cursor()

    # Check if the website exists in the database
    cursor.execute("SELECT count FROM websites WHERE name = ?", (website_name,))
    result = cursor.fetchone()

    if result is None:
        conn.close()
        abort(404, description="Website not found")

    # If 'inspectonly' argument is present, return the current count
    if "inspectonly" in request.args:
        conn.close()
        return str(result[0])

    # Increment the count
    new_count = result[0] + 1
    cursor.execute(
        "UPDATE websites SET count = ? WHERE name = ?",
        (new_count, website_name),
    )
    conn.commit()
    conn.close()

    return str(new_count)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
