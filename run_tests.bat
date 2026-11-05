@echo off
title Restaurant Order Management System - Automated Test Verification
cd /d "%~dp0"
echo ====================================================
echo  Executing All 4 Verification Test Cases...
echo ====================================================
python test_cases_runner.py
pause
