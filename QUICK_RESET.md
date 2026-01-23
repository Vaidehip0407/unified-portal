# QUICK RESET REFERENCE

## What Was Done ✅
- [x] Database deleted: `backend/unified_portal.db`
- [x] Uploads cleaned: `backend/uploads/`
- [x] All user credentials removed
- [x] Reset scripts created (3 versions)

## Quick Commands

### Local Reset (Windows with Docker Desktop)
```powershell
cd f:\DevOps\Gov\unified-portal
.\reset-credentials.ps1
```

### Local Reset (WSL/Git Bash)
```bash
cd f:\DevOps\Gov\unified-portal
bash reset-credentials.sh
```

### EC2 Reset (SSH)
```bash
ssh -i gov-portal.pem ubuntu@18.212.97.51
cd unified-portal
bash reset-credentials.sh
```

### Manual Reset
```bash
docker compose down -v
docker compose build --no-cache
docker compose up -d
```

## Verification
```bash
# Check services running
docker compose ps

# Check database exists
ls -la backend/unified_portal.db

# Test API
curl http://localhost:8000/health
```

## Browser Cleanup
- **Windows/Linux**: Ctrl+Shift+Delete
- **Mac**: Cmd+Shift+Delete
- Select: "All time"
- Clear: Cookies & cached files

## Status
✅ All credentials deleted
✅ Database fresh and empty
✅ Ready for new registration

## Created Files
1. `reset-credentials.ps1` - Windows automation
2. `reset-credentials.sh` - Linux automation
3. `reset_database.py` - Python database reset
4. `RESET_CREDENTIALS_GUIDE.md` - Full documentation
5. `RESET_CREDENTIALS_REPORT.md` - This report
