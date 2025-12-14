rem �diter en cp850 ou 437
REM python3 doit �tre install� et pr�sent dans le path
SET PYTHON_PATH=D:\Python313
SET PATH=%PYTHON_PATH%;%PYTHON_PATH%\scripts;%PATH%

rem pip --proxy http://100.78.40.201:8080 install virtualenv
REM creation de l'environnement venv
python -m venv env
pip install -r requirements.txt
pause


