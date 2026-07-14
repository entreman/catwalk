# ensure to be in an activated virtual environment and have requirements installed. 
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt


# build binary
pyinstaller \
  --onefile \
  --hidden-import=PIL._tkinter_finder \
  --windowed \
  --add-data "assets:assets" \
  src/catwalk.py


