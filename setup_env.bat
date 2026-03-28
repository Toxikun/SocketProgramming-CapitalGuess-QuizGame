@echo off
echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment and installing requirements...
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo Environment setup is complete!
echo To activate the environment manually in the future, run:
echo venv\Scripts\activate
pause
