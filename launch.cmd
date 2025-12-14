
@REM python3 doit etre present dans le path
SET PYTHON_PATH=D:\Python313
SET PATH=%PYTHON_PATH%;%PYTHON_PATH%\scripts;%PATH%

call env\Scripts\activate.bat
python app.py
rem flask --app hello2 run
call env\Scripts\deactivate.bat
pause
