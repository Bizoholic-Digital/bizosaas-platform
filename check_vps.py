import pty
import os
import time
import sys

HOST = "194.238.16.237"
USER = "root"
PASS = "&k3civYG5Q6YPb"  # Note: Special chars might need handling

def run_ssh_command(cmd):
    print(f"Running: {cmd}")
    pid, fd = pty.fork()
    
    if pid == 0:
        # Child process
        # Use StrictHostKeyChecking=no to avoid yes/no prompt for new hosts
        os.execlp("ssh", "ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", f"{USER}@{HOST}", cmd)
    else:
        # Parent process
        # Wait for password prompt availability (crude but often effective)
        time.sleep(2) 
        
        # Send password
        os.write(fd, (PASS + "\n").encode())
        
        # Read output
        output_data = b""
        while True:
            try:
                # Read chunks
                chunk = os.read(fd, 1024)
                if not chunk:
                    break
                output_data += chunk
            except OSError:
                break
        
        # Close the file descriptor
        os.close(fd)
        
        # Wait for child
        os.waitpid(pid, 0)
        
        return output_data.decode('utf-8', errors='ignore')

if __name__ == "__main__":
    # Commands to check implementation
    commands = [
        "uptime",
        "cat /etc/os-release",
        "docker ps --format '{{.Names}} {{.Status}} {{.Ports}}'",
        "ls -la"
    ]
    
    for cmd in commands:
        print(f"\n--- EXEC: {cmd} ---")
        out = run_ssh_command(cmd)
        # Filter out the password echoing if possible, or just print
        print(out)
