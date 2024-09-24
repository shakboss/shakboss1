import subprocess
import json
import os
import time

def run_v2ray(shakboss1):
    # Ensure the V2Ray executable is in your PATH or provide the full path
    v2ray_executable = "v2ray"  # Change this if necessary

    # Check if the config file exists
    if not os.path.isfile(shakboss1):
        print("Configuration file not found.")
        return

    # Start the V2Ray process
    process = subprocess.Popen([v2ray_executable, "-config", shakboss1])
    
    try:
        # Keep the script running
        print("V2Ray client is running. Press Ctrl+C to exit.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping V2Ray client...")
        process.terminate()
        process.wait()
        print("V2Ray client stopped.")

if __name__ == "__main__":
    shakboss1 = "config.json"  # Path to your V2Ray config file
    run_v2ray(shakboss1)
