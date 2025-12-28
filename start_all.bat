@echo off
REM Start backend (FastAPI) in a new window
start "Backend" cmd /k "cd /d %~dp0 && uvicorn api:app --reload --port 8001"

REM Start frontend (Vite) in a new window
start "Frontend" cmd /k "cd /d %~dp0 && cd frontend && npm run dev -- --host"
