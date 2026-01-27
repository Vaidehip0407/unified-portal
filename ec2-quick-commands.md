# 🚀 EC2 Quick Commands - Login Fix Deployment

## 1. Connect to EC2
```bash
ssh -i "your-key.pem" ubuntu@your-ec2-ip
cd ~/unified-portal
```

## 2. One-Command Deployment
```bash
chmod +x ec2-deploy-login-fix.sh
./ec2-deploy-login-fix.sh
```

## 3. Manual Step-by-Step Commands

### Pull Latest Code
```bash
git pull origin main
```

### Rebuild and Deploy
```bash
# Stop containers
docker-compose down

# Remove old images (force rebuild)
docker rmi unified-portal-frontend unified-portal-backend

# Build and start
docker-compose up -d --build

# Wait and check
sleep 15
docker ps
```

### Create Test User
```bash
python3 create-test-user-ec2.py
```

### Test Login API
```bash
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123"
```

## 4. Troubleshooting Commands

### Check Logs
```bash
# Backend logs
docker logs unified-portal-backend --tail 20

# Frontend logs  
docker logs unified-portal-frontend --tail 20

# Nginx logs
docker logs unified-portal-nginx --tail 20
```

### Fix Nginx Issues
```bash
chmod +x fix-nginx-ec2.sh
./fix-nginx-ec2.sh
```

### Restart Specific Container
```bash
docker-compose restart nginx
docker-compose restart backend
docker-compose restart frontend
```

### Check Container Health
```bash
docker exec unified-portal-backend curl -f http://localhost:8000/health
docker exec unified-portal-nginx wget -q --spider http://backend:8000/health
```

## 5. Login Credentials
- **Email:** test@example.com
- **Password:** test123

## 6. Get Public IP
```bash
curl -s http://169.254.169.254/latest/meta-data/public-ipv4
```

## 7. Emergency Commands

### Complete Reset
```bash
docker-compose down
docker system prune -f
docker-compose up -d --build
```

### Check All Services
```bash
# Check if all ports are accessible
curl -I http://localhost:8000/health  # Backend
curl -I http://localhost:3003         # Frontend  
curl -I http://localhost/             # Nginx
```