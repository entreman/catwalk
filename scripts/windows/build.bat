python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt


pyinstaller --onefile --hidden-import=PIL._tkinter_finder --windowed --name=Catwalk --icon=assets\catwalk.ico src\catwalk.py
