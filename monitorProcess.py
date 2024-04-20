import subprocess
import time


def monitor_process(process_name='toAnalyze.py'):
    # Start the script as a subprocess
    process = subprocess.Popen(['python', process_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    try:
        # Wait for the process to start
        time.sleep(1)

        # Check if process has ended
        if process.poll() is not None:
            print("Process finished")

        print("Checking network connections:")
        ss_command = subprocess.Popen(['ss', '-tnp'],
                                      stdout=subprocess.PIPE)  # use ss linux command, whcih return socket statistics
        connections_output = []

        # get connections for the process
        for line in ss_command.stdout:
            if f'pid={process.pid}' in line.decode():
                connections_output.append(line.decode().strip())

        # Print the network connections
        if connections_output:
            for connection in connections_output:
                print(connection)
        else:
            print("No network connections")

        print("Checking open files:")
        lsof_command = subprocess.Popen(['lsof', '-p', str(process.pid)],
                                        stdout=subprocess.PIPE)  # use lsof linux command, which return open files by a process

        # Print the open files
        files_output = lsof_command.stdout.read().decode().strip()
        if files_output:
            print(files_output)
        else:
            print("No open files")

        # Get the output from the process
        stdout, stderr = process.communicate()
        print("stdout:", stdout.decode().strip())

    finally:  # close everything
        process.stdout.close()
        process.stderr.close()

        process.wait()  # wait for the process to finish
        if lsof_command.poll() is None:
            lsof_command.kill()


monitor_process()
