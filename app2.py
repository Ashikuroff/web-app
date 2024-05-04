import streamlit as st
import psutil
import re
import subprocess

def get_cpu_info():
  """Fetches CPU usage and core count (using system_profiler)."""
  cpu_usage = psutil.cpu_percent()
  # Use system_profiler to get number of cores
  output = subprocess.check_output(['system_profiler', 'SPHardwareDataType', '-detailLevel', 'mini'])
  cores_match = re.search(r'(?<=Logical Cores): (\d+)', output.decode('utf-8'))
  if cores_match:
    cpu_cores = int(cores_match.group(1))
  else:
    cpu_cores = "Unknown"

  return cpu_usage, cpu_cores

# Title for your app
st.title('System CPU Information (macOS)')

# Get CPU information
cpu_usage, cpu_cores = get_cpu_info()

# Display CPU usage metric
st.metric("CPU Usage", f"{cpu_usage}%")

# Display CPU cores information
st.write(f"Number of Logical Cores: {cpu_cores}")
