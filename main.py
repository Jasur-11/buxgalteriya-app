from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Buxgalteriya Tizimi</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            /* Zamonaviy shrift va fon */
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                margin: 0; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            }
            
            /* Oq karta dizayni */
            .container { 
                background: white; 
                padding: 40px; 
                border-radius: 16px; 
                box-shadow: 0 10px 25px rgba(0,0,0,0.05); 
                text-align: center; 
                width: 350px; 
            }
            
            h2 {
                color: #1e293b;
                margin-bottom: 30px;
                font-weight: 600;
            }

            /* Kiritish maydonlari */
            input { 
                width: 100%; 
                padding: 14px; 
                margin: 10px 0; 
                border: 1px solid #e2e8f0; 
                border-radius: 8px; 
                box-sizing: border-box; 
                font-size: 15px;
                transition: border-color 0.3s;
                background-color: #f8fafc;
            }
            input:focus {
                border-color: #3b82f6;
                outline: none;
                background-color: white;
            }
            
            /* Tugmalar */
            button { 
                width: 100%; 
                padding: 14px; 
                background-color: #2563eb; 
                color: white; 
                border: none; 
                border-radius: 8px; 
                cursor: pointer; 
                font-size: 16px; 
                font-weight: 500;
                transition: background-color 0.3s, transform 0.1s;
                margin-top: 10px;
            }
            button:hover { 
                background-color: #1d4ed8; 
            }
            button:active {
                transform: scale(0.98);
            }
            button:disabled { 
                background-color: #94a3b8; 
                cursor: not-allowed; 
            }
            
            /* Asosiy menyu tugmalari */
            .menu-btn { 
                background-color: white; 
                color: #1e293b;
                border: 1px solid #e2e8f0;
                margin-bottom: 12px; 
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 10px;
            }
            .menu-btn:hover { 
                background-color: #f8fafc; 
                border-color: #cbd5e1;
            }
            
            .logout-btn {
                background-color: #fee2e2;
                color: #dc2626;
                border: 1px solid #fecaca;
                margin-top: 20px;
            }
            .logout-btn:hover {
                background-color: #fecaca;
            }

            #dashboard { display: none; }
            #message { font-size: 14px; margin-top: 15px; font-weight: 500; }
        </style>
    </head>
    <body>
        <!-- Kirish oynasi -->
        <div class="container" id="loginPage">
            <h2>Tizimga kirish</h2>
            <input type="text" id="phone" placeholder="Telefon raqam (+998...)">
            <input type="password" id="password" placeholder="Parol">
            <button id="loginBtn" onclick="login()">Kirish</button>
            <p id="message"></p>
        </div>

        <!-- Asosiy sahifa (Dashboard) -->
        <div class="container" id="dashboard">
            <h2>Asosiy Menyu</h2>
            <button class="menu-btn" onclick="alert('Shartnoma yaratish sahifasi tez kunda!')">📄 Shartnoma yaratish</button>
            <button class="menu-btn" onclick="alert('Spetsifikatsiya yaratish sahifasi tez kunda!')">📊 Spetsifikatsiya yaratish</button>
            <button class="logout-btn" onclick="logout()">Chiqish</button>
        </div>

        <script>
            async function login() {
                const phone = document.getElementById('phone').value;
                const password = document.getElementById('password').value;
                const msg = document.getElementById('message');
                const btn = document.getElementById('loginBtn');
                
                if (!phone || !password) {
                    msg.textContent = "Iltimos, barcha maydonlarni to'ldiring";
                    msg.style.color = "#dc2626";
                    return;
                }

                msg.textContent = "Tekshirilmoqda... (50 soniyagacha kutish mumkin)";
                msg.style.color = "#2563eb";
                btn.disabled = true;

                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 60000);

                try {
                    const response = await fetch('https://buxgalteriya-api.onrender.com/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ phone: phone, password: password }),
                        signal: controller.signal
                    });
                    
                    clearTimeout(timeoutId);
                    const data = await response.json();
                    
                    if (response.ok) {
                        msg.textContent = "";
                        document.getElementById('loginPage').style.display = 'none';
                        document.getElementById('dashboard').style.display = 'block';
                    } else {
                        msg.textContent = data.detail || "Xatolik yuz berdi";
                        msg.style.color = "#dc2626";
                    }
                } catch (error) {
                    clearTimeout(timeoutId);
                    msg.textContent = "Serverga ulanib bo'lmadi";
                    msg.style.color = "#dc2626";
                } finally {
                    btn.disabled = false;
                }
            }

            function logout() {
                document.getElementById('dashboard').style.display = 'none';
                document.getElementById('loginPage').style.display = 'block';
                document.getElementById('phone').value = '';
                document.getElementById('password').value = '';
                document.getElementById('message').textContent = '';
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8550))
    uvicorn.run(app, host="0.0.0.0", port=port)
