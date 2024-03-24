from sys import stderr
import subprocess
import re


def remove_color_data(text):
    # Define regex pattern to match ANSI escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    # Remove ANSI escape sequences from the text
    return ansi_escape.sub('', text)


def print_gradually(cmd):
    """
    Run a command and print the output gradually.
    This ensures that the output is printed as the
    command is running in the terminal.

    This is an utility function.

    :param cmd: The command to run
    :type cmd: list
    :raises subprocess.CalledProcessError: If the command fails
    """
    process = subprocess.Popen(
        cmd, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, universal_newlines=True)
    for line in process.stdout:
        print(line, end="")  # Print without newline
    error = False
    error_message = ""
    for line in process.stderr:
        error = True
        print(line, file=stderr, end="")  # Print to stderr without newline
        error_message += remove_color_data(line)
    process.wait()  # Wait for the process to finish
    if error:
        raise subprocess.CalledProcessError(
            process.returncode, cmd, stderr=error_message)
