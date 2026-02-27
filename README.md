# Web Scraping Tool 🕷️

A configurable, self-hosted web monitoring tool built with Python and Flask. Define target URLs, CSS selectors, and schedules to track changes on any website. Receive notifications and view history through a clean, modern web interface.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Status](https://img.shields.io/badge/Status-Active-success)

## Features ✨

*   **Easy Job Management:** Add, edit, and delete scraping jobs via a user-friendly Dashboard.
*   **Custom Selectors:** Target specific parts of a page using standard CSS selectors (e.g., `#price`, `.news-item`).
*   **Flexible Scheduling:** Set check intervals in minutes for each job independently.
*   **Change Detection:** Automatically detects changes in content and saves a history of updates.
*   **Manual Trigger:** Run scraping jobs immediately with a single click.
*   **Persistence:** All data is stored locally in a lightweight SQLite database.
*   **Modern UI:** Responsive design using Bootstrap 5 and Bootswatch Zephyr theme.

## Screenshots 📸

*(Add screenshots of the dashboard and results page here)*

## Prerequisites 🛠️

*   Python 3.8 or higher
*   `pip` (Python Package Installer)

## Installation 📦

### macOS / Linux

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/web-scraping-tool.git
    cd web-scraping-tool
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    python3 app/app.py
    ```
    The server will start at `http://127.0.0.1:5000`.

### Windows

1.  Clone the repository and enter the directory.
2.  Create virtual environment: `python -m venv venv`
3.  Activate it: `venv\Scripts\activate`
4.  Install dependencies: `pip install -r requirements.txt`
5.  Run: `python app/app.py`

## Usage 🚀

1.  Open your browser and navigate to `http://127.0.0.1:5000`.
2.  Click **"Add Job"** (or the "New Job" button).
3.  Enter the **URL** of the page you want to monitor.
4.  Enter the **CSS Selector** for the specific element (e.g., `h1` for the main title, `.price` for a product price).
5.  Set the **Interval** in minutes.
6.  Click **"Add Job"**.
7.  The tool will now check the page periodically. You can also click the **Play** icon to run it immediately.
8.  Click the **List** icon to view the history of detected changes.

## Development 💻

To run tests:
```bash
export PYTHONPATH=$PYTHONPATH:.
pytest tests/
```

## License 📄

MIT License
