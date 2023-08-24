import os

# Set environment variables if needed (e.g., your secrets)

os.system("gunicorn -w 4 -b 0.0.0.0:5000 trial:app")
