# Reset Registration Credentials - Start Fresh
# This script will delete all user data, credentials, and reset the system

Write-Host "Deleting all registration credentials..." -ForegroundColor Red
Write-Host "WARNING: This will delete ALL user data, registrations, and credentials!" -ForegroundColor Yellow
Write-Host ""

# Confirmation
$confirm = Read-Host "Are you sure? Type 'YES' to continue"
if ($confirm -ne "YES") {
    Write-Host "Operation cancelled" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "1. Stopping Docker containers..." -ForegroundColor Cyan
docker-compose down -v

Write-Host ""
Write-Host "2️⃣  Deleting database file..." -ForegroundColor Cyan
$dbPath = ".\backend\unified_portal.db"
if (Test-Path $dbPath) {
    Remove-Item $dbPath -Force
    Write-Host "Database deleted: $dbPath" -ForegroundColor Green
} else {
    Write-Host "Database file not found (already clean)" -ForegroundColor Gray
}

Write-Host ""
Write-Host "2. Cleaning uploads folder..." -ForegroundColor Cyan
$uploadsPath = ".\backend\uploads"
if (Test-Path $uploadsPath) {
    Remove-Item "$uploadsPath\*" -Recurse -Force
    Write-Host "Uploads folder cleared" -ForegroundColor Green
} else {
    Write-Host "Uploads folder doesn't exist" -ForegroundColor Gray
}

Write-Host ""
Write-Host "3. Clearing browser cache and storage..." -ForegroundColor Cyan
Write-Host "Tip: Clear your browser cache/storage (Ctrl+Shift+Delete)" -ForegroundColor Gray

Write-Host ""
Write-Host "4. Rebuilding containers from scratch..." -ForegroundColor Cyan
docker-compose build --no-cache

Write-Host ""
Write-Host "5. Starting fresh services..." -ForegroundColor Cyan
docker-compose up -d

Write-Host ""
Write-Host "Waiting for services to be ready..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

Write-Host ""
Write-Host "6. Checking service status..." -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "DONE! System is ready for fresh registration" -ForegroundColor Green
Write-Host ""
Write-Host "Access points:" -ForegroundColor Cyan
Write-Host "   Frontend:  http://localhost:3003" -ForegroundColor White
Write-Host "   Backend:   http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs:  http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "   1. Clear browser cache (Ctrl+Shift+Delete)" -ForegroundColor White
Write-Host "   2. Open http://localhost:3003 in a fresh browser" -ForegroundColor White
Write-Host "   3. Register a new account" -ForegroundColor White
Write-Host ""
