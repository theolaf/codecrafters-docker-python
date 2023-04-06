import subprocess
import sys
import os
import tempfile
import shutil
import ctypes

def main():
    command = sys.argv[3]
    args = sys.argv[4:]
    
    with tempfile.TemporaryDirectory() as temp_dir:
        CLONE_NEWPID = 0x20000000
        libc = ctypes.CDLL(None)
        libc.unshare.argtypes = [ctypes.c_int]
        libc.unshare(CLONE_NEWPID)

        os.makedirs(os.path.join(temp_dir, os.path.dirname(command).strip("/")))
        shutil.copy(command, os.path.join(temp_dir, command.strip("/")))
        os.chroot(temp_dir)

        completed_process = subprocess.run([command, *args], capture_output=True)
    
        sys.stdout.write(completed_process.stdout.decode("utf-8"))
        sys.stderr.write(completed_process.stderr.decode("utf-8"))

        sys.exit(completed_process.returncode)

if __name__ == "__main__":
    main()
