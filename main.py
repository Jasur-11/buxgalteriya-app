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
        <title>Admin Panel - Buxgalteriya</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
            .container { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; width: 400px; }
            h2 { color: #1e293b; margin-bottom: 30px; font-weight: 600; }
            input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #e2e8f0; border-radius: 8px; box-sizing: border-box; font-size: 15px; background-color: #f8fafc; }
            input:focus { border-color: #3b82f6; outline: none; background-color: white; }
            button { width: 100%; padding: 14px; background-color: #2563eb; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 500; margin-top: 10px; }
            button:hover { background-color: #1d4ed8; }
            button:disabled { background-color: #94a3b8; cursor: not-allowed; }
            
            /* Admin Panel uslublari */
            #dashboard { display: none; width: 800px; text-align: left; }
            .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 20px; }
            .card { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
            .status { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; background: #fef08a; color: #854d0e; }
            .btn-approve { background-color: #22c55e; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; width: auto; margin: 0; }
            .btn-approve:hover { background-color: #16a34a; }
            .logout-btn { background-color: #fee2e2; color: #dc2626; border: 1px solid #fecaca; width: auto; padding: 10px 20px; margin: 0;}
        </style>
    </head>
    <body>
        <!-- Kirish oynasi -->
        <div class="container" id="loginPage">
            <h2>👨‍💼 Admin Panel</h2>
            <input type="text" id="phone" placeholder="Admin telefoni (+998...)">
            <input type="password" id="password" placeholder="Parol">
            <button id="loginBtn" onclick="login()">Tizimga kirish</button>
            <p id="message" style="color: #dc2626; font-size: 14px;"></p>
        </div>

        <!-- Asosiy Admin sahifasi -->
        <div class="container" id="dashboard">
            <div class="header">
                <h2>📋 Mijozlar so'rovlari</h2>
                <button class="logout-btn" onclick="logout()">Chiqish</button>
            </div>
            
            <div id="requestsList">
                <!-- Bu yerga API dan kelgan so'rovlar chiqadi -->
                <p style="text-align: center; color: #64748b;">Yuklanmoqda...</p>
            </div>
        </div>

        <script>
            async function login() {
                const phone = document.getElementById('phone').value;
                const password = document.getElementById('password').value;
                const msg = document.getElementById('message');
                const btn = document.getElementById('loginBtn');
                
                if (!phone || !password) {
                    msg.textContent = "Iltimos, barcha maydonlarni to'ldiring";
                    return;
                }

                msg.textContent = "Tekshirilmoqda...";
                msg.style.color = "#2563eb";
                btn.disabled = true;

                try {
                    const response = await fetch('https://buxgalteriya-api.onrender.com/auth/login', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ phone: phone, password: password })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        msg.textContent = "";
                        document.getElementById('loginPage').style.display = 'none';
                        document.getElementById('dashboard').style.display = 'block';
                        // So'rovlarni yuklash funksiyasini chaqiramiz
                        loadRequests();
                    } else {
                        msg.textContent = data.detail || "Xatolik yuz berdi";
                    }
                } catch (error) {
                    msg.textContent = "Serverga ulanib bo'lmadi";
                } finally {
                    btn.disabled = false;
                }
            }

            async function loadRequests() {
                const list = document.getElementById('requestsList');
                try {
                    // API dan shartnomalar ro'yxatini olish (keyinchalik yozamiz)
                    // Hozircha test uchun statik ma'lumot chiqaramiz
                    list.innerHTML = `
                        <div class="card">
                            <div>
                                <h4 style="margin: 0 0 5px 0;">Firma: ABC MChJ</h4>
                                <small style="color: #64748b;">Agent: Ali Valiyev | Sana: 03.11.2026</small>
                            </div>
                            <div>
                                <span class="status">Kutilmoqda</span>
                                <button class="btn-approve">Tasdiqlash</button>
                            </div>
                        </div>
                    `;
                } catch (error) {
                    list.innerHTML = `<p style="color: red;">Xatolik yuz berdi</p>`;
                }
            }

            function logout() {
                document.getElementById('dashboard').style.display = 'none';
                document.getElementById('loginPage').style.display = 'block';
                document.getElementById('phone').value = '';
                document.getElementById('password').value = '';
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8550))
    uvicorn.run(app, host="0.0.0.0", port=port)
