@echo off
pushd "%~dp0"

echo Installing dependencies from requirements.txt...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo Dependencies installed.
popd
