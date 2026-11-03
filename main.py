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
        <title>Buxgalteriya Ilovasi</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background-color: #f0f2f5; }
            .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; width: 300px; }
            input { width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 10px; background-color: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background-color: #0056b3; }
            button:disabled { background-color: #cccccc; cursor: not-allowed; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Tizimga kirish</h2>
            <input type="text" id="phone" placeholder="Telefon raqam (+998...)">
            <input type="password" id="password" placeholder="Parol">
            <button id="loginBtn" onclick="login()">Kirish</button>
            <p id="message" style="color: red;"></p>
        </div>
        <script>
            async function login() {
                const phone = document.getElementById('phone').value;
                const password = document.getElementById('password').value;
                const msg = document.getElementById('message');
                const btn = document.getElementById('loginBtn');
                
                if (!phone || !password) {
                    msg.textContent = "Iltimos, barcha maydonlarni to'ldiring";
                    msg.style.color = "red";
                    return;
                }

                msg.textContent = "Kutilmoqda... (Server uyg'onishi 50 soniya olishi mumkin)";
                msg.style.color = "blue";
                btn.disabled = true;

                // API uyg'onishini kutish uchun 60 soniya vaqt beramiz
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
                        msg.textContent = "Muvaffaqiyatli kirdingiz!";
                        msg.style.color = "green";
                    } else {
                        msg.textContent = data.detail || "Xatolik yuz berdi";
                        msg.style.color = "red";
                    }
                } catch (error) {
                    clearTimeout(timeoutId);
                    if (error.name === 'AbortError') {
                        msg.textContent = "Server javob bermadi (vaqt tugadi)";
                    } else {
                        msg.textContent = "Serverga ulanib bo'lmadi";
                    }
                    msg.style.color = "red";
                } finally {
                    btn.disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8550))
    uvicorn.run(app, host="0.0.0.0", port=port)
