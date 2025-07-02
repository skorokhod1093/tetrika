if not exist "env" (
    python3 -m venv env
)

call env\Scripts\activate.bat

if exist "requirements.txt" (
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
)

cmd /k Title python3 env