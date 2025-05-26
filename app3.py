import streamlit as st
import sqlite3  # For SQLite database connection
import datetime  # For timestamps
import psutil  # Library for CPU usage (moved to top-level)
import pandas as pd # Library for DataFrame (moved to top-level)

# Database connection details (replace with your desired path)
db_path = "access_log.db"

def create_connection():
  """Creates a connection to the SQLite database."""
  conn = None
  try:
    conn = sqlite3.connect(db_path)
    # print("Connected to SQLite database.") # Removed
  except sqlite3.Error as e:
    st.error(f"Error connecting to database: {e}")
  return conn

def create_table(conn):
  """Creates the 'access_logs' table if it doesn't exist."""
  cursor = conn.cursor()
  cursor.execute('''CREATE TABLE IF NOT EXISTS access_logs (
                      timestamp DATETIME,
                      log_message TEXT
                    )''')
  conn.commit()

def store_log(conn, timestamp_str, message, version_accessed):
  """Stores a new log message in the database (if connection provided)."""
  if conn is not None:
    log_entry = f"Accessed {version_accessed} at: {message}"
    cursor = conn.cursor()
    cursor.execute("INSERT INTO access_logs (timestamp, log_message) VALUES (?, ?)", (timestamp_str, log_entry,))
    conn.commit()
  else:
    st.warning("Could not store log message (database connection not available).")

def get_all_logs(conn):
  """Fetches all logs from the access_logs table."""
  if conn is not None:
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, log_message FROM access_logs ORDER BY timestamp DESC")
    logs_data = cursor.fetchall()
    if logs_data:
      df_logs = pd.DataFrame(logs_data, columns=["Timestamp", "Log Message"])
      return df_logs
  return pd.DataFrame(columns=["Timestamp", "Log Message"]) # Return empty DataFrame if no logs or no connection

def get_system_cpu_info():
  """Fetches CPU usage and logical core count."""
  cpu_usage = psutil.cpu_percent()
  logical_cores = psutil.cpu_count(logical=True)
  return cpu_usage, logical_cores

def main():
  """Main function for the Streamlit app."""
  # Select version from dropdown (replace with your desired version names)
  version_options = ["Version 1", "Version 2", "Version 3 (Database Log)"]
  selected_version = st.selectbox("Select Version", version_options)

  # Get database connection using 'with' statement (recommended)
  with create_connection() as conn:
    create_table(conn)  # Create table within the 'with' block

    # Handle specific version functionalities
    if selected_version == "Version 1":
      # Your Version 1 content here (e.g., display sample text)
      st.title('Simple Text App')
      st.write("Hello, World!")

    elif selected_version == "Version 2":
      # Your Version 2 content here (e.g., display OS information)
      # import psutil  # Library for CPU usage - Moved to top level

      # def get_cpu_info(): # Refactored to get_system_cpu_info at top level
      #   """Fetches CPU usage and logical core count."""
      #   cpu_usage = psutil.cpu_percent()
      #   logical_cores = psutil.cpu_count(logical=True)
      #   return cpu_usage, logical_cores

      st.title('System CPU Information')
      cpu_usage, logical_cores = get_system_cpu_info() # Use refactored function
      st.metric("CPU Usage", f"{cpu_usage}%")
      st.metric("Logical CPU Cores", logical_cores)

    elif selected_version == "Version 3 (Database Log)":
      # Store access log on app load
      current_time_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      # The 'message' part of the log entry for "Version 3" will be the timestamp string itself.
      store_log(conn, current_time_str, current_time_str, "Version 3")

      # Your Version 3 content here (if any)
      st.title('Access Logged App')
      
      df_logs = get_all_logs(conn) # Now returns a DataFrame
      if not df_logs.empty:
        # Create a DataFrame for better display
        # import pandas as pd # Moved to top level
        # df_logs = pd.DataFrame(logs, columns=["Timestamp", "Log Message"]) # Handled in get_all_logs
        st.dataframe(df_logs)
      else:
        st.info("No access logs found.")
      # ... (add your app elements)

if __name__ == '__main__':
  main()
