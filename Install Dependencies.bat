@echo off
echo Installing Python dependencies...

REM Install Pillow
python -m pip install --upgrade pip
python -m pip install --upgrade pillow

REM Install tqdm
python -m pip install --upgrade tqdm

pause