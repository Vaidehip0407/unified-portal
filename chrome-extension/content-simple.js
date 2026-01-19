// DGVCL Complete Auto-Fill Extension - v4.0 (Login + New Connection)
console.log('🚀 DGVCL Extension v4.0 - Login + New Connection Support');

// Run on page load
window.addEventListener('load', runExtension);
document.addEventListener('DOMContentLoaded', runExtension);

function runExtension() {
  if (!window.location.hostname.includes('guvnl.in')) return;
  
  const url = window.location.href;
  console.log('🔍 Page:', url);
  
  // LOGIN FLOW
  if (url.includes('login.php')) {
    setTimeout(handleLogin, 1000);
  }
  else if (url.includes('checkOtp.php')) {
    setTimeout(handleOTP, 500);
  }
  else if (url.includes('Submit_Otp.php')) {
    setTimeout(handleSelectUser, 1000);
  }
  else if (url.includes('prtlDashboard.php')) {
    handleDashboard();
  }
  
  // NEW CONNECTION FLOW
  else if (url.includes('LTConsumerReg.php')) {
    setTimeout(handleNewConnectionForm, 2000);
  }
}

// ============ LOGIN FLOW ============
function handleLogin() {
  const params = new URLSearchParams(window.location.search);
  const mobile = params.get('mobile');
  const discom = params.get('discom');
  
  if (!mobile) return;
  
  console.log('📱 Login - Filling:', mobile, discom);
  
  // Fill Mobile
  const mobileInput = document.querySelector('input[placeholder="Mobile No"]') ||
                     document.querySelector('input[type="text"]:not([placeholder*="Captcha"])');
  
  if (mobileInput && !mobileInput.placeholder.includes('Captcha')) {
    mobileInput.value = mobile;
    mobileInput.dispatchEvent(new Event('input', {bubbles: true}));
    mobileInput.style.background = '#c8f7c5';
    console.log('✅ Mobile filled');
  }
  
  // Fill DISCOM
  const select = document.querySelector('select');
  if (select && discom) {
    for (let opt of select.options) {
      if (opt.text.toUpperCase().includes(discom.toUpperCase())) {
        select.value = opt.value;
        select.dispatchEvent(new Event('change', {bubbles: true}));
        select.style.background = '#c8f7c5';
        console.log('✅ DISCOM selected');
        break;
      }
    }
  }
  
  showMsg('✅ Auto-filled: ' + mobile + ' / ' + discom + '\n👉 Enter Captcha & Click Login', 'green');
}

function handleOTP() {
  showMsg('📱 Enter OTP sent to your mobile\n👉 Then click Submit Otp', 'blue');
  
  const otpInput = document.querySelector('input[placeholder*="OTP"]') || 
                   document.querySelector('input[type="text"]');
  if (otpInput) otpInput.focus();
}

function handleSelectUser() {
  console.log('📍 Auto-submitting user selection...');
  showMsg('🔄 Auto-submitting...', 'orange');
  
  const submitBtn = document.querySelector('input[value="Submit"]') ||
                   document.querySelector('input[type="submit"]');
  
  if (submitBtn) {
    submitBtn.click();
    console.log('✅ Submit clicked');
  }
}

function handleDashboard() {
  showMsg('✅ Login Successful!\n👉 Navigate to: New Connection → LT New Connection', 'green');
  
  // Check if we have new connection data
  const storedData = localStorage.getItem('dgvcl_autofill_data');
  if (storedData) {
    const data = JSON.parse(storedData);
    if (data.application_type === 'new_connection') {
      showMsg('🔥 New Connection data ready!\n👉 Go to: New Connection → LT New Connection', 'purple');
    }
  }
}

// ============ NEW CONNECTION FORM ============
function handleNewConnectionForm() {
  console.log('📍 LT New Connection Form detected');
  
  // Get stored data
  const storedData = localStorage.getItem('dgvcl_autofill_data');
  if (!storedData) {
    console.log('❌ No stored data found');
    return;
  }
  
  const data = JSON.parse(storedData);
  if (data.application_type !== 'new_connection') {
    console.log('❌ Not new connection data');
    return;
  }
  
  console.log('📦 Filling New Connection form with:', data);
  showMsg('🤖 Auto-filling New Connection form...', 'blue');
  
  let filled = 0;
  
  // Service Request Information
  if (data.consumer_type) {
    const consumerTypeSelect = document.querySelector('select[name*="consumer_type"], select[name*="ConsumerType"]');
    if (consumerTypeSelect) {
      selectOption(consumerTypeSelect, data.consumer_type);
      filled++;
    }
  }
  
  if (data.category) {
    const categorySelect = document.querySelector('select[name*="category"], select[name*="Category"]');
    if (categorySelect) {
      selectOption(categorySelect, data.category);
      filled++;
    }
  }
  
  if (data.area_type) {
    const areaTypeSelect = document.querySelector('select[name*="area"], select[name*="Area"]');
    if (areaTypeSelect) {
      selectOption(areaTypeSelect, data.area_type);
      filled++;
    }
  }
  
  // Applicant Details
  if (data.applicant_name) {
    const nameInput = document.querySelector('input[name*="name"], input[name*="Name"]');
    if (nameInput) {
      fillInput(nameInput, data.applicant_name);
      filled++;
    }
  }
  
  if (data.mobile) {
    const mobileInput = document.querySelector('input[name*="mobile"], input[name*="Mobile"]');
    if (mobileInput) {
      fillInput(mobileInput, data.mobile);
      filled++;
    }
  }
  
  if (data.email) {
    const emailInput = document.querySelector('input[name*="email"], input[name*="Email"]');
    if (emailInput) {
      fillInput(emailInput, data.email);
      filled++;
    }
  }
  
  // Address Details
  if (data.address_line1) {
    const addr1Input = document.querySelector('input[name*="address1"], input[name*="Address1"], textarea[name*="address"]');
    if (addr1Input) {
      fillInput(addr1Input, data.address_line1);
      filled++;
    }
  }
  
  if (data.address_line2) {
    const addr2Input = document.querySelector('input[name*="address2"], input[name*="Address2"]');
    if (addr2Input) {
      fillInput(addr2Input, data.address_line2);
      filled++;
    }
  }
  
  if (data.district) {
    const districtSelect = document.querySelector('select[name*="district"], select[name*="District"]');
    if (districtSelect) {
      selectOption(districtSelect, data.district);
      filled++;
    }
  }
  
  if (data.taluka) {
    const talukaInput = document.querySelector('input[name*="taluka"], input[name*="Taluka"], select[name*="taluka"]');
    if (talukaInput) {
      if (talukaInput.tagName === 'SELECT') {
        selectOption(talukaInput, data.taluka);
      } else {
        fillInput(talukaInput, data.taluka);
      }
      filled++;
    }
  }
  
  if (data.pincode) {
    const pincodeInput = document.querySelector('input[name*="pin"], input[name*="Pin"], input[name*="postal"]');
    if (pincodeInput) {
      fillInput(pincodeInput, data.pincode);
      filled++;
    }
  }
  
  if (data.nearest_consumer_no) {
    const nearestInput = document.querySelector('input[name*="nearest"], input[name*="Nearest"]');
    if (nearestInput) {
      fillInput(nearestInput, data.nearest_consumer_no);
      filled++;
    }
  }
  
  if (data.connection_load) {
    const loadInput = document.querySelector('input[name*="load"], input[name*="Load"], input[name*="kw"]');
    if (loadInput) {
      fillInput(loadInput, data.connection_load);
      filled++;
    }
  }
  
  if (filled > 0) {
    showMsg(`✅ Auto-filled ${filled} fields!\n👉 Review & Submit form`, 'green');
    console.log(`✅ Filled ${filled} fields in New Connection form`);
  } else {
    showMsg('⚠️ Could not find form fields\n👉 Please fill manually', 'orange');
  }
}

// Helper Functions
function fillInput(input, value) {
  input.focus();
  input.value = value;
  input.dispatchEvent(new Event('input', {bubbles: true}));
  input.dispatchEvent(new Event('change', {bubbles: true}));
  input.style.background = '#c8f7c5';
  input.style.border = '2px solid #27ae60';
}

function selectOption(select, value) {
  for (let opt of select.options) {
    if (opt.text.toUpperCase().includes(value.toUpperCase()) || 
        opt.value.toUpperCase().includes(value.toUpperCase())) {
      select.value = opt.value;
      select.dispatchEvent(new Event('change', {bubbles: true}));
      select.style.background = '#c8f7c5';
      select.style.border = '2px solid #27ae60';
      break;
    }
  }
}

function showMsg(text, color) {
  const colors = {
    green: '#27ae60',
    blue: '#3498db', 
    orange: '#e67e22',
    red: '#e74c3c',
    purple: '#9b59b6'
  };
  
  const old = document.getElementById('dgvcl-msg');
  if (old) old.remove();
  
  const div = document.createElement('div');
  div.id = 'dgvcl-msg';
  div.innerHTML = text.replace(/\n/g, '<br>');
  div.style.cssText = `
    position: fixed;
    top: 15px;
    right: 15px;
    background: ${colors[color] || colors.blue};
    color: white;
    padding: 15px 25px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: bold;
    z-index: 999999;
    box-shadow: 0 5px 25px rgba(0,0,0,0.3);
    max-width: 320px;
    line-height: 1.6;
  `;
  document.body.appendChild(div);
  
  setTimeout(() => { if(div.parentNode) div.remove(); }, 8000);
}

console.log('✅ DGVCL Extension Ready - Login + New Connection!');