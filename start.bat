@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
 echo Can cai Python 3.12 ban 64 bit truoc. Xem README.md.
 pause
 exit /b 1
)
if not exist .venv\Scripts\python.exe py -3.12 -m venv .venv
if errorlevel 1 goto failed
.venv\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 goto failed
if not exist data\mart.sqlite3 (
 set MART_ADMIN_PASSWORD=MartDemo!2026
 set MART_CASHIER_PASSWORD=Cashier!2026
 .venv\Scripts\python.exe seed.py
 if errorlevel 1 goto failed
)
start "" http://127.0.0.1:8000
.venv\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
pause
exit /b 0
:failed
echo Khong khoi dong duoc. Xem thong bao loi ben tren va README.md.
pause
exit /b 1
