import subprocess
import time

def monitor_process(process_name='toAnalyze.py'):
    # Start the script as a subprocess
    process = subprocess.Popen(['python', process_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        time.sleep(1)

        # Check if process has ended
        if process.poll() is not None:
            print("Process finished")

        print("Checking network connections:")
        ss_command = subprocess.Popen(['ss', '-tnp'], stdout=subprocess.PIPE)
        connections_output = []
        for line in ss_command.stdout:
            if f'pid={process.pid}' in line.decode():
                connections_output.append(line.decode().strip())
        if connections_output:
            for connection in connections_output:
                print(connection)
        else:
            print("No network connections")

        # Using lsof to monitor open files specifically by the subprocess PID
        print("Checking open files:")
        lsof_command = subprocess.Popen(['lsof', '-p', str(process.pid)], stdout=subprocess.PIPE)
        files_output = lsof_command.stdout.read().decode().strip()
        if files_output:
            print(files_output)
        else:
            print("No open files")

        stdout, stderr = process.communicate()
        print("stdout:", stdout.decode().strip())

    finally:
        process.stdout.close()
        process.stderr.close()

        # Wait for the subprocess to exit
        process.wait()
        # Terminate the lsof command if it's still running
        if lsof_command.poll() is None:
            lsof_command.kill()


monitor_process()
