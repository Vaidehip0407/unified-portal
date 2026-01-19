"""
DGVCL Portal Proxy - Auto-fills form data
Opens DGVCL portal with pre-filled data without extension
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import httpx

router = APIRouter(prefix="/dgvcl-proxy", tags=["DGVCL Proxy"])

@router.get("/login", response_class=HTMLResponse)
async def proxy_dgvcl_login(mobile: str = "", discom: str = "DGVCL"):
    """
    Proxy DGVCL login page with auto-fill script injected
    User opens: /dgvcl-proxy/login?mobile=9876543210&discom=DGVCL
    """
    
    # Auto-fill script that runs when page loads
    autofill_script = f"""
    <script>
    (function() {{
        const mobile = "{mobile}";
        const discom = "{discom}";
        
        function fillForm() {{
            // Fill mobile number
            const mobileInput = document.querySelector('input[placeholder="Mobile No"]');
            if (mobileInput && mobile) {{
                mobileInput.value = mobile;
                mobileInput.dispatchEvent(new Event('input', {{bubbles: true}}));
                console.log('✅ Mobile filled:', mobile);
            }}
            
            // Fill discom dropdown
            const discomSelect = document.getElementById('discom');
            if (discomSelect && discom) {{
                for (let i = 0; i < discomSelect.options.length; i++) {{
                    if (discomSelect.options[i].text.toUpperCase().includes(discom.toUpperCase())) {{
                        discomSelect.selectedIndex = i;
                        discomSelect.dispatchEvent(new Event('change', {{bubbles: true}}));
                        console.log('✅ Discom selected:', discom);
                        break;
                    }}
                }}
            }}
            
            // Show success message
            if (mobile && mobileInput) {{
                const banner = document.createElement('div');
                banner.innerHTML = '✅ Auto-filled: ' + mobile + ' / ' + discom;
                banner.style.cssText = 'position:fixed;top:0;left:0;right:0;background:#22c55e;color:white;padding:10px;text-align:center;font-weight:bold;z-index:99999;';
                document.body.prepend(banner);
                setTimeout(() => banner.remove(), 5000);
            }}
        }}
        
        // Run when DOM is ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', fillForm);
        }} else {{
            setTimeout(fillForm, 1000);
        }}
    }})();
    </script>
    """
    
    # Create a page that redirects to DGVCL with auto-fill
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Opening DGVCL Portal...</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }}
            .container {{
                text-align: center;
                padding: 40px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
            }}
            .spinner {{
                width: 50px;
                height: 50px;
                border: 5px solid rgba(255,255,255,0.3);
                border-top-color: white;
                border-radius: 50%;
                animation: spin 1s linear infinite;
                margin: 20px auto;
            }}
            @keyframes spin {{
                to {{ transform: rotate(360deg); }}
            }}
            .data {{
                background: rgba(0,0,0,0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .btn {{
                display: inline-block;
                padding: 15px 30px;
                background: #22c55e;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                margin-top: 20px;
                cursor: pointer;
                border: none;
                font-size: 16px;
            }}
            .btn:hover {{
                background: #16a34a;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 Opening DGVCL Portal</h1>
            <div class="spinner"></div>
            <p>Your data will be auto-filled!</p>
            <div class="data">
                <p><strong>📱 Mobile:</strong> {mobile}</p>
                <p><strong>🏢 Discom:</strong> {discom}</p>
            </div>
            <p id="status">Redirecting in <span id="countdown">3</span> seconds...</p>
            <button class="btn" onclick="openPortal()">Open Now →</button>
        </div>
        
        <script>
            const mobile = "{mobile}";
            const discom = "{discom}";
            
            // Countdown
            let count = 3;
            const countdown = document.getElementById('countdown');
            const interval = setInterval(() => {{
                count--;
                countdown.textContent = count;
                if (count <= 0) {{
                    clearInterval(interval);
                    openPortal();
                }}
            }}, 1000);
            
            function openPortal() {{
                // Store data in sessionStorage for the bookmarklet
                sessionStorage.setItem('dgvcl_mobile', mobile);
                sessionStorage.setItem('dgvcl_discom', discom);
                
                // Open DGVCL portal
                const url = 'https://portal.guvnl.in/login.php?mobile=' + mobile + '&discom=' + discom;
                window.location.href = url;
            }}
        </script>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html_content)


@router.get("/autofill-page", response_class=HTMLResponse)
async def autofill_instructions(mobile: str = "", discom: str = "DGVCL"):
    """
    Page with one-click auto-fill button
    """
    
    bookmarklet_code = f"javascript:(function(){{var m='{mobile}';var d='{discom}';var i=document.querySelector('input[placeholder=\"Mobile No\"]');if(i){{i.value=m;i.dispatchEvent(new Event('input',{{bubbles:true}}));}}var s=document.getElementById('discom');if(s){{for(var j=0;j<s.options.length;j++){{if(s.options[j].text.toUpperCase().includes(d.toUpperCase())){{s.selectedIndex=j;s.dispatchEvent(new Event('change',{{bubbles:true}}));break;}}}}}}alert('✅ Filled: '+m+' / '+d);}})();"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>DGVCL Auto-Fill</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 600px;
                margin: 50px auto;
                padding: 20px;
                background: #f5f5f5;
            }}
            .card {{
                background: white;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }}
            h1 {{ color: #1e40af; }}
            .data-box {{
                background: #dbeafe;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
            }}
            .step {{
                background: #f0fdf4;
                padding: 15px;
                border-radius: 10px;
                margin: 10px 0;
                border-left: 4px solid #22c55e;
            }}
            .btn {{
                display: inline-block;
                padding: 15px 30px;
                background: #2563eb;
                color: white;
                text-decoration: none;
                border-radius: 10px;
                font-weight: bold;
                margin: 10px 5px;
            }}
            .btn-green {{
                background: #22c55e;
            }}
            .btn:hover {{
                opacity: 0.9;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>🎯 DGVCL Auto-Fill</h1>
            
            <div class="data-box">
                <h3>Your Data:</h3>
                <p><strong>📱 Mobile:</strong> {mobile}</p>
                <p><strong>🏢 Discom:</strong> {discom}</p>
            </div>
            
            <h2>📋 Steps:</h2>
            
            <div class="step">
                <strong>Step 1:</strong> Click button below to open DGVCL Portal
            </div>
            
            <div class="step">
                <strong>Step 2:</strong> Once page loads, press <kbd>F12</kbd> → Console tab
            </div>
            
            <div class="step">
                <strong>Step 3:</strong> Paste this code and press Enter:
                <pre style="background:#1e293b;color:#22c55e;padding:10px;border-radius:5px;overflow-x:auto;font-size:12px;">
var m='{mobile}';var d='{discom}';
document.querySelector('input[placeholder="Mobile No"]').value=m;
document.getElementById('discom').value=d.toUpperCase();
                </pre>
            </div>
            
            <div style="text-align:center;margin-top:30px;">
                <a href="https://portal.guvnl.in/login.php?mobile={mobile}&discom={discom}" 
                   target="_blank" class="btn btn-green">
                    🚀 Open DGVCL Portal
                </a>
            </div>
        </div>
    </body>
    </html>
    """
    
    return HTMLResponse(content=html)
