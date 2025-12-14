rem ‚diter en cp850 ou 437
REM python3 doit ˆtre install‚ et pr‚sent dans le path
SET PYTHON_PATH=C:\Python313
SET PATH=%PYTHON_PATH%;%PYTHON_PATH%\scripts;%PATH%
rem cd /d D:\flask_apps\106_flartaux
call .\env\Scripts\activate.bat

REM pour mettre a jour pip :
rem python.exe -m pip --proxy http://100.78.40.201:8080 install --upgrade pip
rem pour desinstller un package => pip uninstall docx
rem python -m pip --proxy http://100.78.40.201:8080 install -r requirements.txt

rem python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt

rem python -m pip freeze > requirements.txt
rem python -m pip install --force-reinstall --no-deps -r requirements.txt

rem python -m pip uninstall docx
rem python -m pip install python-docx

rem python -m flask db init
rem python -m flask db migrate -m
rem python -m flask db upgrade
call .\env\Scripts\deactivate.bat
pause


