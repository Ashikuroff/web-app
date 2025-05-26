# Python Streamlit Web Application

## Overview

This project is a simple web application built using Python and Streamlit. The main application is `app3.py`, which consolidates all features and functionalities.

## Features

`app3.py` offers a dropdown menu to select between three different versions, each demonstrating a distinct functionality:

1.  **Version 1: Hello World**
    *   Displays a simple "Hello, World!" message.

2.  **Version 2: System CPU Information**
    *   Shows current CPU usage percentage.
    *   Displays the number of logical CPU cores.
    *   This feature is cross-platform and uses the `psutil` library.

3.  **Version 3: Database Logging**
    *   Logs application access events, including the version accessed and a timestamp.
    *   Displays all stored access logs from the database.

## Setup and Installation

1.  **Prerequisites:**
    *   Python 3.x
    *   pip (Python package installer)

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies:**
    Navigate to the project's root directory (where `requirements.txt` is located) and run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install Streamlit, psutil, pandas, and other necessary packages.

## Running the Application

Once the dependencies are installed, you can run the application using Streamlit:

```bash
streamlit run app3.py
```

This will typically open the application in your default web browser.

## Running Tests

The application includes a suite of unit tests located in the `tests` directory. To run the tests:

1.  Ensure you have installed all dependencies from `requirements.txt`.
2.  Navigate to the project's root directory.
3.  Run the following command:
    ```bash
    python -m unittest tests/test_app3.py
    ```
    Alternatively, you can use test discovery:
    ```bash
    python -m unittest discover tests
    ```

## Database

The application uses an SQLite database named `access_log.db` to store access logs for "Version 3". This file will be automatically created in the project root if it doesn't exist when the application is run and "Version 3" is accessed.

---
*This README has been updated to reflect the current project structure and features.*
