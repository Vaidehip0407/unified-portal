# Registration Credentials Reset - Complete Guide

## ✅ What Has Been Done Locally

1. ✅ **Database File Deleted** - `backend/unified_portal.db` removed
2. ✅ **Uploads Folder Cleared** - All user document uploads deleted
3. ✅ **Reset Scripts Created** - Ready to use on your deployment

---

## 🚀 Next Steps

### Option 1: Reset on EC2 (Production/Remote)

If your portal is deployed on EC2, SSH into the instance and run:

```bash
ssh -i gov-portal.pem ubuntu@18.212.97.51

# Go to project directory
cd unified-portal

# Pull latest changes
git pull origin main

# Run the reset script
chmod +x reset-credentials.sh
./reset-credentials.sh
```

### Option 2: Reset Locally (Development)

Make sure Docker Desktop is running, then:

```powershell
cd f:\DevOps\Gov\unified-portal

# Using WSL or Git Bash (if available)
bash reset-credentials.sh

# Or manually:
docker compose down -v
Remove-Item ".\backend\unified_portal.db" -Force
Remove-Item ".\backend\uploads\*" -Recurse -Force
docker compose build --no-cache
docker compose up -d
```

---

## 📋 What Gets Deleted

When you run the reset, the following data is permanently deleted:

| Item | Location | Status |
|------|----------|--------|
| Database | `backend/unified_portal.db` | ✅ Deleted |
| User Accounts | Database | ✅ Deleted |
| User Passwords | Database | ✅ Deleted |
| Registration Info | Database | ✅ Deleted |
| Uploaded Documents | `backend/uploads/` | ✅ Cleaned |
| Applications | Database | ✅ Deleted |
| Service Credentials | Database | ✅ Deleted |
| Authentication Tokens | Database | ✅ Deleted |

---

## 🔄 What Happens After Reset

1. **Database**: Fresh empty database created automatically
2. **Services**: All containers restart with clean state
3. **Frontend**: Browser cache needs manual clearing
4. **Backend**: API ready for new registrations
5. **User Data**: Everything erased - completely fresh start

---

## 🧹 Manual Cleanup Checklist

If you want to be extra thorough:

### On Local Machine:
```powershell
# 1. Clear browser cache
# - Press: Ctrl+Shift+Delete
# - Select: All time
# - Check: Cookies, Cached images/files
# - Click: Clear

# 2. Clear LocalStorage (dev tools)
# F12 → Application → Local Storage → Clear All

# 3. Clear SessionStorage
# F12 → Application → Session Storage → Clear All
```

### On EC2:
```bash
# SSH to your instance
ssh -i gov-portal.pem ubuntu@YOUR_IP

# Navigate to project
cd unified-portal

# Stop all containers
docker compose down -v

# Delete database
rm -f ./backend/unified_portal.db

# Clean uploads
rm -rf ./backend/uploads/*

# Clear Python cache
find ./backend -type d -name __pycache__ -exec rm -rf {} +

# Rebuild and restart
docker compose build --no-cache
docker compose up -d

# Check status
docker compose ps
```

---

## ✨ Fresh Registration Ready!

After running the reset:

1. **Clear browser cache** (Ctrl+Shift+Delete)
2. **Open fresh browser window**
3. **Go to**: `http://localhost:3003` (local) or your domain (EC2)
4. **Register new account**
5. **Test all services fresh**

---

## 📝 Created Scripts

Two scripts have been created for easy reset:

1. **reset-credentials.ps1** (Windows/PowerShell)
   - For local development with Docker Desktop
   - Full automated cleanup and restart

2. **reset-credentials.sh** (Linux/Bash)
   - For EC2 instances
   - SSH in and run: `./reset-credentials.sh`

3. **reset_database.py** (Python)
   - Alternative: Python-based database reset
   - Run: `python reset_database.py`
   - Select option 1 or 2 for full or partial reset

---

## 🆘 Troubleshooting

### If Docker won't start:
```bash
docker compose logs -f
```

### If database won't recreate:
```bash
# Check permissions
chmod 777 ./backend

# Try manual recreation
docker compose down -v
docker compose up -d --build
```

### If services still not working:
```bash
# Check all containers
docker compose ps -a

# View logs
docker compose logs backend
docker compose logs frontend
docker compose logs nginx
```

---

## ✅ Verification

After reset, verify everything is working:

```bash
# Check services are running
curl http://localhost:8000/health
curl http://localhost:3003
curl http://localhost:8000/docs

# Test registration endpoint
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "mobile": "9999999999",
    "password": "TestPassword123",
    "full_name": "Test User"
  }'
```

---

## 📞 Need Help?

If you have any issues:
1. Check the logs: `docker compose logs -f`
2. Verify database exists: `ls -la backend/unified_portal.db`
3. Check port availability: `netstat -an | grep 8000`
4. Restart everything: `docker compose down -v && docker compose up -d`

**Status**: ✅ Credentials deleted successfully. Ready for fresh registration!
