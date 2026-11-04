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
            body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 20px; box-sizing: border-box; }
            .container { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; width: 100%; max-width: 800px; }
            h2 { color: #1e293b; margin-bottom: 30px; font-weight: 600; }
            input { width: 100%; padding: 14px; margin: 10px 0; border: 1px solid #e2e8f0; border-radius: 8px; box-sizing: border-box; font-size: 15px; background-color: #f8fafc; }
            button { padding: 14px; background-color: #2563eb; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: 500; margin-top: 10px; transition: 0.3s;}
            button:hover { background-color: #1d4ed8; }
            
            /* Admin Panel uslublari */
            #dashboard { display: none; text-align: left; }
            .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; padding-bottom: 20px; margin-bottom: 20px; }
            .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
            .tab-btn { background: #f1f5f9; color: #334155; width: auto; padding: 10px 20px; margin: 0; border-radius: 8px; border: 1px solid #e2e8f0; }
            .tab-btn.active { background: #2563eb; color: white; border-color: #2563eb; }
            
            .card { background: #f8fafc; border: 1px solid #e2e8f0; padding: 15px; border-radius: 8px; margin-bottom: 15px; display: flex; justify-content: space-between; align-items: center; }
            .status { padding: 5px 10px; border-radius: 20px; font-size: 12px; font-weight: bold; }
            .status-pending { background: #fef08a; color: #854d0e; }
            .status-approved { background: #dcfce7; color: #166534; }
            
            .btn-approve { background-color: #22c55e; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; width: auto; margin: 0 5px 0 0; font-size: 14px; }
            .btn-reject { background-color: #ef4444; color: white; padding: 8px 15px; border: none; border-radius: 5px; cursor: pointer; width: auto; margin: 0; font-size: 14px; }
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
                <h2>Admin Panel</h2>
                <button class="logout-btn" onclick="logout()">Chiqish</button>
            </div>
            
            <div class="tabs">
                <button class="tab-btn active" id="tabUsers" onclick="switchTab('users')">👥 Foydalanuvchilar</button>
                <button class="tab-btn" id="tabContracts" onclick="switchTab('contracts')">📄 Shartnomalar</button>
            </div>
            
            <div id="contentList">
                <p style="text-align: center; color: #64748b;">Yuklanmoqda...</p>
            </div>
        </div>

        <script>
            let authToken = null;
            let currentTab = 'users';

            async function login() {
                const phone = document.getElementById('phone').value;
                const password = document.getElementById('password').value;
                const msg = document.getElementById('message');
                const btn = document.getElementById('loginBtn');
                
                if (!phone || !password) { msg.textContent = "Iltimos, barcha maydonlarni to'ldiring"; return; }

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
                        authToken = data.access_token;
                        document.getElementById('loginPage').style.display = 'none';
                        document.getElementById('dashboard').style.display = 'block';
                        switchTab('users');
                    } else {
                        msg.textContent = data.detail || "Xatolik yuz berdi";
                    }
                } catch (error) { msg.textContent = "Serverga ulanib bo'lmadi"; } 
                finally { btn.disabled = false; }
            }

            function switchTab(tab) {
                currentTab = tab;
                document.getElementById('tabUsers').className = tab === 'users' ? 'tab-btn active' : 'tab-btn';
                document.getElementById('tabContracts').className = tab === 'contracts' ? 'tab-btn active' : 'tab-btn';
                if (tab === 'users') loadUsers(); else loadContracts();
            }

            async function loadUsers() {
                const list = document.getElementById('contentList');
                list.innerHTML = `<p style="text-align: center; color: #64748b;">Yuklanmoqda...</p>`;
                try {
                    const response = await fetch('https://buxgalteriya-api.onrender.com/admin/users', {
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    if (!response.ok) throw new Error("Xatolik");
                    const users = await response.json();
                    
                    if (users.length === 0) { list.innerHTML = `<p style="text-align: center;">Foydalanuvchilar yo'q</p>`; return; }

                    let html = "";
                    for (let u of users) {
                        let statusClass = u.status === 'pending' ? 'status-pending' : 'status-approved';
                        let statusText = u.status === 'pending' ? 'Kutilmoqda' : 'Tasdiqlangan';
                        html += `
                            <div class="card">
                                <div>
                                    <h4 style="margin: 0 0 5px 0;">${u.first_name} ${u.last_name} (${u.company})</h4>
                                    <small style="color: #64748b;">Tel: ${u.phone} | Sana: ${u.created_at}</small>
                                </div>
                                <div>
                                    <span class="status ${statusClass}">${statusText}</span>
                                    ${u.status === 'pending' ? `<button class="btn-approve" onclick="changeUserStatus(${u.id}, 'approve')">Tasdiqlash</button>` : ''}
                                </div>
                            </div>`;
                    }
                    list.innerHTML = html;
                } catch (error) { list.innerHTML = `<p style="color: red; text-align: center;">Xatolik yuz berdi</p>`; }
            }

            async function loadContracts() {
                const list = document.getElementById('contentList');
                list.innerHTML = `<p style="text-align: center; color: #64748b;">Yuklanmoqda...</p>`;
                try {
                    const response = await fetch('https://buxgalteriya-api.onrender.com/contracts/list', {
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    if (!response.ok) throw new Error("Xatolik");
                    const contracts = await response.json();
                    
                    if (contracts.length === 0) { list.innerHTML = `<p style="text-align: center;">Shartnomalar yo'q</p>`; return; }

                    let html = "";
                    for (let c of contracts) {
                        html += `
                            <div class="card">
                                <div>
                                    <h4 style="margin: 0 0 5px 0;">Shartnoma № ${c.number} - ${c.firma}</h4>
                                    <small style="color: #64748b;">INN: ${c.inn} | Sana: ${c.date} | Kompaniya: ${c.company.toUpperCase()}</small>
                                </div>
                                <div>
                                    <span class="status status-approved">Yuborilgan</span>
                                </div>
                            </div>`;
                    }
                    list.innerHTML = html;
                } catch (error) { list.innerHTML = `<p style="color: red; text-align: center;">Xatolik yuz berdi</p>`; }
            }

            async function changeUserStatus(userId, action) {
                try {
                    const response = await fetch(`https://buxgalteriya-api.onrender.com/admin/users/${userId}/${action}`, {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${authToken}` }
                    });
                    if (response.ok) loadUsers();
                } catch (error) { alert("Xatolik"); }
            }

            function logout() {
                authToken = null;
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
