import flet as ft
import flet.fastapi as flet_fastapi
import httpx
import os
from fastapi import FastAPI

# API manzilimiz
API_URL = "https://buxgalteriya-api.onrender.com"

def main(page: ft.Page):
    page.title = "Buxgalteriya Ilovasi"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Kirish maydonlari
    phone_input = ft.TextField(label="Telefon raqam", hint_text="+998901234567", width=300)
    password_input = ft.TextField(label="Parol", password=True, can_reveal_password=True, width=300)
    
    # Xabar (agar xato bo'lsa)
    message_text = ft.Text(value="", color=ft.colors.RED)

    def login_clicked(e):
        page.splash = ft.ProgressBar()
        page.update()
        
        try:
            # API ga so'rov yuborish
            response = httpx.post(
                f"{API_URL}/auth/login",
                json={"phone": phone_input.value, "password": password_input.value},
                timeout=20.0
            )
            
            if response.status_code == 200:
                data = response.json()
                message_text.value = "Tizimga muvaffaqiyatli kirdingiz!"
                message_text.color = ft.colors.GREEN
                # Bu yerda keyinchalik asosiy sahifaga o'tish kodi yoziladi
            else:
                detail = response.json().get("detail", "Xatolik yuz berdi")
                message_text.value = detail
                message_text.color = ft.colors.RED
                
        except Exception as ex:
            message_text.value = f"Serverga ulanib bo'lmadi: {ex}"
            message_text.color = ft.colors.RED
            
        page.splash = None
        page.update()

    login_button = ft.ElevatedButton(text="Kirish", on_click=login_clicked, width=300)

    # Ro'yxatdan o'tishga o'tish tugmasi
    register_button = ft.TextButton(
        text="Akkountingiz yo'qmi? Ro'yxatdan o'tish",
        on_click=lambda _: page.go("/register")
    )

    # Oynaga joylash
    page.add(
        ft.Column(
            [
                ft.Icon(ft.icons.ACCOUNT_CIRCLE, size=80, color=ft.colors.BLUE),
                ft.Text("Tizimga kirish", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                phone_input,
                password_input,
                message_text,
                ft.Container(height=10),
                login_button,
                register_button
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

# ==========================================
# FASTAPI VA FLET INTEGRATSIYASI
# ==========================================

# FastAPI ilovasini yaratamiz
app = FastAPI()

# Flet'ni FastAPI ga ulaymiz (Bu xatolarni oldini oladi)
app.mount("/web", flet_fastapi.app(main), name="web")

@app.get("/")
def read_root():
    return {"message": "Ilova ishlayapti. Iltimos /web manziliga o'ting."}

# Render uchun portni aniqlash va serverni ishga tushirish
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8550))
    uvicorn.run(app, host="0.0.0.0", port=port)
