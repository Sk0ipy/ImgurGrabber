import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from threading import Thread
import asyncio
import itertools
import string
import aiohttp
import mysql.connector.pooling
from datetime import date
from functools import lru_cache

# Database configuration
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_NAME = "imgur"
BASE_URL = "https://i.imgur.com/"
DB_POOL_NAME = "imgur_pool"
DB_POOL_SIZE = 5

# Initialize connection pool
db_config = {
    "host": DB_HOST,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "database": DB_NAME
}
pool = mysql.connector.pooling.MySQLConnectionPool(pool_name=DB_POOL_NAME,
                                                   pool_size=DB_POOL_SIZE,
                                                   **db_config)


# Generate a random string of letters and numbers
def create_string(start_len=5, end_len=8):
    chars = string.ascii_lowercase + string.digits
    for length in range(start_len, end_len + 1):
        for s in itertools.product(chars, repeat=length):
            yield ''.join(s)


# Async HTTP session
async def async_get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return response.history


# Check if the URL is a valid Imgur image asynchronously
async def is_valid_async(url):
    try:
        history = await async_get(url)
        return not history
    except Exception:
        return False


# Add URL to the database
def add_to_database(url):
    conn = pool.get_connection()
    cursor = conn.cursor()
    today = date.today()
    query = "INSERT INTO imgur_photos (url, date_added) VALUES (%s, %s)"
    cursor.execute(query, (url, today))
    conn.commit()
    cursor.close()
    conn.close()


# Use a set for caching
cache = set()


# Memoization for URL checking
@lru_cache(maxsize=10000)
def is_valid_cached(url):
    if url in cache:
        return True
    valid = asyncio.run(is_valid_async(url))
    if valid:
        cache.add(url)
    return valid


# GUI Application
class App:
    def __init__(self, root):
        self.root = root
        root.title("Imgur URL Checker")

        # Styling
        style = ttk.Style(root)
        style.configure('TLabel', font=('Helvetica', 12))

        # Layout using frames
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        # Labels
        self.label_total_checked = ttk.Label(frame, text="Total Checked: 0")
        self.label_total_checked.grid(row=0, column=0, sticky=tk.W, pady=2)

        self.label_valid_urls = ttk.Label(frame, text="Valid URLs: 0")
        self.label_valid_urls.grid(row=1, column=0, sticky=tk.W, pady=2)

        self.label_invalid_urls = ttk.Label(frame, text="Invalid URLs: 0")
        self.label_invalid_urls.grid(row=2, column=0, sticky=tk.W, pady=2)

        # Initialize counters
        self.total_checked = 0
        self.valid_urls = 0
        self.invalid_urls = 0

    def update_counters(self, valid):
        self.total_checked += 1
        if valid:
            self.valid_urls += 1
        else:
            self.invalid_urls += 1

        self.label_total_checked.config(text=f"Total Checked: {self.total_checked}")
        self.label_valid_urls.config(text=f"Valid URLs: {self.valid_urls}")
        self.label_invalid_urls.config(text=f"Invalid URLs: {self.invalid_urls}")


def run_script(app):
    string_generator = create_string()
    while True:
        url = BASE_URL + next(string_generator)
        valid = is_valid_cached(url)
        app.root.after(0, app.update_counters, valid)
        if valid:
            print(f"Valid URL {url}")
            add_to_database(url)
        else:
            print(f"Invalid URL {url}")


def test_run():
    # Test URL
    test_url = "https://i.imgur.com/aQR85cF.png"

    # Check if the URL is valid
    valid = asyncio.run(is_valid_async(test_url))

    # Print the result
    if valid:
        print(f"The URL {test_url} is valid.")
    else:
        print(f"The URL {test_url} is invalid.")
        exit()

def main():
    test_run()
    root = ThemedTk(theme="equilux")  # Using a themed Tkinter window
    app = App(root)

    # Run the script in a separate thread
    thread = Thread(target=run_script, args=(app,))
    thread.daemon = True
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
