import unittest
from unittest.mock import patch, MagicMock
import sqlite3
import os
import sys

# Add the parent directory to sys.path to allow importing app3
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app3 # Import the module to be tested

class TestApp3(unittest.TestCase):

    def test_get_cpu_info_in_app3(self):
        # This test is for the get_cpu_info function that is now part of app3's Version 2.
        # We need to ensure app3.get_cpu_info (or the equivalent logic) is callable and returns expected types.
        # Since the actual get_cpu_info function is nested within main() in app3.py,
        # we might need to refactor app3.py slightly to make it testable, or test via mocking streamlit elements if it's tightly coupled.
        # For now, let's assume we can call a refactored or accessible version of get_cpu_info.
        # If app3.get_cpu_info is not directly accessible, this test might need adjustment or the subtask might need to refactor app3.py.

        # Mocking psutil functions
        with patch('psutil.cpu_percent') as mock_cpu_percent,                  patch('psutil.cpu_count') as mock_cpu_count:

            mock_cpu_percent.return_value = 55.5
            mock_cpu_count.return_value = 4

            # Assuming app3.main() initializes and calls the relevant part for Version 2,
            # or that we have a direct way to call the CPU info logic.
            # This is a placeholder for how one might test the CPU info logic.
            # Direct invocation of the internal get_cpu_info might be tricky without refactoring.
            # For this subtask, we'll focus on the database part first, as it's more straightforward.
            # And create a placeholder for CPU test.
            
            # The CPU info logic has been refactored into app3.get_system_cpu_info()
            cpu_usage, cpu_cores = app3.get_system_cpu_info()
            
            self.assertEqual(cpu_usage, 55.5)
            self.assertEqual(cpu_cores, 4)
            mock_cpu_percent.assert_called_once()
            mock_cpu_count.assert_called_once_with(logical=True)

    @patch('app3.create_connection')
    def test_store_log(self, mock_create_connection):
        # Use an in-memory SQLite database for testing
        mock_conn = sqlite3.connect(':memory:')
        mock_create_connection.return_value = mock_conn

        app3.create_table(mock_conn) # Ensure table exists

        test_timestamp = "2023-01-01 12:00:00"
        test_message = "Test log entry for Version Test"
        # app3.store_log now expects (conn, timestamp_str, message, version_accessed)
        app3.store_log(mock_conn, test_timestamp, test_message, "Version Test")

        cursor = mock_conn.cursor()
        # Check against the log_message and also that the timestamp was stored.
        cursor.execute("SELECT log_message, timestamp FROM access_logs WHERE log_message LIKE ?", (f"%{test_message}%",))
        result = cursor.fetchone()

        self.assertIsNotNone(result)
        self.assertIn(test_message, result[0]) # log_message is result[0]
        self.assertIn("Version Test", result[0])
        self.assertEqual(result[1], test_timestamp) # timestamp is result[1]
        
        mock_conn.close()

    def test_get_all_logs(self):
        # Use an in-memory SQLite database for testing
        conn = sqlite3.connect(':memory:')
        app3.create_table(conn) # Ensure table exists

        # Timestamps for testing order
        ts1 = "2023-01-01 10:00:00" # Older
        ts2 = "2023-01-01 10:01:00" # Newer

        # Add test data with explicit timestamps.
        # app3.store_log(conn, timestamp_str, message, version_accessed)
        app3.store_log(conn, ts1, "Log 1", "Version A")
        app3.store_log(conn, ts2, "Log 2", "Version B") # Logged later

        # app3.get_all_logs now returns a pandas DataFrame.
        # The DataFrame columns are "Timestamp" and "Log Message".
        # The query in app3.py is "ORDER BY timestamp DESC".
        logs_df = app3.get_all_logs(conn) 
        self.assertEqual(len(logs_df), 2)

        actual_log_messages = logs_df['Log Message'].tolist()
        actual_timestamps = logs_df['Timestamp'].tolist()

        # "Log 2" (Version B) was logged with ts2 (newer timestamp), so it should be first.
        self.assertEqual(actual_log_messages[0], "Accessed Version B at: Log 2")
        self.assertEqual(actual_timestamps[0], ts2)
        
        # "Log 1" (Version A) was logged with ts1 (older timestamp), so it should be second.
        self.assertEqual(actual_log_messages[1], "Accessed Version A at: Log 1")
        self.assertEqual(actual_timestamps[1], ts1)
        
        conn.close()

if __name__ == '__main__':
    unittest.main()
