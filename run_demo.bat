@echo off
setlocal

pushd "%~dp0"

echo Starting FastAPI backend...
start "Pharm-Drive API" cmd /k "python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

timeout /t 2 /nobreak >nul

echo Launching Streamlit demo...
streamlit run ui.py --server.headless true --server.port 8501

popd
