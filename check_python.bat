@echo off
echo ===================================================================
echo 🐍 Python Installation Check
echo ===================================================================
echo.

echo 🔍 Checking different Python commands...
echo.

echo 1. Trying 'python':
python --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ 'python' command works
) else (
    echo ❌ 'python' command not found
)

echo.
echo 2. Trying 'py':
py --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ 'py' command works
) else (
    echo ❌ 'py' command not found
)

echo.
echo 3. Trying 'python3':
python3 --version 2>nul
if %errorlevel% equ 0 (
    echo ✅ 'python3' command works
) else (
    echo ❌ 'python3' command not found
)

echo.
echo 4. Checking PATH for Python:
where python 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python found in PATH
) else (
    echo ❌ Python not found in PATH
)

echo.
echo 5. Checking for Python Launcher:
where py 2>nul
if %errorlevel% equ 0 (
    echo ✅ Python Launcher found
) else (
    echo ❌ Python Launcher not found
)

echo.
echo ===================================================================
echo 💡 Solutions:
echo 1. Install Python from: https://www.python.org/downloads/
echo 2. During installation, check "Add Python to PATH"
echo 3. Or use Windows Store Python: ms-windows-store://pdp/?productid=9NRWMJP3717K
echo ===================================================================
pause
