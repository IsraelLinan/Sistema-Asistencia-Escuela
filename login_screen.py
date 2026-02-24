import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from colegio_lib import db_pool, COLORS, FONTS

# Configuración global de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión Escolar")
        self.configure(fg_color=COLORS["bg"])
        self.resizable(True, True)

        # Centrar ventana
        width, height = 420, 590
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - width) // 2
        y = (sh - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        self._build_ui()

    def _build_ui(self):
        # Panel central con fondo ligeramente diferente
        panel = ctk.CTkFrame(self, fg_color=COLORS["bg2"], corner_radius=20,
                             border_width=1, border_color=COLORS["border"])
        panel.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.88, relheight=0.88)

        # Logo
        try:
            logo_img = ctk.CTkImage(
                light_image=Image.open("logo_colegio.png"),
                dark_image=Image.open("logo_colegio.png"),
                size=(110, 110)
            )
            ctk.CTkLabel(panel, image=logo_img, text="").pack(pady=(30, 5))
        except Exception:
            ctk.CTkLabel(panel, text="🏫", font=("Segoe UI", 50)).pack(pady=(30, 5))

        # Título
        ctk.CTkLabel(panel, text="Bienvenido",
                     font=ctk.CTkFont("Segoe UI", 22, "bold"),
                     text_color=COLORS["text"]).pack(pady=(8, 2))
        ctk.CTkLabel(panel, text="Ingrese sus credenciales para continuar",
                     font=ctk.CTkFont("Segoe UI", 11),
                     text_color=COLORS["text_muted"]).pack(pady=(0, 25))

        # Campo usuario
        ctk.CTkLabel(panel, text="Usuario", font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=COLORS["text_muted"], anchor="w").pack(padx=35, fill="x")
        self.username_entry = ctk.CTkEntry(
            panel, placeholder_text="Ingrese su usuario",
            height=42, corner_radius=10,
            fg_color=COLORS["bg3"], border_color=COLORS["border"],
            text_color=COLORS["text"], font=ctk.CTkFont("Segoe UI", 12)
        )
        self.username_entry.pack(padx=35, pady=(4, 14), fill="x")

        # Campo contraseña
        ctk.CTkLabel(panel, text="Contraseña", font=ctk.CTkFont("Segoe UI", 11, "bold"),
                     text_color=COLORS["text_muted"], anchor="w").pack(padx=35, fill="x")
        self.password_entry = ctk.CTkEntry(
            panel, placeholder_text="Ingrese su contraseña",
            show="●", height=42, corner_radius=10,
            fg_color=COLORS["bg3"], border_color=COLORS["border"],
            text_color=COLORS["text"], font=ctk.CTkFont("Segoe UI", 12)
        )
        self.password_entry.pack(padx=35, pady=(4, 28), fill="x")
        self.password_entry.bind("<Return>", lambda e: self.verify_login())

        # Botón login
        self.login_btn = ctk.CTkButton(
            panel, text="Iniciar Sesión", height=44,
            corner_radius=10, font=ctk.CTkFont("Segoe UI", 13, "bold"),
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self.verify_login
        )
        self.login_btn.pack(padx=35, fill="x")

        # Status label
        self.status_label = ctk.CTkLabel(panel, text="",
                                          font=ctk.CTkFont("Segoe UI", 10),
                                          text_color=COLORS["danger"])
        self.status_label.pack(pady=(10, 0))

    def verify_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status_label.configure(text="⚠  Complete todos los campos.")
            return

        self.login_btn.configure(text="Verificando...", state="disabled")
        self.update()

        try:
            conn = db_pool.get_conn()
            cur = conn.cursor()
            cur.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s",
                        (username, password))
            result = cur.fetchone()
            cur.close()
            db_pool.put_conn(conn)

            if result:
                self.destroy()
                from main import MainApplication
                app = MainApplication()
                app.mainloop()
            else:
                self.status_label.configure(text="✗  Usuario o contraseña incorrectos.")
                self.login_btn.configure(text="Iniciar Sesión", state="normal")

        except Exception as e:
            self.status_label.configure(text=f"✗  Error de conexión.")
            self.login_btn.configure(text="Iniciar Sesión", state="normal")
            messagebox.showerror("Error", f"Error al verificar usuario: {e}")


if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()

