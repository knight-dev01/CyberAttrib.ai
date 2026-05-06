Write-Host "Starting CyberAttrib.AI Backend Server on port 8000..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath "powershell" -ArgumentList "-Command .\venv\Scripts\Activate.ps1; uvicorn backend.main:app --host 0.0.0.0 --port 8000"

Write-Host "Starting CyberAttrib.AI Frontend Server on port 8080..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath "powershell" -ArgumentList "-Command cd frontend; python -m http.server 8080"

Write-Host "Both servers are running." -ForegroundColor Green
Write-Host "Frontend: http://localhost:8080" -ForegroundColor Yellow
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "Press Ctrl+C in their respective windows or close powershell to stop them."
