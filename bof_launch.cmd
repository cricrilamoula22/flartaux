
@REM python3 doit etre present dans le path
SET PYTHON_PATH=D:\Python313
SET PATH=%PYTHON_PATH%;%PYTHON_PATH%\scripts;%PATH%

call env\Scripts\activate.bat
rem pip install -r D:\flask_apps\fintrack_project_adl-main\requirements.txt
rem cd /d D:\flask_apps\fintrack_project_adl-main
rem .\env\Scripts\pip install -r requirements.txt

rem python -m flask db init
rem python -m flask db migrate -m
rem python -m flask db upgrade

python app.py
rem call env\Scripts\cmd.bat

rem flask --app hello2 run
call env\Scripts\deactivate.bat
pause
