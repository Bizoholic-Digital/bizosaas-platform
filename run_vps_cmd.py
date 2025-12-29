import pty
import os
import time
import sys

HOST = "72.60.98.213"
USER = "root"
PASS = "&k3civYG5Q6YPb"

def run_ssh_command(cmd):
    pid, fd = pty.fork()
    
    if pid == 0:
        os.execlp("ssh", "ssh", "-o", "StrictHostKeyChecking=no", f"{USER}@{HOST}", cmd)
    else:
        # Wait for password prompt
        time.sleep(2) 
        os.write(fd, (PASS + "\n").encode())
        
        output_data = b""
        while True:
            try:
                chunk = os.read(fd, 1024)
                if not chunk:
                    break
                output_data += chunk
            except OSError:
                break
        
        os.close(fd)
        os.waitpid(pid, 0)
        return output_data.decode('utf-8', errors='ignore')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 run_vps_cmd.py '<command>'")
        sys.exit(1)
    
    cmd = sys.argv[1]
    print(run_ssh_command(cmd))
