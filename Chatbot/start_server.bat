@echo off
echo Starting Task Management HTTP Server...
echo.

REM Change to the Chatbot directory (relative to script location)
cd /d "%~dp0"

echo Installing requirements...
pip install -r requirements.txt

echo.
echo Starting the HTTP server on port 8000...
echo Visit http://localhost:8000/docs to see the API documentation
echo.

REM Start the server using the backend module
python backend/http_server.py