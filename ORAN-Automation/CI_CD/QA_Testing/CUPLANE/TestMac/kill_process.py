import subprocess

def kill_process(pid,process):
    if pid:
        print(f"Found PID for {process} : {pid}")
        subprocess.run(["kill", pid])
        print(f"Process {process} with PID {pid} killed.")
    else:
        print("Process not found.")

if __name__ == "__main__":
    p1 = subprocess.getoutput("pgrep -o ptp.sh")
    kill_process(p1,"ptp.sh")
    p2 = subprocess.getoutput("pgrep -o l1.sh")
    kill_process(p2,"l1.sh")
    p3 = subprocess.getoutput("pgrep -o l2.sh")
    kill_process(p3,"l2.sh")