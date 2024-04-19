import subprocess

import psutil
import time


def run_python_script_and_monitor(script_path):
    # Start the Python script as a separate process
    command = f"python {script_path}"
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
    time.sleep(1)

    try:
            p = psutil.Process(process.pid)
            files = p.open_files()
            connections = p.connections()
            process_info = {
                'opened_files': [f.path for f in files],
                'network_connections': [
                    f"{conn.laddr.ip}:{conn.laddr.port} -> {conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else f"{conn.laddr.ip}:{conn.laddr.port}"
                    for conn in connections],
            }

            # Wait for the process to complete
            stdout, stderr = process.communicate()

            process_info['stdout'] = stdout
            process_info['stderr'] = stderr
            process_info['exit_code'] = process.returncode

            print(process_info)
    except Exception as e:
            print(f"An error occurred: {e}")
# Example usage:
script_path = "./toAnalyze.py"  # Make sure to specify the correct path
run_python_script_and_monitor(script_path)
