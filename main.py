import flet as ft
import httpx

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
            response = httpx.post(
                f"{API_URL}/auth/login",
                json={"phone": phone_input.value, "password": password_input.value}
            )
            
            if response.status_code == 200:
                # Muvaffaqiyatli kirish
                data = response.json()
                message_text.value = "Tizimga kirdingiz! (Keyingi oynalar keyin qo'shiladi)"
                message_text.color = ft.colors.GREEN
                # Bu yerda keyinchalik asosiy sahifaga o'tish kodi yoziladi
            else:
                # Xato
                detail = response.json().get("detail", "Xatolik yuz berdi")
                message_text.value = detail
                message_text.color = ft.colors.RED
                
        except Exception as ex:
            message_text.value = f"Serverga ulanib bo'lmadi: {ex}"
            message_text.color = ft.colors.RED
            
        page.splash = None
        page.update()

    login_button = ft.ElevatedButton(text="Kirish", on_click=login_clicked, width=300)

    # Ro'yxatdan o'tishga o'tish tugmasi (hozircha faqat matn)
    register_button = ft.TextButton(
        text="Akkountingiz yo'qmi? Ro'yxatdan o'tish",
        on_click=lambda _: page.go("/register") # Keyinchalik sahifa qo'shiladi
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

# Ilovani ishga tushirish (Render uchun Web rejimda)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8550))
    ft.app(target=main, view=ft.AppView.WEB_BROWSER, port=port, host="0.0.0.0")