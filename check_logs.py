import pty
import os
import time
import sys

HOST = "194.238.16.237"
USER = "root"
PASS = "&k3civYG5Q6YPb"

def run_ssh_command(cmd):
    print(f"\n>>> CMD: {cmd}")
    pid, fd = pty.fork()
    if pid == 0:
        os.execlp("ssh", "ssh", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", f"{USER}@{HOST}", cmd)
    else:
        time.sleep(2)
        os.write(fd, (PASS + "\n").encode())
        output_data = b""
        start_time = time.time()
        while time.time() - start_time < 10: # 10s timeout per command
            try:
                chunk = os.read(fd, 4096)
                if not chunk: break
                output_data += chunk
            except OSError: break
        
        # Determine strict wait or just kill
        try:
            os.kill(pid, 9)
            os.waitpid(pid, 0)
        except: pass
            
        return output_data.decode('utf-8', errors='ignore')

if __name__ == "__main__":
    # Check logs for admin dashboard
    print(run_ssh_command("docker logs --tail 50 bizosaas-admin-dashboard"))
    
    # Check enviroment variables for client portal to see if it points to brain gateway
    # Using docker exec to cat env (assuming 'env' works inside)
    print(run_ssh_command("docker exec client-portal env | grep -E 'API|BRAIN|URL'"))
