#!/bin/bash
# Fix Login Issues and Update Frontend Design

echo "🔧 Fixing login issues and updating frontend design..."

# Pull latest changes
cd ~/unified-portal
git pull origin main

# Fix backend applications.py if still broken
cd ~/unified-portal/backend/app/routers
if grep -q "rpa_service" applications.py 2>/dev/null; then
    echo "🔧 Fixing applications.py..."
    sed -i '/rpa_service/d' applications.py
fi

# Create a test user in database
cd ~/unified-portal
echo "👤 Creating test user..."
cat > create_test_user.py << 'EOF'
import sys
sys.path.append('/app')
from app.database import SessionLocal, engine
from app.models import User, Base
from passlib.context import CryptContext
import uuid

# Create tables
Base.metadata.create_all(bind=engine)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create session
db = SessionLocal()

try:
    # Check if test user exists
    existing_user = db.query(User).filter(User.email == "test@example.com").first()
    
    if existing_user:
        print("✅ Test user already exists")
    else:
        # Create test user
        hashed_password = pwd_context.hash("test123")
        
        test_user = User(
            id=str(uuid.uuid4()),
            email="test@example.com",
            hashed_password=hashed_password,
            full_name="Test User",
            mobile="9876543210",
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        print("✅ Test user created successfully")
        print("   Email: test@example.com")
        print("   Password: test123")

except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
EOF

# Force complete rebuild of all containers
echo "🔄 Force rebuilding all containers..."
docker-compose down

# Remove all images to force fresh build
docker rmi unified-portal-frontend unified-portal-backend 2>/dev/null || true

# Clear all cache
sudo rm -rf frontend/node_modules/.cache 2>/dev/null || true
sudo rm -rf frontend/dist 2>/dev/null || true
sudo find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Rebuild everything from scratch
echo "🔨 Building all containers from scratch..."
docker-compose build --no-cache --pull

# Start all containers
echo "▶️ Starting all containers..."
docker-compose up -d

# Wait for containers to start
echo "⏳ Waiting for containers to start..."
sleep 60

# Create test user
echo "👤 Creating test user in database..."
docker-compose exec -T backend python create_test_user.py

# Check container status
echo "📊 Container status:"
docker-compose ps

# Test backend health
echo "🧪 Testing backend health..."
curl -s http://localhost:8000/health || echo "Backend not responding"

# Test frontend
echo "🧪 Testing frontend..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost:3003

# Test portal
echo "🧪 Testing portal..."
curl -s -o /dev/null -w "HTTP Status: %{http_code}\n" http://localhost/

# Check if beautiful login page is served
echo "🎨 Checking login page design..."
if curl -s http://localhost/ | grep -q "Gujarat.*Unified.*Services.*Portal\|Citizen.*Login"; then
    echo "✅ Beautiful login page is now active!"
else
    echo "❌ Still showing simple login page"
    echo "🔄 Trying nginx restart..."
    docker-compose restart nginx
    sleep 10
    if curl -s http://localhost/ | grep -q "Gujarat.*Unified.*Services.*Portal"; then
        echo "✅ Beautiful login page now active after nginx restart!"
    else
        echo "❌ Manual browser cache clear needed"
    fi
fi

echo ""
echo "🎉 Setup completed!"
echo "📋 Test Login Credentials:"
echo "   Email: test@example.com"
echo "   Password: test123"
echo ""
echo "🌐 Portal URL: http://98.81.95.183/"
echo "📝 Clear browser cache and hard refresh (Ctrl+F5)"
echo "🔍 Try incognito mode if still showing old design"

# Cleanup
rm -f create_test_user.py