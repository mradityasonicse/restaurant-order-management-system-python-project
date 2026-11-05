@echo off
title Restaurant Order Management System - Web POS
cd /d "%~dp0"
echo ====================================================
echo  Starting Restaurant Web POS Dashboard...
echo  Opening http://127.0.0.1:5000 in your browser
echo ====================================================
python app.py
pause
