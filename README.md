# Install dependencies manually
*Note: It is recommended to use the Dockerfile or venv (see below)*
RUN pip install --no-cache-dir -r requirements.txt

# Venv
source venv/bin/activate

# Start application
python app/app.py

# Development
nix-shell -p python3 python3Packages.tkinter
cd app
python -m tests.TESTNAME
