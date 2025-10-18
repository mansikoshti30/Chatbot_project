@echo off
echo ========================================
echo   Starting Geospatial Chatbot
echo ========================================
echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Starting server...
echo The chatbot will be available at: http://localhost:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

pause
