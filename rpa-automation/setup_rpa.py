#!/usr/bin/env python3
"""
RPA Setup Script
Installs and configures RPA automation environment
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(command, description):
    """Run shell command with error handling"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def install_chrome_driver():
    """Install Chrome and ChromeDriver"""
    system = platform.system().lower()
    
    if system == "linux":
        # Ubuntu/Debian
        commands = [
            "sudo apt-get update",
            "sudo apt-get install -y wget gnupg",
            "wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -",
            "echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | sudo tee /etc/apt/sources.list.d/google-chrome.list",
            "sudo apt-get update",
            "sudo apt-get install -y google-chrome-stable",
            "sudo apt-get install -y chromium-chromedriver"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Installing Chrome/ChromeDriver: {cmd}"):
                return False
                
    elif system == "darwin":
        # macOS
        commands = [
            "brew install --cask google-chrome",
            "brew install chromedriver"
        ]
        
        for cmd in commands:
            if not run_command(cmd, f"Installing Chrome/ChromeDriver: {cmd}"):
                return False
                
    elif system == "windows":
        print("⚠️ Windows: Please install Chrome manually from https://www.google.com/chrome/")
        print("⚠️ ChromeDriver will be managed automatically by webdriver-manager")
        
    return True

def setup_python_environment():
    """Setup Python virtual environment and install packages"""
    
    # Create virtual environment
    if not run_command("python3 -m venv rpa_env", "Creating Python virtual environment"):
        return False
    
    # Activate and install packages
    if platform.system().lower() == "windows":
        activate_cmd = "rpa_env\\Scripts\\activate"
    else:
        activate_cmd = "source rpa_env/bin/activate"
    
    install_cmd = f"{activate_cmd} && pip install -r requirements.txt"
    if not run_command(install_cmd, "Installing Python packages"):
        return False
    
    return True

def create_config_file():
    """Create RPA configuration file"""
    config_content = """# RPA Configuration
RPA_HEADLESS=true
RPA_TIMEOUT=30
RPA_IMPLICIT_WAIT=10
RPA_PAGE_LOAD_TIMEOUT=30

# Chrome Options
CHROME_NO_SANDBOX=true
CHROME_DISABLE_DEV_SHM=true
CHROME_DISABLE_GPU=true
CHROME_WINDOW_SIZE=1920,1080

# Logging
LOG_LEVEL=INFO
LOG_FILE=rpa_automation.log

# DGVCL Specific
DGVCL_BASE_URL=https://portal.guvnl.in
DGVCL_LOGIN_TIMEOUT=60
DGVCL_OTP_TIMEOUT=120
"""
    
    with open(".env", "w") as f:
        f.write(config_content)
    
    print("✅ Configuration file created: .env")
    return True

def test_setup():
    """Test the RPA setup"""
    print("🧪 Testing RPA setup...")
    
    test_script = """
import sys
sys.path.append('.')
from dgvcl_rpa_bot import DGVCLRPABot

# Test bot initialization
bot = DGVCLRPABot(headless=True)
if bot.setup_driver():
    print("✅ RPA Bot setup successful!")
    bot.driver.quit()
    exit(0)
else:
    print("❌ RPA Bot setup failed!")
    exit(1)
"""
    
    with open("test_setup.py", "w") as f:
        f.write(test_script)
    
    # Run test
    if platform.system().lower() == "windows":
        test_cmd = "rpa_env\\Scripts\\python test_setup.py"
    else:
        test_cmd = "source rpa_env/bin/activate && python test_setup.py"
    
    success = run_command(test_cmd, "Testing RPA setup")
    
    # Cleanup
    os.remove("test_setup.py")
    
    return success

def main():
    """Main setup function"""
    print("🚀 Setting up RPA Automation Environment...")
    print("=" * 50)
    
    # Change to RPA directory
    rpa_dir = Path(__file__).parent
    os.chdir(rpa_dir)
    
    steps = [
        (install_chrome_driver, "Install Chrome and ChromeDriver"),
        (setup_python_environment, "Setup Python environment"),
        (create_config_file, "Create configuration file"),
        (test_setup, "Test RPA setup")
    ]
    
    for step_func, description in steps:
        print(f"\n📋 {description}")
        if not step_func():
            print(f"❌ Setup failed at: {description}")
            sys.exit(1)
    
    print("\n🎉 RPA Automation setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Update backend/app/main.py to include RPA router")
    print("2. Update frontend to call RPA endpoints")
    print("3. Test with: python dgvcl_rpa_bot.py")
    print("\n🔧 Usage:")
    print("- Headless mode: DGVCLRPABot(headless=True)")
    print("- GUI mode: DGVCLRPABot(headless=False)")

if __name__ == "__main__":
    main()