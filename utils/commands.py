import subprocess

def run_command(command, description, cwd=None):
    """
    Execute a shell command with a description and optional working directory.

    :param command: The shell command to run.
    :param description: A brief description of the command.
    :param cwd: Optional directory to execute the command in.
    """
    print(f"Running: {description}")
    result = subprocess.run(command, shell=True, text=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        print(f"Failed: {description}\n{result.stderr.strip()}")
        raise RuntimeError(f"Command failed: {description}")
    print(f"Success: {description} completed.")
