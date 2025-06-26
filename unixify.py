#!/usr/bin/env python3
import subprocess
from pathlib import Path

def fix_all_files(directory):
    path = Path(directory)
    for py_file in path.rglob("*.py"):  # recursive search
        # Make the file executable
        py_file.chmod(py_file.stat().st_mode | 0o111)

        # Run dos2unix on the file
        try:
            subprocess.run(["dos2unix", str(py_file)], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to run dos2unix on {py_file}")
    for sh_file in path.rglob("*.sh"):  # recursive search
        # Make the file executable
        sh_file.chmod(sh_file.stat().st_mode | 0o111)

        # Run dos2unix on the file
        try:
            subprocess.run(["dos2unix", str(sh_file)], check=True)
        except subprocess.CalledProcessError:
            print(f"Failed to run dos2unix on {sh_file}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} /path/to/directory")
    else:
        fix_all_files(sys.argv[1])
