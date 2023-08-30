import os
import subprocess

cur_dir = os.path.dirname(__file__)

# Run Gunicorn using subprocess
subprocess.Popen(["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "trial:app"], cwd=cur_dir)