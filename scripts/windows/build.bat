python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt


pyinstaller --onefile --hidden-import=PIL._tkinter_finder --windowed --name=Catwalk --icon=assets\catwalk.ico src\catwalk.py
