REM Jalankan file ini untuk memulai aplikasi MKIT Trimmer
REM Pastikan sudah install Python dan uvicorn
REM Cukup klik dua kali file ini

@ECHO OFF
uv sync
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info --reload
