#!/bin/bash

echo "🚀 EC2 Deployment Script - Login Fix"
echo "======================================"

echo "Step 1: Pull latest code from GitHub"
git pull origin main

echo -e "\nStep 2: Stop all containers"
docker-compose down

echo -e "\nStep 3: Remove old images to force rebuild"
docker rmi unified-portal-frontend unified-portal-backend 2>/dev/null || true

echo -e "\nStep 4: Build and start containers"
docker-compose up -d --build

echo -e "\nStep 5: Wait for containers to start"
sleep 15

echo -e "\nStep 6: Check container status"
docker ps

echo -e "\nStep 7: Check container health"
echo "Backend health:"
docker exec unified-portal-backend curl -f http://localhost:8000/health || echo "Backend not ready yet"

echo -e "\nFrontend health:"
docker exec unified-portal-frontend curl -f http://localhost:80 || echo "Frontend not ready yet"

echo -e "\nStep 8: Test nginx connectivity"
docker exec unified-portal-nginx wget -q --spider http://backend:8000/health && echo "✅ Nginx → Backend OK" || echo "❌ Nginx → Backend FAILED"
docker exec unified-portal-nginx wget -q --spider http://frontend:80 && echo "✅ Nginx → Frontend OK" || echo "❌ Nginx → Frontend FAILED"

echo -e "\nStep 9: Create test user"
python3 create-test-user-ec2.py

echo -e "\nStep 10: Test login API"
curl -X POST http://localhost/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=test123" \
  && echo -e "\n✅ Login API working!" || echo -e "\n❌ Login API failed"

echo -e "\nStep 11: Get public IP"
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "🌐 Access your portal at: http://$PUBLIC_IP"

echo -e "\nStep 12: Final container status"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

echo -e "\n🎉 Deployment Complete!"
echo "Login credentials:"
echo "  Email: test@example.com"
echo "  Password: test123"
echo "  URL: http://$PUBLIC_IP"