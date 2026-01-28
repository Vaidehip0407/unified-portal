// Torrent Power Name Change Automation Script
// This script automates the complete flow for Torrent Power name change

class TorrentPowerAutomation {
    constructor() {
        this.userData = null;
        this.currentStep = 1;
        this.maxRetries = 5;
        this.retryCount = 0;
    }

    // Initialize automation with user data
    init(userData) {
        this.userData = userData;
        console.log('🚀 Starting Torrent Power Name Change Automation');
        this.startAutomation();
    }

    // Main automation flow
    async startAutomation() {
        const currentUrl = window.location.href;
        
        if (currentUrl.includes('connect.torrentpower.com')) {
            if (currentUrl.includes('/session/signin')) {
                await this.handleLoginPage();
            } else if (currentUrl.includes('/application/myapplications')) {
                await this.handleApplicationsPage();
            } else if (currentUrl.includes('/application/namechangerequest')) {
                await this.handleNameChangeForm();
            } else {
                // Start from main page
                await this.navigateToLogin();
            }
        } else {
            // Navigate to Torrent Power portal
            window.location.href = 'https://connect.torrentpower.com';
        }
    }

    // Step 1: Navigate to login page
    async navigateToLogin() {
        console.log('📍 Step 1: Navigating to login page');
        window.location.href = 'https://connect.torrentpower.com/tplcp/session/signin';
    }

    // Step 2: Handle login page (user needs to login manually)
    async handleLoginPage() {
        console.log('📍 Step 2: On login page - User needs to login manually');
        
        // Show notification to user
        this.showNotification('Please login to your Torrent Power account', 'info');
        
        // Wait for login completion and redirect
        this.waitForLoginCompletion();
    }

    // Wait for user to complete login
    waitForLoginCompletion() {
        const checkLogin = setInterval(() => {
            if (!window